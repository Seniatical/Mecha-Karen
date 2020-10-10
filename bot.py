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

# Events

@bot.event
async def on_connect():
    print('Bot connected')

@bot.event
async def on_message_delete(message):
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

    @bot.event
    async def on_message(msg):
        try:
            if '👀' in msg.content:
                channel = discord.utils.get(msg.guild.channels, name=channels['tracking'])
                amount = 0
                if msg.channel.name == '👀tracking':
                    pass
                else:
                    x = list(msg.content)
                    for letter in x:
                        if '👀' in letter:
                            amount += 1
                    if amount > 1:
                        await channel.send('**{}** ({}) has sent \👀 {} times in `{}`.'.format(msg.author.name, msg.author.id, amount, msg.channel.name))
                    else:
                        await channel.send('**{}** ({}) has sent \👀 {} time in `{}`.'.format(msg.author.name, msg.author.id, amount, msg.channel.name))
            try:
                if msg.mentions[0] == bot.user:
                    await msg.channel.send('> Hello {}!\n> \n> I am Mecha Karen and thank you for inviting me. My prefix for the server is **`{}`** .'.format(msg.author.mention, get_prefix(bot, msg)))
                else:
                    pass
            except Exception:
                pass
        except Exception:
            pass
        await bot.process_commands(message=msg)

# End of Events PT1
        
# Start of Cog Load, Unload and Reload Functions

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
    
@bot.command()
@commands.cooldown(1, 60, BucketType.user)
@commands.has_guild_permissions(administrator=True)
async def reload(ctx, extention):
    bot.reload_extension(f'cogs.{extention}')
    await ctx.send('Reloaded {}'.format(extention))
    
@bot.command()
@commands.is_owner()
@cooldown(1, 300, BucketType.user)
async def sync(ctx):
    msg = await ctx.send('Syncing Mecha Karen now!')
    async with ctx.channel.typing():
        for file in os.listdir('./cogs'):
            if file.endswith('.py'):
                bot.reload_extension(f"cogs.{file[:-3]}")
    await msg.edit(content='Mecha Karen has been synced!')
    
# End of Cog Load, Unload and Reload Functions

bot.run(Token)
