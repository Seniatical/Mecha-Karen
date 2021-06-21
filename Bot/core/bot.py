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

import datetime
from time import time

import aiofiles
import discord
import pymongo
from discord.ext import commands, ipc
from utility import (Enviroment, Cache, handler, get_dm_embed, errors, emojis)
from utility.prefix import PrefixHandler
from src.support.join_events import ending
from . import config

from ._ import extract_

env = Enviroment('./.env')

client = pymongo.MongoClient(env('MONGO_DB_URI'))
super_user = env('MONGO_DB_URI').split(':')[1][2:]

table = client['Bot']
column = table['Guilds']
start = time()

print('Connected to MongoDB - Account used: `{}`'.format(super_user))


class MechaKaren(commands.AutoShardedBot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents = discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            presences=True,
            messages=True,
            guild_messages=True,
            reactions=True,
            integrations=True
        ),
        self.prefix = PrefixHandler(column)

        super().__init__(
            command_prefix=self.prefix,
            case_insensitive=True,
            allowed_mentions=allowed_mentions,
            description='I am Mecha Karen. An open sourced bot inspiring others!',
            intents=intents[0],
            help_command=None,
            owner_id=475357293949485076,
        )
        self.launch_time = datetime.datetime.utcnow()
        self.owner = self.owner_id
        self.env = env

        self.ipc = ipc.Server(self, secret_key='Daftlikeslongsausages', host='0.0.0.0')
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

        """ LOAD COGS """
        from src import core

        core.load_cogs(self)

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

        @self.after_invoke
        async def after_any_command(ctx):
            if await ctx.bot.is_owner(ctx.author):
                ctx.command.reset_cooldown(ctx)

    class IPCError(Exception):
        r""" Raised when an error occurs from the IPC """
        pass

    def __call__(self):
        return 'My Name is Mecha Karen!'

    @property
    async def version(self):
        async with aiofiles.open('./core/version.py', 'r') as f:
            data = await f.read()
        return data.split('=')[-1]

    async def on_connect(self):
        self.ipc.start()
        print('Bot Connected to discord - Took {} Seconds after starting'.format(time() - start))

    @staticmethod
    async def on_ipc_ready():
        print("[ + ] IPC Server is now running!")

    async def on_ipc_error(self, endpoint, error):
        ## Allows me to see both endpoint + error in 1 tb
        raise self.IPCError('Uncaught Error from %s' % endpoint) from error

    async def on_guild_remove(self, guild: discord.Guild):

        column.delete_one({'_id': guild.id})
        warns = table['Warns']
        warns.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        tags = table['Tags']
        tags.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        giveaways = client['Giveaways']['codes']
        giveaways.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})

        if not self.guild_logs:
            self.guild_logs = self.get_channel(787372543240568932)
        embed = discord.Embed(title='I have left a guild', colour=discord.Colour.red(),
                              timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Name', value=guild.name)
        embed.add_field(name='Member Count', value=guild.member_count, inline=False)
        embed.set_author(name=guild.owner, icon_url=guild.owner.avatar)
        embed.set_thumbnail(url=guild.icon)
        embed.set_footer(icon_url=self.user.avatar, text='Left At ')

        if not self.guild_logs:
            self.guild_logs = self.get_channel(787372543240568932)
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
        except Exception:
            return

        channel = guild.system_channel

        if channel:

            embed = discord.Embed(
                title='Thanks for Inviting me!',
                colour=discord.Colour.green(),
                description='You are the **{} {}** server to invite me! {}'.format(len(self.guilds), ending(len(self.guilds)),
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
            if '👀' in message.content or 'eyes' in message.content:
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
            if message.content.lower() == 'mecha karen' or message.content == '<@!740514706858442792>':
                await message.reply(embed=discord.Embed(
                    description='<a:wave:787761464697421835> My Prefix for this Server is `{}`'.format(
                        (self.prefix.cache.get(message.guild.id) or ['-'])[-1]),
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
        try:
            reconnect = env('RECONNECT') or False
            if env('IS_MAIN'):
                token = env('DISCORD_BOT_TOKEN')
            else:
                token = env('ALT_TOKEN')

            super().run(token, reconnect=reconnect)
        except Exception as error:
            raise discord.errors.LoginFailure('Failed to connect to discord') from error
