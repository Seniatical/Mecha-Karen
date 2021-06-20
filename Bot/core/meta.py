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

        """ LOAD COGS """

        ## For the meta we just wanna load the `.ipc` cog + `error handler`
        ## Due to the errors being spammed! - No commands ofc just for dashboard tests on my PC
        self.load_extension('src.passive.dashboard')
        self.load_extension('src.passive.handler')

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

    @staticmethod
    async def on_ipc_error(endpoint, error):
        raise Exception('Error from %s' % endpoint) from error

    def run(self):
        try:
            reconnect = env('RECONNECT') or False
            if env('IS_MAIN'):
                token = env('DISCORD_BOT_TOKEN')
            else:
                token = env('ALT_TOKEN')

            super().run(token, reconnect=reconnect)
        except discord.errors.LoginFailure:
            return 'Failed to run Mecha Karen!\nDue to Incorrect Credentials...'
