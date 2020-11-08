import discord
from asyncio import sleep
from os import system, name
from discord.ext import commands
from colorama import Fore, init
import platform
import sys

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
        print(Fore.BLUE + 'All Cogs loaded!\n' + Fore.RESET)
        print(Fore.GREEN + f'{sys.version}\n' + Fore.RESET)
        self.bot.loop.create_task(status())

def setup(bot):
    bot.add_cog(Boot(bot))
