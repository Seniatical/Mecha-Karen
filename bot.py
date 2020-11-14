"""

Discord bot made by Seniatical / _-*™#1234
Created at 5/8/2020
Available under the Apache License 2.0

"
A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.
"

"""
import datetime
import asyncio
import os
import json

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown

from Utils.main import *
from Utils.SQL import NEWGUILDTABLE
import version

import mysql.connector
from __future__ import print_function
from mysql.connector import errorcode

class Mecha_Karen(commands.AutoShardedBot):
    def __init__(self):
        allowed_mentions = discord.AllowedMentions(everyone=False, roles=False, users=True)
        intents = discord.Intents.all()
        super().__init__(
            command_prefix=PREFIX,
            case_insensitive=True,
            allowed_mentions=allowed_mentions,
            intents=intents,
            description='I am Mecha Karen. An open sourced bot inspiring others!',
            help_command=None,
            owner_id=475357293949485076,
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
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    raise e
        
    async def on_connect(self):
        if self.ENDPOINT1.connected() != True:
            print('Endpoint 1 has failed to load.')
        elif not self.SOCKET1.connected():
            self.CLOSE_CONNECTION
            raise Utils.ERRORS.SOCKETFAILURE
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
                raise "The API refused to connected"
        except Utils.ERRORS.CREDENTIALS_WRONG as failure:
            raise failure
            
        print('Bot Connected')
        
    async def on_disconnect(self):
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
                    await msg.channel.send('> Hello {}!\n> \n> I am Mecha Karen and thank you for inviting me. My prefix for the server is **`{}`** .'.format(msg.author.mention, get_prefix(bot, msg)))
            except Exception:
                pass
            await self.process_commands(message=msg)
        except Exception:
            pass
        
        '''
        self.command / self.before_invoke may be used here.
        If it doesnt work for you may be due to your python version or d.py version.
        If you have any questions join the support server and ask!
        '''
        
if __name__ == '__main__':
    bot = Mecha_Karen()
    
    '''
    If you want to create a command or a bot task. 
    This the place were you do it. 
    Events go in the class.
    We dont do the commands above. This is due to some confusion between events and loops
    It is possible to put a task/command in the class by doing :
    
    self.before_invoke
    
    or
    
    self.command()
    '''
    @bot.command()
    async def greet(ctx):
        await ctx.send('Hello. I am Mecha Karen. View my code by running command `Source`!')
    
    bot.run('')
