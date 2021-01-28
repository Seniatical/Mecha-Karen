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
from __logging__ import MOTHER_BOOT
import datetime
from Utils import boot
import json

os = platform.system()

if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")
    
'''
The code above clears your terminal. and prints a character which allows the text printed next to be coloured
This code will automatically run everytime you refresh the code or call the function below

This function can be called at anytime and anywhere.
It will clear the terminal giving you a fresh slate and this prevents miles and miles long error codes.
Concept is pretty simple if you dont understand read on it here. This will show what its used for and how to use it:
    https://www.geeksforgeeks.org/python-os-system-method/
'''

def clear():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

class Boot(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async def status():
            while True:
                await self.bot.wait_until_ready()
                await self.bot.change_presence(status=discord.Status.do_not_disturb ,activity=discord.Activity(type=discord.ActivityType.watching, name='-Help | Use -Invite to invite Mecha Karen 👀'))
                await sleep(10)
                await self.bot.change_presence(status=discord.Status.do_not_disturb ,activity=discord.Activity(type=discord.ActivityType.listening, name=f'{len(self.bot.commands)} Commands | {len(self.bot.users)} Users | {len(self.bot.guilds)} Servers'))
                await sleep(10)
                await self.bot.change_presence(status=discord.Status.do_not_disturb ,activity=discord.Activity(type=discord.ActivityType.watching, name=f"My next updates."))
                await sleep(10)
                await self.bot.change_presence(status=discord.Status.do_not_disturb ,activity=discord.Activity(type=discord.ActivityType.listening, name='the Manager!'))
                await sleep(10)
                await self.bot.change_presence(status=discord.Status.do_not_disturb ,activity=discord.Activity(type=discord.ActivityType.playing, name='Use -Source to view the source code!'))
                await sleep(10)
        self.bot.dispatch(boot)
        print(Fore.BLUE + 'All Cogs loaded!\n' + Fore.RESET)
        print(Fore.GREEN + f'{sys.version}\n' + Fore.RESET)
        self.bot.loop.create_task(status())
        
    @staticmethod
    @commands.Cog.listener()
    async def boot():
        with open('./Utils/configs/setup_settings.json', 'r') as f:
            settings = json.load(f)
        MOTHER_BOOT(
            configs = {
                BOOT = True
                LOAD = False
                STATUS = 'Active',
                LAUNCHED = datetime.datetime.now(),
                BRANCHES = (
                    'MOTHER' ## Main branch
                    'INTERNAL HELPERS',
                    'MULTI-EXTENT-BRANCHES -> LEECH INTERNAL HELPERS'   ## Branches can go mad once off the internal helpers branch
                )
            },
            SETTINGS = settings
        )

def setup(bot):
    bot.add_cog(Boot(bot))
