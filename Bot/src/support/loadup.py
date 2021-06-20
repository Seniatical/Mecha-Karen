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

import discord
from asyncio import sleep
from os import system, name
from discord.ext import commands
from colorama import Fore, init
import platform
import sys
from core._.handle_clear

os = platform.system()

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')
                        ## Cleans up stdout
    handle_clear()      ## This function cleans up the hidden area

class Boot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = bot.cache
        self.text = """\
 ███▄ ▄███▓▓█████  ▄████▄   ██░ ██  ▄▄▄          ██ ▄█▀▄▄▄       ██▀███  ▓█████  ███▄    █ 
▓██▒▀█▀ ██▒▓█   ▀ ▒██▀ ▀█  ▓██░ ██▒▒████▄        ██▄█▒▒████▄    ▓██ ▒ ██▒▓█   ▀  ██ ▀█   █ 
▓██    ▓██░▒███   ▒▓█    ▄ ▒██▀▀██░▒██  ▀█▄     ▓███▄░▒██  ▀█▄  ▓██ ░▄█ ▒▒███   ▓██  ▀█ ██▒
▒██    ▒██ ▒▓█  ▄ ▒▓▓▄ ▄██▒░▓█ ░██ ░██▄▄▄▄██    ▓██ █▄░██▄▄▄▄██ ▒██▀▀█▄  ▒▓█  ▄ ▓██▒  ▐▌██▒
▒██▒   ░██▒░▒████▒▒ ▓███▀ ░░▓█▒░██▓ ▓█   ▓██▒   ▒██▒ █▄▓█   ▓██▒░██▓ ▒██▒░▒████▒▒██░   ▓██░
░ ▒░   ░  ░░░ ▒░ ░░ ░▒ ▒  ░ ▒ ░░▒░▒ ▒▒   ▓▒█░   ▒ ▒▒ ▓▒▒▒   ▓▒█░░ ▒▓ ░▒▓░░░ ▒░ ░░ ▒░   ▒ ▒ 
░  ░      ░ ░ ░  ░  ░  ▒    ▒ ░▒░ ░  ▒   ▒▒ ░   ░ ░▒ ▒░ ▒   ▒▒ ░  ░▒ ░ ▒░ ░ ░  ░░ ░░   ░ ▒░
░      ░      ░   ░         ░  ░░ ░  ░   ▒      ░ ░░ ░  ░   ▒     ░░   ░    ░      ░   ░ ░ 
       ░      ░  ░░ ░       ░  ░  ░      ░  ░   ░  ░        ░  ░   ░        ░  ░         ░ 
                  ░                                                                        
"""

    @commands.Cog.listener()
    async def on_ready(self):
        async def status():
            for user in self.bot.users:
                res = await self.cache.base_template(user.id)
                if res == False:
                    print('Failed to add %s to the cache.' % str(user))
            
            while True:
                shard_count = self.bot.shard_count
                shards = self.bot.shards
                await self.bot.wait_until_ready()
                for i in range(shard_count):
                    shard = self.bot.get_shard(shards[i])
                    await self.bot.change_presence(status=discord.Status.do_not_disturb,
                                               activity=discord.Activity(type=discord.ActivityType.watching,
                                                                         name='-Help | {}/{}            https://mechakaren.xyz/'.format(1, shard_count)))
                await sleep(20)
        print(Fore.BLUE + 'All Cogs loaded!\n' + Fore.RESET)
        print(Fore.GREEN + f'{sys.version}\n\n' + Fore.RESET)
        print(Fore.LIGHTRED_EX + self.text + Fore.RESET)
        self.bot.loop.create_task(status())

    @commands.command()
    @commands.is_owner()
    async def reset(self, ctx):
        clear()
        print(Fore.BLUE + 'All Cogs loaded!\n' + Fore.RESET)
        print(Fore.GREEN + f'{sys.version}\n\n' + Fore.RESET)
        print(Fore.LIGHTRED_EX + self.text + Fore.RESET)
        return await ctx.send('Cleared the following:```\nInternal Cache\nLogging Cache\nSTDOUT && STDIN && STDERR\nGateway Storage\nAll Containers```')

def setup(bot):
    bot.add_cog(Boot(bot))
