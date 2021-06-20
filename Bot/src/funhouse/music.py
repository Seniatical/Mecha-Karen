import re
import typing

import discord
import lavalink
from discord.ext import commands
from lavalink import format_time
import random
import asyncio
from duration import to_seconds
from requests.utils import requote_uri
from io import BytesIO
import asyncio
from itertools import accumulate

url_rx = re.compile(r'https?://(?:www\.)?.+')


def convert(time: int):
    mins = time // 60
    time %= 60
    return '%d:%d' % (mins, time)


class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        self.votes = {}
        self.session = __import__('aiohttp').ClientSession()
        self.gains = ([(1 * (i / 100)) for i in range(101)] + [-(1 * (i / 100)) for i in range(26)])
        self.filter_maps = {
            "flat": [
                (0, .0), (1, .0), (2, .0), (3, .0), (4, .0),
                (5, .0), (6, .0), (7, .0), (8, .0), (9, .0),
                (10, .0), (11, .0), (12, .0), (13, .0), (14, .0)
            ],
            "boost": [
                (0, -0.075), (1, .125), (2, .125), (3, .1), (4, .1),
                (5, .05), (6, 0.075), (7, .0), (8, .0), (9, .0),
                (10, .0), (11, .0), (12, .125), (13, .15), (14, .05)
            ],
            "metal": [
                (0, .0), (1, .1), (2, .1), (3, .15), (4, .13),
                (5, .1), (6, .0), (7, .125), (8, .175), (9, .175),
                (10, .125), (11, .125), (12, .1), (13, .075), (14, .0)
            ],
            "piano": [
                (0, -0.25), (1, -0.25), (2, -0.125), (3, 0.0),
                (4, 0.25), (5, 0.25), (6, 0.0), (7, -0.25), (8, -0.25),
                (9, 0.0), (10, 0.0), (11, 0.5), (12, 0.25), (13, -0.025)
            ],
            "bassboost": [
                (0, 0.01), (1, 0.25), (2, 0.64), (3, 0.44),
                (4, 0.46), (5, -0.03), (6, 0.98), (7, 0.13), (8, 0.77), (9, 0.25),
                (10, 0.01), (11, -0.04), (12, 0.18), (13, 0.78), (14, 0.27)
            ],
            "speed": [
                (0, 0.25), (1, 0.25), (2, 0.25), (3, 0.25),
                (4, 0.25), (5, 0.25), (6, 0.25), (7, 0.25), (8, 0.25), (9, 0.25),
                (10, 0.25), (11, 0.25), (12, 0.25), (13, 0.25), (14, 0.25)
            ],
            "crystal": [(0, 0.2), (1, -0.01), (2, 0.27), (3, -0.11), (4, 0.01), (5, 0.65),
                        (6, -0.24), (7, 0.39), (8, 0.6), (9, 0.08), (10, -0.07),
                        (11, -0.06), (12, 0.78), (13, 0.42), (14, 0.37)]
        }

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(740514706858442792)

            env = bot.env

            bot.lavalink.add_node(env('LAVALINK_SERVER_IP'), env('LAVALINK_SERVER_PORT'),
                                  env('LAVALINK_SERVER_PASSWORD'), env('LAVALINK_REGION'),
                                  env('LAVALINK_NODETYPE'))
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        if not bot.lavalink._event_hooks['Generic']:
            lavalink.add_event_hook(self.track_hook)

    def cog_unload(self) -> None:
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx):
        guild_check = ctx.guild is not None
        if guild_check and ctx.command.name not in ['lyrics', 'join']:
            await self.ensure_voice(ctx)
        return guild_check

    async def cog_command_error(self, ctx, error) -> None:
        if isinstance(error, lavalink.exceptions.NodeException):
            return await ctx.send('Woops, Looks like the node is full!')

        if isinstance(error, commands.errors.CommandInvokeError):
            return

    @staticmethod
    async def convert(milliseconds: int) -> int:
        seconds = milliseconds * 1000
        minutes = (seconds / 60)
        return int(minutes)

    async def random_filter(self, as_order=True) -> list:
        sync = list(range(15))
        if not as_order:
            random.shuffle(sync)
        groups = []
        for i in sync:
            gain = random.choice(self.gains)
            groups.append((i, gain))
        return groups

    async def ensure_voice(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play', 'join')

        if not ctx.author.voice or not ctx.author.voice.channel:
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(
                content='You must be a voice channel inorder to use this command!',
                mention_author=False)
            raise commands.errors.CommandInvokeError

        if not player.is_connected:
            if not should_connect:
                ctx.command.reset_cooldown(ctx)
                await ctx.message.reply(
                    content='I am currently not connected to any VC.',
                    mention_author=False)
                raise commands.errors.CommandInvokeError

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                ctx.command.reset_cooldown(ctx)
                await ctx.message.reply(
                    content='I am missing `CONNECT` or `SPEAK` permissions!',
                    mention_author=False)
                raise commands.errors.CommandInvokeError

            player.store('channel', ctx.channel.id)
            player.store('ctx', ctx)

            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))

            await asyncio.sleep(1)  ## Kept joining way too fast.
            await ctx.message.reply(
                content='Connected to **%s** and bound to **%s**!' % (ctx.me.voice.channel, ctx.channel),
                mention_author=False
            )

        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                ctx.command.reset_cooldown(ctx)
                await ctx.message.reply(
                    content='You need to be in the same vc as me!',
                    mention_author=False
                )
                raise commands.errors.CommandInvokeError

    async def track_hook(self, event) -> any:
        if isinstance(event, lavalink.events.QueueEndEvent):
            await asyncio.sleep(30)
            if event.player.is_playing:
                return
            guild_id = int(event.player.guild_id)
            ctx = event.player.fetch('ctx')
            if ctx:
                try:
                    await ctx.send('Left **%s** because I am no longer playing anything.' % ctx.me.voice.channel)
                except AttributeError:
                    await ctx.send('Left the channel because i am no longer playing anything.')

            event.player.delete('ctx')
            await self.connect_to(guild_id, None)

        if isinstance(event, lavalink.events.TrackStartEvent):
            ctx = event.player.fetch('ctx')
            track = event.track

            if ctx and not event.player.repeat:
                await ctx.send('Now playing **%s** requested by **%s**' % (
                    track.title, ctx.guild.get_member(int(track.requester))))

        if isinstance(event, lavalink.events.TrackStuckEvent):
            ctx = event.player.fetch('ctx')

            if ctx:
                await ctx.send('An error has occured whilst playing your track!')

    async def connect_to(self, guild_id: int, channel_id: typing.Union[str, None]) -> None:
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @staticmethod
    def convert_to_min_and_seconds(milliseconds: int):
        minutes = milliseconds // 60000
        seconds = round(((milliseconds % 60000) // 1000), 0)
        minutes = int(minutes)
        seconds = int(seconds)
        if len(str(seconds)) == 1:
            seconds = "0" + str(seconds)
        return f"{minutes}:{seconds}"

    @staticmethod
    def convert_to_milli(minute, second):
        minute = int(minute) * 60000
        second = int(second) * 1000
        return minute + second

    @staticmethod
    async def pretty_convert(num) -> str:
        if num >= (60 * 60):
            hours = num // (60 * 60)
            num %= (60 * 60)
            mins = num // 60
            num %= 60
            return '{}:{}:{}'.format(hours, mins, num)
        elif num > 60:
            mins = num // 60
            num %= 60
            return '{}:{}'.format(mins, num)
        else:
            return '00:{}'.format(num)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before: discord.VoiceState, after: discord.VoiceState):
        guild: typing.Optional[discord.Guild] = member.guild
        if not guild:
            return
        bot_voice_state: typing.Optional[discord.VoiceState] = guild.me.voice
        if not bot_voice_state:
            # BOT NOT IN A VC
            return
        voice_channel: typing.Optional[discord.VoiceChannel] = bot_voice_state.channel
        if not voice_channel:
            return

        player = self.bot.lavalink.player_manager.get(guild.id)

        if player:
            ctx = player.fetch('ctx')
        else:
            ctx = None

        if player.is_playing and ctx:
            if int(player.current.requester) == member.id:
                track = player.current
                await player.skip()
                await ctx.send('Automatically skipped **%s** as the requester left the channel' % track.title)

        if len(voice_channel.voice_states) == 1:
            # This means its just karen in the VC
            await asyncio.sleep(10)

            if len(voice_channel.voice_states) == 1:
                if player and ctx:
                    await ctx.send('Left **%s** as there is nobody in the VC.' % voice_channel.name)
                    player.delete('ctx')

                player.queue.clear()
                await player.reset_equalizer()
                await player.set_volume(100)
                player.repeat = False
                await player.stop()
                await self.connect_to(guild_id=guild.id, channel_id=None)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def join(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if ctx.author.voice and not player:

            try:
                await ctx.message.add_reaction('🎵')
            except Exception:
                pass
            return await self.ensure_voice(ctx)

        if ctx.author.voice and not player.is_connected:
            try:
                await ctx.message.add_reaction('🎵')
            except Exception:
                pass
            return await self.ensure_voice(ctx)

        try:
            if player.is_connected:
                return await ctx.message.reply(
                    content='Im already connected to %s!' % ctx.me.voice.channel.mention,
                    mention_author=False
                )
        except AttributeError:
            if ctx.me.voice:
                return await ctx.message.reply(
                    content='Im already connected to %s!' % ctx.me.voice.channel.mention,
                    mention_author=False
                )

        await ctx.message.reply(
            content='You need to be connected to a voice channel inorder to use this command!',
            mention_author=False
        )
        ctx.command.reset_cooldown(ctx)

    @commands.command(aliases=['dc', 'leave'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def disconnect(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.message.reply(
                content='I am not connected to any voice channels!',
                mention_author=False)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.message.reply(
                content='Your not connected in the same VC as me!',
                mention_author=False)

        channel = ctx.me.voice.channel
        player.queue.clear()
        await player.reset_equalizer()
        await player.set_volume(100)
        player.repeat = False
        await player.stop()
        await self.connect_to(ctx.guild.id, None)

        await ctx.message.reply(
            content='Successfully disconnected from **%s**.' % channel.name,
            mention_author=False)

    @commands.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if query.lower().startswith('soundcloud'):
            query = f'scsearch:{query.lower().split("soundcloud")[-1]}'

        elif not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.message.reply(
                content='I could not find any **videos/songs** using your search query.',
                mention_author=False)

        embed = discord.Embed(color=discord.Color.red())
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)

            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command(aliases=['sc'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def soundcloud(self, ctx, *, query: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'scsearch:{query}'

        results = await player.node.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.message.reply(
                content='I could not find any **songs** using your search query.',
                mention_author=False)

        embed = discord.Embed(color=discord.Color.red())
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
        else:
            track = results['tracks'][0]
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)

            player.add(requester=ctx.author.id, track=track)

        if not player.is_playing:
            await player.play()

        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def queue(self, ctx, page: str = '1'):
        try:
            page = int(page)
        except ValueError:
            return await ctx.send('The page must actually be a number!')

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        queue = player.queue

        if not queue and player.is_playing:
            queue.insert(0, player.current)

        if not queue:
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        if player.queue[0] != player.current:
            queue.insert(0, player.current)

        embed = discord.Embed(title='Queue ({}/{})'.format(page, (len(queue) // 10) + 1), colour=discord.Colour.red())
        try:
            embed.description = '\n'.join(
                f'`{(i + 1)}.` [{v.title}]({v.uri})' for i, v in enumerate(queue[((page * 10) - 10):(page * 10)]))
        except IndexError:
            return await ctx.send('This page number cannot be found!')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True, aliases=['looping'])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def loop(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.repeat:
            return await ctx.message.reply(
                content='Looping is currently **disabled** for this track.',
                mention_author=False
            )
        await ctx.message.reply(
            content='Looping is currently **enabled** for this track.',
            mention_author=False
        )

    @loop.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def enable(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if player.repeat:
            return await ctx.message.reply(
                content='This track is already being looped!',
                mention_author=False
            )
        player.repeat = True

        try:
            await ctx.message.add_reaction('\U0001f501')
        except Exception:
            pass
        await ctx.message.reply(
            content='Looping has been **enabled** for this track.',
            mention_author=False
        )

    @loop.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def disable(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.repeat:
            return await ctx.message.reply(
                content='This track isn\'t currently looping.',
                mention_author=False
            )
        player.repeat = False

        try:
            await ctx.message.add_reaction('\U0001f502')
        except Exception:
            pass
        await ctx.message.reply(
            content='Looping has been **disabled** for this track.',
            mention_author=False
        )

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def shuffle(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.queue:
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        queue = player.queue
        random.shuffle(queue)
        player.queue = queue

        await ctx.message.reply(
            content='Shuffled the queue for you.',
            mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def skip(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        await player.skip()

        await ctx.message.reply(
            content='Skipped the current track being played!',
            mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        if not player.paused:
            await player.set_pause(True)
            await ctx.message.add_reaction('⏸️')
            await ctx.message.reply(
                content='Paused the current track.',
                mention_author=False)
        else:
            await ctx.send('This track has already been paused.')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def unpause(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        if player.paused:
            await player.set_pause(False)
            await ctx.message.add_reaction('⏯️')
            await ctx.message.reply(
                content='Resuming the current track!',
                mention_author=False)
        else:
            await ctx.message.reply(
                content='This track hasn\'t been paused.',
                mention_author=False)

    @commands.group(aliases=['vol'], invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def volume(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        return await ctx.send('The current volume is set at **%s**' % int(player.volume / 10))

    @volume.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def set(self, ctx, new_volume: str):

        try:
            volume = int(new_volume)
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='Make sure the new volume is actually a number',
                mention_author=False)

        if volume not in range(0, 101):
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='Volume must be within the range of **0 - 100**',
                mention_author=False)

        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        await player.set_volume(volume * 10)
        try:
            await ctx.message.add_reaction('📶')
        except Exception:
            pass

        await ctx.message.reply(
            content='Set the volume to **%s**.' % volume,
            mention_author=False)

    @volume.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reset(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        if player.volume == 100:
            return await ctx.message.reply(
                content='Volume is already set the default level!',
                mention_author=False)

        await player.set_volume(100)
        await ctx.message.reply(
            content='Volume has been set as normal again.',
            mention_author=False)

    @commands.command(name="time", aliases=["np", "song", "current", "nowplaying"])
    async def _time(self, ctx):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if player.is_playing:
            # Get Current Timestamp player.current
            current_song_position = player.position
            current_song_position_in_min = self.convert_to_min_and_seconds(current_song_position)
            # Get Full Song Length From Memory
            song_name = player.current.title
            song_link = player.current.uri
            song_duration = player.current.duration
            song_duration_in_min = self.convert_to_min_and_seconds(song_duration)

            ratio_of_times = (current_song_position / song_duration) * 100
            now_playing_cursor = ""
            ratio_of_times_in_range = ratio_of_times // 5
            # Make The Cursor
            for i in range(20):
                if i == ratio_of_times_in_range:
                    now_playing_cursor += "🔘"
                else:
                    now_playing_cursor += "▬"
            embed = discord.Embed(
                title=song_name,
                color=discord.Colour.red(),
                url=song_link,
                description=f'{now_playing_cursor}\t{current_song_position_in_min} / {song_duration_in_min}')
            await ctx.send(embed=embed)
        else:
            await ctx.message.reply(
                content='Nothing is currently playing!',
                mention_author=False)

    """ FILTERS """

    @commands.command(help='Adds a filter to your tracks.', aliases=['filters'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def filter(self, ctx, *, _filter: str = None):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not _filter:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title='List of filters',
                description='It may take a few seconds for the filters to be applied to your tracks.\n\nTo apply a filter use `-Filter [FILTER-NAME]`. To remove a filter use\n`-Filter Remove` or re-use the same command as before.',
                timestamp=ctx.message.created_at
            )

            current_eq = player.fetch('filter')

            if not current_eq:
                embed.set_footer(text='No filters added')
            else:
                embed.set_footer(text='Currently using %s filter' % current_eq.title())

            embed.set_thumbnail(url=self.bot.user.avatar)
            embed.add_field(name='Filters:', value="""\
Flat⠀⠀⠀⠀Boost⠀⠀⠀⠀Metal⠀⠀⠀⠀Piano
Bassboost⠀⠀⠀⠀Random
            """)

            return await ctx.send(embed=embed)

        _filter = _filter.lower()

        if _filter in ['remove', 'r']:
            current_eq = player.fetch('filter')

            if not current_eq:
                return await ctx.send('There are currently no filters playing on your tracks!')

            await player.reset_equalizer()
            return await ctx.send('Removed filter **%s** from your tracks!' % current_eq.title())

        if _filter == 'random':
            embed = discord.Embed(title='The Random Filter', colour=discord.Colour.red())
            raw_filter = await self.random_filter(random.choice([True, False, True, False, True, True]))

            embed.add_field(name='Filter:', value='```\n{}\n```'.format(raw_filter))
            embed.description = 'If you like this filter join our [Support Server](https://discord.gg/Q5mFhUM) and suggest it our community!'
            await player.set_gains(*raw_filter)
            player.store('filter', _filter)
            return await ctx.send(embed=embed)

        if _filter not in list(self.filter_maps.keys()):
            return await ctx.send('This filter cannot be found!')

        current_eq = player.fetch('filter')

        if not current_eq:
            await player.set_gains(*self.filter_maps.get(_filter))
            player.store('filter', _filter)
            return await ctx.send('Added the **%s** filter to your tracks.' % _filter.title())

        if current_eq == _filter:
            await player.reset_equalizer()
            player.delete('filter')
            return await ctx.send('Removed the filter from the tracks.')

        if current_eq != _filter:
            await player.set_gains(*self.filter_maps.get(_filter))
            player.store('filter', _filter)
            return await ctx.send('Swapped the **%s** filter with **%s**.' % (current_eq.title(), _filter.title()))

    @commands.command(aliases=['lyric'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lyrics(self, ctx, *, song: str = None):
        embed = discord.Embed(colour=discord.Colour.red())

        if not song:
            player = self.bot.lavalink.player_manager.get(ctx.guild.id)
            if not player:
                return await ctx.send('I am not connected to any voice channels!')
            if not player.is_connected or not player.is_playing:
                return await ctx.send('I am not playing anything!')
            embed.title = player.current.title
            embed.url = player.current.uri
            request = await self.session.get(
                requote_uri('https://some-random-api.ml/lyrics?title=%s' % player.current.title))
            try:
                json = await request.json()
            except Exception:
                embed.description = 'Sorry I couldn\'t find that song\'s lyrics'
                return await ctx.send(embed=embed)
            if json.get('error'):
                embed.description = 'Sorry I couldn\'t find that song\'s lyrics'
                return await ctx.send(embed=embed)
            embed.title = json['title']
            lyrics = json['lyrics']

        else:
            request = await self.session.get(requote_uri('https://some-random-api.ml/lyrics?title=%s' % song))
            try:
                json = await request.json()
            except Exception:
                embed.description = 'Sorry I couldn\'t find that song\'s lyrics'
                return await ctx.send(embed=embed)
            if json.get('error'):
                embed.description = 'Sorry I couldn\'t find that song\'s lyrics'
                return await ctx.send(embed=embed)
            embed.title = json['title']
            lyrics = json['lyrics']

        if len(lyrics) >= 2048:
            with BytesIO() as b:
                b.write(bytes(
                    ('Song:\n{!r} - {}\n\nLyrics:\n'.format(json['title'], json['author']) + lyrics).encode('utf-8')))
                b.seek(0)
                return await ctx.send(
                    content='Woops! These lyrics were abit large, but don\'t worry. I have put them in a file for you!',
                    file=discord.File(fp=b, filename='Lyrics.txt'))
        else:
            embed.description = lyrics
            await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def seek(self, ctx, *, time: str):
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(
                content='I am currently not playing anything!',
                mention_author=False)

        try:
            seconds = to_seconds(time, strict=False)
        except Exception:
            return await ctx.send(
                'Failed to parse the time, please use a valid format! And make sure it is not in negatives.')
        as_milli = seconds * 1000

        if as_milli > player.current.duration:
            return await ctx.send('This time duration is larger than the song duration!')

        await player.seek(as_milli)
        return await ctx.message.reply(
            content='Moved to postion **%s** of the track!' % await self.pretty_convert(int(seconds)),
            mention_author=False
        )


def setup(bot):
    bot.add_cog(Music(bot))
