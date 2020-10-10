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

@bot.event
async def on_command_error(ctx, error):
    embed = discord.Embed(
        title='',
        color=discord.Color.red()
    )
    if isinstance(error, commands.BadArgument):
        embed.add_field(name='Finish the command', value='Finish the command off! smh.')
        await ctx.send(embed=embed)
    if isinstance(error, commands.MissingPermissions):
        embed.add_field(name='Invalid Permissions', value=f'You dont have {error.missing_perms} permissions')
        await ctx.send(embed=embed)
    if isinstance(error, commands.CommandNotFound):
        pass
    if isinstance(error, commands.CommandOnCooldown):
        if error.retry_after < 60:
            f=round(error.retry_after) / 60
            embed.add_field(name=f'Your on cooldown!', value=f'Stop trying. Wait {round(error.retry_after, 0)} seconds and retry again.')
            await ctx.send(embed=embed)
    if isinstance(error, commands.ArgumentParsingError):
        embed.add_field(name='Error', value='Something Went wrong. Reloading Mecha Karen!')
        await ctx.send(embed=embed)
        await bot.sleep(10)
    if isinstance(error, commands.BadUnionArgument):
        embed.add_field(name='Error', value='Something Went Wrong. Reloading Mecha Karen!')
        await ctx.send(embed=embed)
    #if isinstance(error, commands.)

@bot.event
async def on_member_join(member):
    print(f'{member} has joined')

@bot.event
async def on_member_remove(member):
    print(f'{member} has left')

@bot.event
async def on_guild_join(guild):
    with open('economy.json', 'r') as f:
        guilds = json.load(f)

    guilds[str(guild.id)] = '-'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

# End of Events
# Cog Loads

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

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(aliases=['Action'])
async def Actions(ctx):
        guild = ctx.author.guild
        entries = await guild.audit_logs(limit=None, user=guild.me).flatten()
        await ctx.send('The server has made {} moderation actions.'.format(len(entries)))

bot.run(Token)
