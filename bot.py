"""
Discord bot made by Seniatical / _-*™#7139
Created at 5/8/2020
Available under the Apache License 2.0

"
A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.
"

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

# Imports
import json
import random
import datetime
import time

import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
from discord.ext import tasks
import os
from asyncio import sleep
import asyncio
import requests

from Utils.main import *

# End of Imports

# Events and Variables

bot = BOT_PREF
bot.launch_time = datetime.datetime.utcnow()
Token = TOKEN
index = -1
os.chdir('C:\\Users\\Isa\\PycharmProjects\\Discord Bot')

bot.remove_command('help')

@tasks.loop(minutes=60, count=INF)
async def Time(minutes=60):
    global index
    print('Uptime is currently at {} hour.'.format(index + 1))
    index += 1

@Time.before_loop
async def is_ready_bot():
    await bot.wait_until_ready()

Time.start()

# Cog Loads

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
@commands.cooldown(1, 60, BucketType.user)
@commands.has_guild_permissions(administrator=True)
async def load(ctx, extention):
    bot.load_extension(f'cogs.{extention}')
    await ctx.send(f'{extention} cog has loaded')

@bot.command()
@commands.cooldown(1, 60, BucketType.user)
@commands.has_guild_permissions(administrator=True)
async def disable(ctx, extention):
    bot.unload_extension(f'cogs.{extention}')
    await ctx.send(f'{extention} cog has been disabled')

bot.run(Token)
