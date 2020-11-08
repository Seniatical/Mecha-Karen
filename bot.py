"""

Discord bot made by Seniatical / _-*™#7139
Created at 5/8/2020
Available under the Apache License 2.0

"
A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.
"

Any of my works are free for use. As mentioned above. Any small snippets or a few lines. Nothing too large. I dont mind if its not mentioned.
How ever using larger works. Such as a good chunk (10 - 20+) lines. A mention that the code has been originally made by me and edited by you is required.

When using this code you must remember what you can and cannot do.

Permissions:
    Commercial use
    Modification
    Distribution
    Patent use
    Private use

Limitations:
    Trademark use
    Liability
    Warranty

"""
import datetime
import asyncio
from time import time
import os
import json
import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from Utils.main import *
import version

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
        
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    self.load_extension(f'cogs.{filename[:-3]}')
                except Exception as e:
                    raise 'Failed to load {}. Due to {}'.format(filename, e)
        
    async def on_connect(self):
        print('Bot Connected')
    
    async def on_disconnect(self):
        print('Bot has disconnected.\nReconnecting Shortly')
        
    async def on_message_delete(self, message):
        if message.author.bot == True:
            pass
        else:
            with open('JSON/snipe.json', 'r') as f:
                snipe = json.load(f)
            snipe[str(message.channel.id)] = {}
            snipe[str(message.channel.id)]['author'] = message.author.name + '#' + message.author.discriminator
            snipe[str(message.channel.id)]['avatar'] = str(message.author.id)
            snipe[str(message.channel.id)]['message'] = message.content
            snipe[str(message.channel.id)]['created_at'] = message.created_at.strftime('%I:%M %p')
            with open('JSON/snipe.json', 'w') as f:
                json.dump(snipe, f, indent=4) 
                
    async def on_guild_remove(self, guild):
        with open('JSON/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes.pop(str(guild.id))

        with open('JSON/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)
            
    async def on_guild_join(self, guild):
        x = 0
        with open('JSON/prefixes.json', 'r') as f:
            prefixes = json.load(f)

        prefixes[str(guild.id)] = '-'

        with open('JSON/prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        channel = self.get_channel(753311458171027547)
        await channel.send('> <@!475357293949485076> You Retard.\n> I have made it into another server!\n\n> Guild Name: **{}**'.format(guild.name))
        
    async def on_message(self, msg):
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

