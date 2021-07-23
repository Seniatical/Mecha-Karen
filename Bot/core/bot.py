import datetime
from time import time

import aiofiles
import discord
import pymongo
import pymongo.errors
from discord.ext import commands, ipc
import aiohttp.web
from utility import (Enviroment, Cache, handler, get_dm_embed, errors, emojis)
from utility.prefix import PrefixHandler
from src.support.join_events import ending

from ._ import extract_
from .logging import *

global env, client, user, table, column, start


def get_tail():
    r""" Get db and env which we don't want loading in the CLI Instantly """

    env = Enviroment('./.env')

    client = pymongo.MongoClient(env('MONGO_DB_URI'))
    super_user = env('MONGO_DB_URI').split(':')[1][2:]

    table = client['Bot']
    column = table['Guilds']
    start = time()

    print('Connected to MongoDB - Account used: `{}`'.format(super_user))

    return env, client, super_user, table, column, start


class MechaKaren(commands.AutoShardedBot):
    def __init__(self):
        global env, client, user, table, column, start

        env, client, user, table, column, start = get_tail()

        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            messages=True,
            guild_messages=True,
            reactions=True,
        ),
        self.prefix = PrefixHandler(column)

        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            allowed_mentions=allowed_mentions,
            description='I am Mecha Karen. An open sourced bot inspiring others!',
            intents=intents[0],
            help_command=None,
            owner_ids=[475357293949485076, 491630879085559808],
        )
        self.launch_time = datetime.datetime.utcnow()
        self.owner = self.owner_id
        self.env = env

        self.ipc = ipc.Server(self, secret_key=env('IPC_SECRET_KEY'), host=env('IPC_HOST'))
        self.client = client
        self.blacklisted = client['Blacklisted']
        self.blacklistedusers = self.blacklisted['Users']
        self.blacklistedguilds = self.blacklisted['Guilds']
        self.beta_client = handler.MongoDB()

        self.cache = Cache()
        self.session = __import__('aiohttp').ClientSession()

        extract_.session = self.session
        extract_.cache = self.cache
        self.extract_ = extract_

        print('Created Internal Helper Cache - Accessible via `self.cache`')

        self.column = column
        self.table = table

        self.blacklist_cache = {
            'guilds': {},
            'users': {},
        }
        self.guild_logs = None
        self.premium = dict()

        """ LOAD COGS """
        from src import core

        core.load_cogs(self)

        """ LOAD GAMES """
        from core.games import core

        core.load_games(self)

        """ Set up logger """
        self.command_logger = CommandLogger()
        self.event_logger = EventLogger()
        setup_discord_logger()

        @self.before_invoke
        async def before_any_command(ctx):
            disabled = self.column.find_one({'_id': ctx.guild.id})

            if self.blacklist_cache['users'].get(ctx.author.id):
                raise errors.Blacklisted

            disabled = disabled['Disabled']
            if ctx.command.name.lower() in disabled:
                raise commands.errors.DisabledCommand

            ctx.timer = time()
            try:
                await ctx.trigger_typing()
            except discord.errors.Forbidden:
                pass

    class IPCError(Exception):
        r""" Raised when an error occurs from the IPC """
        pass

    def __call__(self):
        return 'My Name is Mecha Karen!'

    @property
    async def version(self):
        async with aiofiles.open('./core/version.py', 'r') as f:
            data = await f.read()
        return data.split('=')[-1].strip()

    async def on_connect(self):
        print('Bot Connected to discord - Took {} Seconds after starting'.format(time() - start))

        # Manual startup for IPC

        self.ipc._server = aiohttp.web.Application()
        self.ipc._server.router.add_route("GET", "/", self.ipc.handle_accept)

        if self.ipc.do_multicast:
            self._multicast_server = aiohttp.web.Application()
            self._multicast_server.router.add_route("GET", "/", self.ipc.handle_multicast)

        async def handle_soundboard_response(request: aiohttp.web.Request):
            url_data = request.query
            file = url_data.get('file')

            if not file:
                return aiohttp.web.Response(
                    body="{'error': 400, 'message': 'Invalid URL Parameters'}",
                    status=400, content_type='application/json'
                )

            try:
                response = aiohttp.web.FileResponse(path='./storage/soundboard/{}'.format(file))
            except FileNotFoundError:
                return aiohttp.web.Response(
                    body="{'error': 400, 'message': 'Cannot Locate Specified File'}",
                    status=400, content_type='application/json'
                )

            return response

        self.ipc._server.router.add_route(
            'GET', '/lavalink', handle_soundboard_response
        )
        print('[ + ] Added lavalink route to IPC')

        # Run the server
        runner = aiohttp.web.AppRunner(self.ipc._server)
        await runner.setup()

        site = aiohttp.web.TCPSite(runner, self.ipc.host, self.ipc.port)
        await site.start()

        self.dispatch('ipc_ready')

    async def on_ipc_ready(self):
        self.event_logger.debug('IPC is now running', 'IPC_READY')
        print("[ + ] IPC Server is now running!")

    async def on_ipc_error(self, endpoint, error):
        self.event_logger.critical('Error from endpoint "%s"' % endpoint, name=endpoint)
        raise self.IPCError('Uncaught error from "%s"' % endpoint) from error

    async def on_guild_remove(self, guild: discord.Guild):

        column.delete_one({'_id': guild.id})
        warns = table['Warns']
        warns.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        tags = table['Tags']
        tags.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        giveaways = client['Giveaways']['codes']
        giveaways.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        suggestions = table['Suggestions']
        suggestions.delete_one({'_id': guild.id})
        # Free up DB space

        if not self.guild_logs:
            self.guild_logs = self.get_channel(787372543240568932)
        embed = discord.Embed(title='I have left a guild', colour=discord.Colour.red(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Name', value=guild.name)
        embed.add_field(name='Member Count', value=guild.member_count, inline=False)
        embed.set_author(name=guild.owner, icon_url=guild.owner.avatar)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(icon_url=self.user.avatar, text='Left At ')

        await self.guild_logs.send(embed=embed)

    async def on_guild_join(self, guild: discord.Guild):

        res = self.blacklist_cache['guilds'].get(guild.id)

        if res is not None:
            try:
                await guild.owner.send('It looks like I am blacklisted from this server!')
            except discord.errors.Forbidden:
                pass
            return await guild.leave()

        try:
            column.insert_one({'_id': guild.id, 'prefix': '-', 'Disabled': [], 'StarChannel': int(), 'StarCount': 0})
        except pymongo.errors.DuplicateKeyError:
            return

        channel = guild.system_channel

        if channel:

            embed = discord.Embed(
                title='Thanks for Inviting me!',
                colour=discord.Colour.green(),
                description='You are the **{} {}** server to invite me! {}'.format(len(self.guilds), (await ending(len(self.guilds))),
                                                                                   emojis.KAREN_ADDITIONS_ANIMATED['tada']),
                timestamp=datetime.datetime.utcnow()
            ).set_footer(text='Bot created by {}'.format(self.get_user(self.owner_id)),
                         icon_url=self.get_user(self.owner_id).avatar)
            url = 'https://discord.com/api/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot'
            embed.add_field(name='Useful Links:',
                            value='**[Support Server!](https://discord.gg/Q5mFhUM)** | **[Invite Me!]({})** | **[Source Code!](https://github.com/Seniatical/Mecha-Karen-Source-Code)** | **[Dashboard](https://mechakaren.xyz/)**'.format(
                                url))
            embed.add_field(name='Features:',
                            value='```\n100+ Commands!\nOffer the best NSFW out there!\nFun Commands\nTODO Lists\nMusic\nAnd More!```',
                            inline=False)
            embed.add_field(name='Lets Get Started!',
                            value='To view all my commands run **`-Help`**, I Have 2 prefixes. **`-`** and Mentioning me! You change the default prefix of `-` to anything you like by visiting my dashboard!',
                            inline=False)
            embed.set_thumbnail(url=self.user.avatar)
            try:
                await channel.send(embed=embed)
            except discord.errors.Forbidden:
                pass

        embed = discord.Embed(title='I have joined a guild', colour=discord.Colour.red(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Name', value=guild.name)
        embed.add_field(name='Member Count', value=guild.member_count, inline=False)
        embed.add_field(name='Owner', value=guild.owner)

        if not self.guild_logs:
            self.guild_logs = self.get_channel(787372543240568932)
        await self.guild_logs.send(embed=embed)

    async def on_message(self, message):
        if message.author.bot:
            return

        if not message.guild:
            return await message.author.send(embed=await get_dm_embed(self, message))

        try:
            if '👀' in message.content or 'eyes' in message.content and message.guild.id == 740523643980873789:
                channel = discord.utils.get(message.guild.channels, name='👀tracking')
                amount = 0
                if message.channel.name == '👀tracking':
                    pass
                else:
                    await message.add_reaction('👀')
                    x = list(message.content)
                    for letter in x:
                        if '👀' in letter or 'eyes' in letter:
                            amount += 1
                    if 1 < amount < 5:
                        await channel.send(
                            '**{}** ({}) has sent \👀 {} times in `{}`.'.format(message.author.name, message.author.id,
                                                                                amount, message.channel.name))
                    elif amount > 5:
                        await message.channel.send('That is spamming.')
                    else:
                        await channel.send(
                            '**{}** ({}) has sent \👀 {} time in `{}`.'.format(message.author.name, message.author.id,
                                                                               amount, message.channel.name))
        except discord.errors.Forbidden:
            return

        try:
            prefix = self.prefix.cache.get(message.guild.id)

            if not prefix:
                prefix = '-'
            else:
                prefix = list(prefix)[-1]

            if self.user.mentioned_in(message) and message.mentions[0] == message.content.strip():
                await message.reply(embed=discord.Embed(
                    description='<a:wave:787761464697421835> My Prefix for this Server is `{}`'.format(prefix),
                    colour=discord.Color.red()))
        except discord.errors.Forbidden:
            return

        await self.process_commands(message=message)

    async def on_raw_reaction_add(self, payload):
        try:
            if payload.emoji.name == '👀':
                if payload.member.bot:
                    return
                channel = discord.utils.get(self.get_guild(payload.guild_id).text_channels, name='👀tracking')
                channel_ = self.get_channel(payload.channel_id)
                await channel.send(
                    '**{}** ({}) has reacted with a \👀 in `{}`'.format(payload.member, payload.member.id, channel_))
        except AttributeError:
            pass

    def run(self):
        reconnect = env('RECONNECT') or False
        if env('IS_MAIN'):
            token = env('DISCORD_BOT_TOKEN')
        else:
            token = env('ALT_TOKEN')

        super().run(token, reconnect=reconnect)
