# !/usr/bin/python

"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0

A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.

Licensed works, modifications, and larger works may be distributed under different terms and without source code.

FULL LICENSE CAN BE FOUND AT:
    https://www.apache.org/licenses/LICENSE-2.0.html

Any violation to the license, will result in moderate action
You are legally required to mention (original author, license, source and any changes made)
"""
import re
import discord
import lavalink
from discord.ext import commands

url_rx = re.compile(r'https?://(?:www\.)?.+')

def convert(time: int):
    mins = time // 60
    time %= 60
    return '%d:%d' % (mins, time)

class LAVALINK(Exception):
    pass

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        if not hasattr(bot, 'lavalink'):
            bot.lavalink = lavalink.Client(740514706858442792)
            bot.lavalink.add_node('your server ip', you_know_some_port, 'youshallnopass', 'region', 'other stuff')
            bot.add_listener(bot.lavalink.voice_update_handler, 'on_socket_response')

        lavalink.add_event_hook(self.track_hook)

    def cog_unload(self) -> None:
        self.bot.lavalink._event_hooks.clear()

    async def cog_before_invoke(self, ctx) -> bool:
        guild_check = ctx.guild is not None
        if guild_check:
            await self.ensure_voice(ctx)
        return guild_check

    async def cog_command_error(self, ctx, error) -> None:
        if isinstance(error, commands.errors.CommandInvokeError):
            pass

    async def ensure_voice(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
        should_connect = ctx.command.name in ('play', 'join')

        if not ctx.author.voice or not ctx.author.voice.channel:
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Must be in a voice channel to use this command!',
                colour=discord.Colour.red()
            ), mention_author=False)
            raise commands.errors.CommandInvokeError

        if not player.is_connected:
            if not should_connect:
                ctx.command.reset_cooldown(ctx)
                await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> I am not connected to any **VC**.',
                    colour=discord.Colour.red()
                ).set_footer(
                    text='If this is a mistake manually kick the bot.',
                    icon_url=self.bot.user.avatar_url), mention_author=False)
                raise commands.errors.CommandInvokeError

        if player.is_connected:
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(embed=discord.Embed(
               description='<a:nope:787764352387776523> I am already connected to a **VC** in your server.',
               colour=discord.Colour.red()
            ).set_footer(
               text='If this is a mistake manually kick the bot.',
               icon_url=self.bot.user.avatar_url), mention_author=False)
            raise commands.errors.CommandInvokeError

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                ctx.command.reset_cooldown(ctx)
                await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> I need `CONNECT` and `SPEAK` permissions.',
                    colour=discord.Colour.red()
                ), mention_author=False)
                raise commands.errors.CommandInvokeError

            player.store('channel', ctx.channel.id)
            await self.connect_to(ctx.guild.id, str(ctx.author.voice.channel.id))
        else:
            if int(player.channel_id) != ctx.author.voice.channel.id:
                ctx.command.reset_cooldown(ctx)
                await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> You need to be in the same VC as me!',
                    colour=discord.Colour.red()
                ), mention_author=False)
                raise commands.errors.CommandInvokeError

    async def track_hook(self, event) -> None:
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)

    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)

    @commands.command()
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def join(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if ctx.author.voice:
            await ctx.message.add_reaction('🎵')
            return await ctx.send(embed=discord.Embed(
                description='🎶 **Mecha Karen** has joined **{}**'.format(ctx.author.voice.channel),
                colour=discord.Colour.green()
            ))
        if player.is_connected:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> I am already connected to a **VC**.',
                colour=discord.Colour.red()
            ))
        await ctx.send(embed=discord.Embed(
            description='<a:nope:787764352387776523> You need to be connected to **VC**!',
            colour=discord.Colour.red()
        ))
        ctx.command.reset_cooldown(ctx)

    @commands.command(aliases=['dc'])
    @commands.cooldown(1, 5, commands.BucketType.guild)
    async def disconnect(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> I am not connected to any VC!',
                colour=discord.Colour.red()
            ), mention_author=False)

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Your not **connected** to my voice channel!',
                colour=discord.Colour.red()
            ), mention_author=False)
        player.queue.clear()
        await player.stop()
        await self.connect_to(ctx.guild.id, None)
        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Successfully disconnect from VC.',
            colour=discord.Colour.green()
        ), mention_author=False)

    @commands.command(aliases=['p'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def play(self, ctx, *, query: str = None) -> None:
        if not query:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Need to give a song to play!',
                colour=discord.Colour.red()
            ), mention_author=False)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        query = query.strip('<>')
        if not url_rx.match(query):
            query = f'ytsearch:{query}'
        results = await player.node.get_tracks(query)
        if not results or not results['tracks']:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> No **videos/songs** found!',
                colour=discord.Colour.red()
            ), mention_author=False)

        embed = discord.Embed(color=discord.Color.red(), timestamp=ctx.message.created_at)
        if results['loadType'] == 'PLAYLIST_LOADED':
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)

            embed.title = 'Playlist Enqueued!'
            embed.description = f'{results["playlistInfo"]["name"]} - {len(tracks)} tracks'
            embed.set_footer(icon_url=ctx.author.avatar_url, text='Requested by {}'.format(ctx.author))
        else:
            track = results['tracks'][0]
            embed.description = f'[{track["info"]["title"]}]({track["info"]["uri"]})'
            embed.set_footer(icon_url=ctx.author.avatar_url, text='Requested by {}'.format(ctx.author))
            track = lavalink.models.AudioTrack(track, ctx.author.id, recommended=True)
            player.add(requester=ctx.author.id, track=track)

        await ctx.message.reply(embed=embed, mention_author=False)

        if not player.is_playing:
            await player.play()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def queue(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.queue:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> I am not playing anything!',
                colour=discord.Colour.red()
            ), mention_author=False)
        embed = discord.Embed(title='Queue - ({})'.format(len(player.queue)),
                              colour=discord.Colour.red(),
                              timestamp=ctx.message.created_at)
        embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
        embed.set_footer(text='Requested by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.description='\n'.join(
            ['`{}.` [{}]({})'.format(
                player.queue.index(i)+1, i.title, i.uri) for i in player.queue])
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def loop(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.repeat:
            player.repeat = True
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Looping enabled!',
                colour=discord.Colour.green()
            ), mention_author=False)
            await ctx.message.add_reaction('🔁')
        else:
            player.repeat = False
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Looping disabled!',
                colour=discord.Colour.green()
            ), mention_author=False)
            await ctx.message.add_reaction('🔂')

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def shuffle(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        player.shuffle = True
        if not player.queue:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523>'
            ), mention_author=False)
        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Shuffled the queue!',
            colour=discord.Colour.green()
        ), mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def skip(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> There is nothing to skip!',
                colour=discord.Colour.red()
            ), mention_author=False)
        await player.skip()
        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Skipped the current track!',
            colour=discord.Colour.green()
        ), mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pause(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        if not player.is_playing:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> There is nothing playing!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if not player.paused:
            await player.set_pause(True)
            await ctx.message.add_reaction('⏸️')
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Paused the track.',
                colour=discord.Colour.green()
            ), mention_author=False)
        else:
            await player.set_pause(False)
            await ctx.message.add_reaction('⏯️')
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Resuming the track.',
                colour=discord.Colour.green()
            ), mention_author=False)

    @commands.command(aliases=['sv'])
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def set_volume(self, ctx, vol: str = '15') -> None:
        try:
            vol = int(vol)
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Volume must a number!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if vol not in range(0, 101):
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Volume can only be in the range of **0 - 100**',
                colour=discord.Colour.red()
            ), mention_author=False)
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.set_volume(vol*10)
        await ctx.message.add_reaction('📶')
        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Volume set at **{}**.'.format(vol),
            colour=discord.Colour.green()
        ), mention_author=False)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def equalizer(self, ctx, band: str='5', gain: str='5') -> None:
        try:
            band = int(float(band))
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> `BAND` change must a number!',
                colour=discord.Colour.red()
            ), mention_author=False)
        try:
            gain = float(int(float(gain)))
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> `GAIN` change must a number!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if band > 14 or band < 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> **Band** must be in the range of **0 - 14**.',
                colour=discord.Colour.red()
            ))
        if gain > 1.00 or gain < -0.25:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> **Gain** must be in the range of **-0.25 - 1**.',
                colour=discord.Colour.red()
            ))
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.set_gain(band, gain)
        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Changed the equalizer! ({}, {})'.format(band, gain),
            colour=discord.Colour.green()
        ), mention_author=False)

    @commands.command(aliases=['re'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def reset_equalizer(self, ctx) -> None:
        player = self.bot.lavalink.player_manager.get(ctx.guild.id)
        await player.reset_equalizer()
        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Reset equalizer to default values! (0, 0)',
            colour=discord.Colour.green()
        ))

def setup(bot):
    bot.add_cog(Music(bot))
