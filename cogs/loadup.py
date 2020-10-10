import asyncio
import json
import discord
import time
from asyncio import sleep
import traceback
from os import system, name
from random import randint
from discord.ext import commands
import re
import httpx
from colorama import Fore, init
import platform
import sys
import datetime
import test

os = platform.system()

if os == "Windows":
    system("cls")
else:
    system("clear")
    print(chr(27) + "[2J")

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
        print(Fore.LIGHTRED_EX + """\
                 
                 
                            ███▄ ▄███▓    ▓█████     ▄████▄      ██░ ██     ▄▄▄                ██ ▄█▀    ▄▄▄          ██▀███     ▓█████     ███▄    █ 
                            ▓██▒▀█▀ ██▒   ▓█   ▀    ▒██▀ ▀█     ▓██░ ██▒   ▒████▄              ██▄█▒    ▒████▄       ▓██ ▒ ██▒   ▓█   ▀     ██ ▀█   █ 
                            ▓██    ▓██░   ▒███      ▒▓█    ▄    ▒██▀▀██░   ▒██  ▀█▄           ▓███▄░    ▒██  ▀█▄     ▓██ ░▄█ ▒   ▒███      ▓██  ▀█ ██▒
                            ▒██    ▒██    ▒▓█  ▄    ▒▓▓▄ ▄██▒   ░▓█ ░██    ░██▄▄▄▄██          ▓██ █▄    ░██▄▄▄▄██    ▒██▀▀█▄     ▒▓█  ▄    ▓██▒  ▐▌██▒
                            ▒██▒   ░██▒   ░▒████▒   ▒ ▓███▀ ░   ░▓█▒░██▓    ▓█   ▓██▒         ▒██▒ █▄    ▓█   ▓██▒   ░██▓ ▒██▒   ░▒████▒   ▒██░   ▓██░
                            ░ ▒░   ░  ░   ░░ ▒░ ░   ░ ░▒ ▒  ░    ▒ ░░▒░▒    ▒▒   ▓▒█░         ▒ ▒▒ ▓▒    ▒▒   ▓▒█░   ░ ▒▓ ░▒▓░   ░░ ▒░ ░   ░ ▒░   ▒ ▒ 
                            ░  ░      ░    ░ ░  ░     ░  ▒       ▒ ░▒░ ░     ▒   ▒▒ ░         ░ ░▒ ▒░     ▒   ▒▒ ░     ░▒ ░ ▒░    ░ ░  ░   ░ ░░   ░ ▒░
                            ░      ░         ░      ░            ░  ░░ ░     ░   ▒            ░ ░░ ░      ░   ▒        ░░   ░       ░         ░   ░ ░ 
                                   ░         ░  ░   ░ ░          ░  ░  ░         ░  ░         ░  ░            ░  ░      ░           ░  ░            ░ 
                                                ░                                                                                                 
        """ + Fore.RESET)
        print(Fore.BLUE + 'All Cogs loaded!\n' + Fore.RESET)
        print(Fore.GREEN + f'{sys.version}\n' + Fore.RESET)
        self.bot.loop.create_task(status())

def setup(bot):
    bot.add_cog(Boot(bot))
