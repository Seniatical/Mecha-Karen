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

import datetime, asyncio, os, json, discord, version, subprocess, sys, Helpers, traceback, json

from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from time import time
from pathlib import Path
from Utils.main import *
from Utils import UD, __logging__
from Utils.help import PING, IMPORTED
from Utils import db, events
from typing import *
from Utils import ratelimiter, parse_error
from Helpers import cache
from IPC import AsyncAppClient

class DATA:
    cache_limit = 500
    concurrent = False
    CACHE = {}
    CACHE_ = tuple(Utils.main.PRELOADED().cache)
    ## Config cache & logging cache
    IMPORTED = globals()
    TOKEN = Utils.customs.READ_ENV('./Utils/Sensitive/LOGINS.env').give_obj('TOKEN')
        
PATH = Path(__file__).parents
EXE = PATH[0]
stringed_exe = str(EXE)

table = client['Bot']
column = table['Guilds']

os.chdir(os.path.dirname(os.path.realpath(__file__)))
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SECONDARY_DIR = '{}\\Utils'.format(CURRENT_DIR)

PERM_COGS = (
    "cogs.Error Handler",
    "cogs.Loadup",
    ## Removed the R&R cog
    "cogs.Help",
    "cogs.Join_Events",
)
        
facts = ('Your server is seen in the support server once you add me!',
         'I automatically report unknown bugs!', 'I am fully tunable!',
         'I was made for fun!', 'I am still expanding with new features',
         'You can contribute to Karen by opening a pull request on the repo',
         'Show me an error code in the support server for a special role!',
         'My Code was lost 10 times before! This is why you may loose your data from time to time.')

def get_prefix(bot, message):
    if isinstance(message.channel, discord.DMChannel):
        return
    res = bot.cache.find('prefix', message.guild.id)
    if not res:
        data = {'_id': message.guild.id, 'prefix': '-', 'Disabled': [], 'StarChannel': int(), 'StarCount': 0}
        column.insert_one(data)
        prefix = '-'
    else:
        prefix = res['prefix']
    return commands.when_mentioned_or(prefix)(bot, message)

class Mecha_Karen(commands.AutoShardedBot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents=discord.Intents(
            guilds=True,
            members=True,
            bans=True,
            emojis=True,
            voice_states=True,
            presences=True,
            messages=True,
            guild_messages=True,
            reactions=True,
        ),

        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            allowed_mentions=allowed_mentions,
            intents=intents,
            description='I am Mecha Karen. An open sourced bot inspiring others!',
            help_command=None,
            owner_id=475357293949485076,
            heartbeat_timeout=200.0,
            help_attrs=dict(hidden=False),
            guild_ready_timeout=5.0,
            assume_unsync_clock=False ''' <---
                                        Dont Bother Adding this.
                                        Your Code will slowly erode if you dont know much about syncing,
                                        If your adding this its recommended you sync it with :
                                            "Google’s NTP server"
                                        '''
        )
        self.launch_time = datetime.datetime.utcnow()
        self.version = version.__version__
        self.logging = Utils.main.__logging__
        
        self.client = client
        black = self.client['Blacklisted']
        self.blacklistedusers = black['Users']
        self.blacklistedguilds = black['Guilds']
        
        self.CLOSE_CONNECTION = Utils.main.CLOSE_CURRENT_SOCKET_CONNECTION(True)
        self.threads = main.THREADS()
        self.alpha = True
        self._str = main.cls(main.conv_to_work(self.threads))
        self.connected = True if self.threads is not None and not self.client == False else False
        self.__xxx__ = True if self.threads < 4 and self.logging.grab_logs('threads').errors is not None
        self.ratelimter = ratelimiter.ratelimiter()
        
        self.ratelimiter.start()
        ## Mongo management from the client class
        ## Uses Mongo features normally whilst allowing queueing
        ## Prevents spam and manages the capped collection
        ## Handles all the triggers from the Mongo server and the dashboard
        
        self.server = AsyncAppClient(*self.logging.GET_ADDR)
        
        self.server.start()
        
        with open('../logs/json/cache.json', 'r') as f:
            data = json.load(f)
        self.cache = cache.Cache(data)
        
        with open('./config.json', 'r') as f:
            data = json.load(f)
        
        self.logging.ext.networks(data)
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{filename[:-3]}')
                except Exception as error:
                    if type(error) == ImportError:
                        error = parse_error(error)
                        os.system('python -m pip install %s' % error.__package__)
                        continue
                    traceback.print_exception(etype=type(error), value=error, tb=error.__traceback__)
        
        @self.before_invoke
        async def before_any_command(ctx):
            data = column.find_one({'_id': ctx.guild.id})
            blacklisted = self.blacklistedusers.find_one({'_id': ctx.author.id})

            if blacklisted:
                raise commands.errors.Blacklisted('You have been blacklisted from MechaKaren...')
            
            disabled = data['Disabled']
            if ctx.command.name.lower() in disabled:
                raise commands.errors.CommandHasBeenDisabled
            
            ctx.timer = time()
            try:
                await ctx.trigger_typing()
            except discord.errors.Forbidden:
                pass
        
    async def on_connect(self) -> None:
        if self.__xxx__:
            sys.exit('Error via booting up multi threading')
        if not self.connected:
            sys.exit('Threads failed to setup...')
        self.logging.environ['CLIENT_KEY'] = client.connection()
        
        self.logging.ROOT_CONNECTION = 'None' if not self.logging.status is self.logging.statuses.Connected
        
        print('Bot Connected')
        
    async def on_disconnect(self) -> None:
        '''
        :Automatic handling of __logging__ dual instancing:
        
        :Asynced: it so it doesnt stop the bot whilst waiting
        '''
        if self.logging.instances > 1:
            __logging__.handle_instances(self.logging)
            import warnings ## we dont need it by default :p
            
            warnings.warn('Attempting to fix dual instancing of __main__.py', category=DeprecationWarning)
            
            cond = await __logging__.wait_until_completion(__logging__.queue[-1])  ## latest addition of tasks
            
            if str(cond.status) != 'Green':
                warnings.warn('Failed to complete issue. Currently sitting at: {}'.format(str(cond.status)))
        
    async def on_message_delete(self, message:discord.Message) -> [Any]:
        if message.author.bot:
            pass
        else:
            Utils.main.handle_snipe(message)
            
        op = __logging__.cache('update', {message.id: None}, 'store', 'deleted')
        
        if not __logging__.operation(op):
            if __logging__.fetch_completed_operation(op) is not None and __logging__.completed(op):
                return
        await __logging__.until_completed(op)   ## Stops any other operations from running e.g. stops the module from being flooded
                
    async def on_guild_remove(self, guild:discord.Guild):
        column.delete_one({'_id': guild.id})
        warns = table['Warns']
        warns.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        tags = table['Tags']
        tags.delete_many({'_id': {'$regex': '^{}'.format(guild.id)}})
        ## No guarantee that they are going to re-add the bot so might as well delete their data
        ## Also saves up memory
            
    async def on_guild_join(self, guild:discord.Guild):
        x = self.ratelimiter.action(guild.id, '+=', 1, 
            statement='''
            if self.ratelimiter.get_logs(guild.id) >= 5:
                self.ratelimter.destroy(guild.id):
                    return await guild.leave()
                      '''
            ## Uses an env parsed by ast to complete this action
            ## Bonuses as it allows me to use local variables as well global variables between both files
        )
        if x is not None and str(x) is not 'Failed':
            return
        
        main.add_to_stack(guild.id)
        
        res = self.blacklistedguilds.find_one({'_id': guild.id})
        
        if res is not None:
            try:
                await guild.owner.send(Helpers.Blacklisted.Messages['server'])
            except discord.errors.Forbidden:
                pass
            return await guild.leave()

        channel = self.get_channel(753311458171027547)
        await channel.send('> <@!475357293949485076> You Retard.\n> I have made it into another server!\n\n> Guild Name: **{}**'.format(guild.name))
        
    async def on_message(self, msg:discord.Message):
        if isinstance(msg.channel, discord.DMChannel):
            if msg.author.bot and self.blacklistedusers.find_one({'_id': ctx.author.id}) is not None:
                return
            '''
            Stops blacklisted uses from accessing any features of the bot.
            '''
            
            embed = discord.Embed(
                title='Hello {}!'.format(msg.author),
                colour=discord.Colour.from_rgb(random.randrange(255), random.randrange(255), random.randrange(255)),
                timestamp=datetime.datetime.utcnow(),
                description='I see you are interested! \👀'
            )
            
            embed.add_field(name='Support Server?', value='**[My Support Server!](https://discord.gg/Q5mFhUM)**')
            embed.add_field(name='Bot Invite?', value='**[My Very Own Invite!](https://discord.com/api/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)**', inline=False)
            embed.add_field(name='Source Code?', value='**[My Source Code!](https://github.com/Seniatical/Mecha-Karen-Source-Code)**', inline=False)
            embed.add_field(name='Fun Fact!', value=random.choice(facts))
            embed.set_thumbnail(url=self.user.avatar_url)
            embed.set_footer(
                text='Bot created by _-*™#1234',
                icon_url='https://i.imgur.com/jSzSeva.jpeg'
            )
            
            await msg.channel.send(embed=embed)
            
        try:
            if '👀' in msg.content:
                if msg.author.bot:
                    pass
                else:
                    channel = discord.utils.get(msg.guild.channels, name=channels['tracking'])
                    amount = 0
                    if msg.channel.name == '👀tracking':
                        pass
                    else:
                        await msg.add_reaction('👀')
                        x = list(msg.content)
                        for letter in x:
                            if '👀' in letter:
                                amount += 1
                        if amount > 1 and amount < 5:
                            await channel.send('**{}** ({}) has sent \👀 {} times in `{}`.'.format(msg.author.name, msg.author.id, amount, msg.channel.name))
                        elif amount > 5:
                            await msg.delete()
                            await msg.channel.send('That is spamming.')
                        else:
                            await channel.send('**{}** ({}) has sent \👀 {} time in `{}`.'.format(msg.author.name, msg.author.id, amount, msg.channel.name))
                            
            if msg.content == '<@!740514706858442792>':
                await msg.channel.send('> Hello {}!\n> \n> I am Mecha Karen and thank you for inviting me. My prefix for the server is **`{}`** .'.format(msg.author.mention, get_prefix(bot, msg)[-1]))
            await self.process_commands(message=msg)
        except (discord.errors.Forbidden, discord.errors.HTTPException, AttributeError):    ## Only problems here
            pass
        
    @staticmethod
    async def on_socket_raw_receive(message):
        _recieve = self.logging.call('./Logs/recieved.log')
        
        @_recieve.update(cls=__logging__.binary)
        async def clog(message_):
            x = await __logging__.encode(message)
            if not x:
                return
            await message_.repel(x)
            return message_.rebound(x if type(x) == __logging__.CLS, indentify=True).result_as_bytes
        
        @_recieve.result
        async def log_result(_bytes):
            if not type(_bytes) == bytes:
                return False
            if not hasattr(_bytes, 'clog'):
                return False
            
            self.logging.log('event', 'recieved.log', _bytes.clog.raw, format='[{data}] [{time}] -> {data}')
        
    def run(self):
        try:
            event_ = self.logging.start()
            event_.cache = self.logging.loads('../logs')
            if not event_.cache:
                raise Exception('Failed to load logging cache')
            cxn = event_.connect('thread')
            cxn.start()
            __import__('time').sleep(cxn.delay)
            cxn.run()
            
            super().run(DATA.TOKEN, reconnect=True)
        except discord.errors.LoginFailure:
            return 'Failed to run Mecha Karen!\nDue to Incorrect Credentials...'
    
## You have sucessfully made it to the end!
## Ping -> random.randint(1, 10) is good
## Goodbye

if __name__ == '__main__':
    import sys
    from shutil import Error
    
    raise Error('Run __main__.py not bot.py')
    sys.exit(0)
