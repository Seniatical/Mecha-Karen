"""

Discord bot made by Seniatical / _-*™#1234
Created at 5/8/2020
Available under the Apache License 2.0

"
A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.
"

Note:
This bot has an extensive backend network.
I will get around to publishing that soon. Rn its just full of personal info such as server IPs and webhooks

Another thing:
    Dont copy the entirety of this bot and complain it doesnt work,
    It was made for people to learn from and to improve the code behind it,
"""
import datetime, asyncio, os, json, discord, version, subprocess, sys
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from time import time
from pathlib import Path
from Utils.main import *
from Utils.SQL import NEWGUILDTABLE
import mysql.connector
from __future__ import print_function
from mysql.connector import errorcode
from Utils import UD, __logging__

class DATA:
    def __init__(self):
        self.cache_limit = 500
        self.concurrent = False
        self.CACHE = {}
        self.CACHE_ = tuple(Utils.main.PRELOADED().cache)
        self.IMPORTED = (
            'datetime', 'asyncion', 'os',
            'json', 'discord', 'version', 'subprocess',
            'sys', 'time', 'pathlib', 'Utils', 'mysql',
            '__future__'
        )
        self.TOKEN = Utils.customs.READ_ENV('./Utils/Sensitive/LOGINS.env').give_obj('TOKEN')
        
class BASE(Exception):
    pass
        
PATH = Path(__file__).parents
EXE = PATH[0]
stringed_exe = str(EXE)

os.chdir(os.path.dirname(os.path.realpath(__file__)))
CURRENT_DIR = os.path.dirname(os.path.realpath(__file__))
SECONDARY_DIR = '{}\\Utils'.format(CURRENT_DIR)

def PING(file, dir_):
    try:
        try:
            data = open(dir_+'\\'+file)
        except NotADirectoryError:
            raise NotADirectoryError('Directory Given doesnt Exist.')
    except FileNotFoundError:
        raise FileNotFoundError('File Given doesnt Exist.')
        
    lines = data.readlines()
    holder = []
        
    for line in lines:
        response=subprocess.Popen(["ping", "-c", "1", line.strip()],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
        stdout, stderr = response.communicate()
        #print(stdout)
        #print(stderr)

        if (response.returncode == 0):
            status = line.rstrip() + " is Reachable"
        else:
            status = line.rstrip() + " is Not reachable"
        holder.append(status)
    return holder

'''
Moved stuff which was here to:
    ./Helpers/functions.py
'''

def IMPORTED():
    loaded = globals()
    for i in DATA().IMPORTED:
        if i not in loaded:
            raise ImportError('{} isnt loaded.'.format(i.title()))
        continue
    return True

PERM_COGS = (
    "cogs.Error Handler",
    "cogs.Loadup",
    "cogs.R&R,",
    "cogs.Help",
    "cogs.Join_Events",
)

for file in os.listdir('./cogs/mini_helpers'):
    try:
        exec('import %s' % (file))
    except FileNotFoundError:
        raise ImportError('Couldnt Import %s From Mini Helpers -> (cogs/mini_helpers)')

for file in os.listdir('./Helpers'):
    if file == 'Sockets.py':
        try:
            exec('''
                from Helpers.Sockets import get_res
                try:
                    x = get_res(ping('socks.txt', '.\\Utils\\sockets'))
                except socket.error as failure:
                    raise failure
                if x == True:
                    return
                raise Warning('Results from helper func >> Sockets/get_res returned False\nRerun to prevent any long term errors.')
            ''')
        except SyntaxError as error:
            raise error
    try:
        exec('import %s' % (file))
    except FileNotFoundError:
        print('Couldnt Import %s From Helpers.')
        
facts = ('Your server is seen in the support server once you add me!',
         'I automatically report unknown bugs!', 'I am fully tunable!',
         'I was made for fun!', 'I am still expanding with new features',
         'You can contribute to Karen by opening a pull request on the repo',
         'Show me an error code in the support server for a special role!',
         'My Code was lost 10 times before! This is why you may loose your data from time to time.',
         'I offer no premium so all commands can be used by anybody, anywhere!')

class NotValid(Exception):
    pass

def stock():
    return __file__.globals()

exec('x = True')

class Mecha_Karen(commands.AutoShardedBot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents = discord.Intents.all()
        
        def is_support():
            async def predicate(ctx):
                if ctx.guild != Utils.TABLES.CLASS_BUILDS().support_server:
                    raise NotValid('This server isnt the support server!')
                return True
            commands.check(predicate)
        
        super().__init__(
            command_prefix=PREFIX,case_insensitive=True,
            allowed_mentions=allowed_mentions,intents=intents,
            description='I am Mecha Karen. An open sourced bot inspiring others!',
            help_command=None,owner_id=475357293949485076,heartbeat_timeout=200.0,
            help_attrs=dict(hidden=False),guild_ready_timeout=5.0
            assume_unsync_clock=False ''' <---
                                        Dont Bother Adding this.
                                        Your Code will slowly erode if you dont know much about syncing,
                                        If your adding this its recommended you sync it with :
                                            "Google’s NTP server"
                                        '''
        )
        self.launch_time = datetime.datetime.utcnow()
        self.version = version.__version__
        self.user = Utils.main.USERNAME
        self.password = Utils.main.PASSWORD
        self.logging = Utils.main.__logging__
        self.MySQL = mysql.connector.connect(
                     host="127.0.0.1",
                     user=self.user,
                     password=self.password,
                     database='Mecha_Karen',
                     raise_on_warnings=True
        )
        self.cursor = self.MySQL.cursor()
        self.TABLES = self.cursor.execute("SHOW TABLES")
        self.STEPRISE = Utils.main.GETBOTSTEP(self).launch(True).giveres()
        self.ISRUNNING = Utils.main.RUNTESTCHECK(self).FULL(True)
        self.ENDPOINT1 = Utils.ENDPOINTSYS.load(CONFIG=1, RAISEALL=True)
        self.SOCKET1 = Utils.SOCKET.connect(self.ENDPOINT1().parent(getatr=True, FULL=True, LOGGING=True))
        self.RECONNECT = Utils.SOCKET.reconnect(self.ENDPOINT1().parent(LOAD_PREV_ATR=True, KEEP_ATR=True, LORD=True))
        self.SHUTDOWN = Utils.ORMs.DELETE_CLASS_TABLE(main)
        self.CLOSE_CONNECTION = Utils.main.CLOSE_CURRENT_SOCKET_CONNECTION(True)
        
        @self.command(help='Track how long **Mecha Karen** has been online for.\n**Usage:**\n```\n-Uptime\n```')
        @commands.cooldown(1, 10, BucketType.user)
        async def uptime(ctx):
            delta_uptime = datetime.datetime.utcnow() - bot.launch_time
            hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            days, hours = divmod(hours, 24)
            embed = discord.Embed(title = "Uptime:",description = f"{days}d, {hours}h, {minutes}m", color = discord.Colour.red())
            await ctx.send(embed = embed)
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    raise e
        
        @self.before_invoke
        async def before_any_command(ctx):
            ctx.timer = time()
            try:
                await ctx.trigger_typing()
            except discord.errors.Forbidden:
                pass
            
        async def search(QUERY : str=None):
            data = UD.Search(QUERY)
            return {
                'PREV' : data
            }
        
        def QUANTIFY(x : list):
            if len(x) != 1:
                raise AttributeError('MUST CONTAIN 1 ELEMENT')
            for element in x:
                if not isinstance(element, list):
                    raise AttributeError('LIST GIVEN >> NOT NESTED')
                current_ = x.index(element, 0)
                if not isinstance(x[current_], list):
                  raise AttributeError('LIST GIVEN >> NOT NESTED ^2 <INDEX: yourlist[0][0]>')
                prev, attrs = x[current_][0], x[current_]
                x[current_] = [prev]
                x[0].append(attrs)
                return x
        
    @staticmethod
    async def on_connect():
        if self.ENDPOINT1.connected() != True:
            print('Endpoint 1 has failed to load.')
        elif not self.SOCKET1.connected():
            self.CLOSE_CONNECTION
            raise Utils.ERRORS.SOCKETFAILURE('Check if the socket is actually on.')
        if self.ISRUNNING != 'RUNNING':
            exit()
        try:
            async self.logging with self.MySQL as logging:
                start = "UPDATE logging SET start = main WHERE started = True"
                self.cursor.execute(start)
        except mysql.connector.Error as err:
            raise err
        try:
            x = self.STEPRISE
            if bool(x.connected()) != False and x.connected().latency() <= 100:
                raise "The API's latency is too high!"
            elif bool(x.connect()) != True and x.downtime().returnnum().convert(form=FACTOR) != 'CONNECTED':
                raise ConnectionRefusedError("The API refused to connected")
        except Utils.ERRORS.CREDENTIALS_WRONG as failure:
            raise failure
            
        print('Bot Connected')
        
    @staticmethod
    async def on_disconnect():
        for x in self.guilds:
            if not Utils.main.ISTABLELOADED(x):
                Utils.main.CLOSE(x, self.SHUTDOWN)
        try:
            x = self.RECONNECT
            if not x:
                raise Utils.ERRORS.MASACRE
            elif x.DISASTER_LVL_10_MAJOR != False:
                raise Utils.ERRORS.LORD_RECONNECT
            elif x.GUILDTABLELOADED != True:
                raise Utils.ERRORS.GUILD_ATR
        except mysql.connector.Error as err:
            raise err
        
    async def on_message_delete(self, message):
        if message.author.bot == True:
            pass
        else:
            db = self.TABLES[self.TABLES.index('SNIPETABLE', 0, -1)]
            sql = "INSERT INTO db (channel_id) VALUES (%s)"
            val = ('{message.channel.id : {"author" : message.author.name + "#" + message.author.discriminator, "user" : str(message.author.id), "content" : message.content, "created_at" : message.created_at.strftime('%I:%M %p')}}')
            db.cursor().execute(sql, val)
                
    async def on_guild_remove(self, guild):
        delete = "DROP TABLE {}".format(guild.id)
        self.cursor.execute(delete)
            
    async def on_guild_join(self, guild):
        x = NEWGUILDTABLE(self.cursor, guild.id, '-')
        if x == 'FAILED':
            for channel in guild.TextChannels:
                await channel.send('There was an error creating a table for your server. Please re-add me!')
                await asyncio.sleep(1)
            await guild.leave()
        elif x == 'WARNING':
            delete = "DROP TABLE {}".format(guild.id)
            self.cursor.execute(delete)
            try:
                x = NEWGUILDTABLE(self.cursor, guild.id, '-')
                if x == 'WARNING' or x == 'FAILED':
                    for channel in guild.TextChannels:
                        await channel.send('There was an error creating a table for your server. Please re-add me!')
                        await asyncio.sleep(1)
                    await guild.leave()
            except mysql.connector.Error:
                await guild.leave()

        channel = self.get_channel(753311458171027547)
        await channel.send('> <@!475357293949485076> You Retard.\n> I have made it into another server!\n\n> Guild Name: **{}**'.format(guild.name))
        
    async def on_message(self, msg):
        if hash(msg)+Utils.main.ASSIGN().HASHTYPE('SENIATICAL_V2.6').ECHO(self.TABLES[0]) in Utils.main.GETLOGGEDMESSAGE():
            return
        else:
            self.cursor.execute('FROM {} SELECT {} WHERE count = {}'.format(self.TABLES[0], msg.author.id, self.Utils.get_count(msg.author)))
        if isinstance(msg.channel, discord.DMChannel):
            if msg.author.bot == True:
                return
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
                if msg.author.bot == True:
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
            try:
                if msg.mentions[0] == self.user and msg.content == '<@!740514706858442792>':
                    await msg.channel.send('> Hello {}!\n> \n> I am Mecha Karen and thank you for inviting me. My prefix for the server is **`{}`** .'.format(msg.author.mention, get_prefix(bot, msg)[-1]))
            except Exception:
                pass
            await self.process_commands(message=msg)
        except Exception:
            pass
        
    async def close(self):
        await super().close()
        await self.session.close()

    def run(self):
        try:
            if x:
                Utils.ANTICOPY()
            super().run(DATA().TOKEN, reconnect=True)
            for _ in self.logging.FILES:
                try:
                    __logging__.update('cache')
                except Utils.LOGGINGERRORS.file_empty_error:
                    print('File : {} was empty. Couldnt be emptied within the cache.'.format(_))
            self.logging.load(__logging__.CACHE) 
        except discord.errors.LoginFailure:
            return 'Failed to run Mecha Karen!\nDue to Incorrect Credentials...'
        
    @property
    async def ver(self):
        return __import__('version')
    
    @property
    async def config(self):
        return __import__('Utils')

def kickstart():
    Utils.MechaBootUp('./Bot/bot.py')
    return True
