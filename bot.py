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

# Owner commands for loading and reload certain JSON files!

@bot.command()
@cooldown(1, 1000, BucketType.guild)
async def add(ctx, file=None, *, message=None):
    if ctx.author.id == 475357293949485076:
        with open(f'JSON/{file}.json', 'r') as f:
            guilds = json.load(f)

        for guild in bot.guilds:
            guilds[str(guild.id)] = f'{message}'

            with open(f'JSON/{file}.json', 'w') as f:
                json.dump(guilds, f, indent=4)
        await ctx.send("Added all guild ID's to the json file!")
    else:
        await ctx.send('You do not own the bot!')

@bot.command()
@cooldown(1, 1000, BucketType.guild)
async def add1(ctx, file=None, *, message=None):
    if ctx.author.id == 475357293949485076:
        with open(f'JSON/{file}.json', 'r') as f:
            guilds = json.load(f)

        for user in bot.users:
            guilds[str(user.id)] = {}
            guilds[str(user.id)]['Level'] = '1'

            with open(f'JSON/{file}.json', 'w') as f:
                json.dump(guilds, f, indent=4)
        await ctx.send("Added all guild ID's to the json file!")
    else:
        await ctx.send('You do not own the bot!')

@bot.command()
async def update(ctx, channelid : int=0, *args):
    if ctx.author.id != 475357293949485076:
        await ctx.send('You do not own the bot!')
    else:
        message = ' '.join(map(str, args))
        if channelid == 0:
            channels = []
        channel = bot.get_channel(channelid)
        await channel.send(message)
        await ctx.send('Successfully sent the message!')

# End of owner commands

# Uptime Command / Others Which I cba moving.

@bot.command()
@commands.cooldown(1, 10, BucketType.user)
async def uptime(ctx):
    delta_uptime = datetime.datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"{days}d, {hours}h, {minutes}m")

@bot.command()
@commands.cooldown(1, 10, BucketType.member)
async def emote(ctx, choice=None):
    if choice == None:
        await ctx.send(bot.emojis[0])
    else:
        for emoji in bot.emojis:
            if choice == emoji.name:
                await ctx.send(emoji)

@bot.command()
@commands.cooldown(1, 60, BucketType.member)
async def covid(ctx, Country=None):
    global x
    if Country == None:
        COVID()
        embed = discord.Embed(
            title='Cases!',
            colour=discord.Color.red()
        )
        embed.description=f'Cases : {COVID.cases:,}\nDeaths : {COVID.deaths:,}\nRecovered : {COVID.recovered:,}'
        await ctx.send(embed=embed)
    else:
        COVID_SPECIFIC(Country)
        if COVID_SPECIFIC.error == 'nil':
            embed = discord.Embed(
                title='Global Cases!',
                colour=discord.Color.red()
            )
            embed.description=f'Cases : {COVID_SPECIFIC.cases:,}\nDeaths : {COVID_SPECIFIC.deaths:,}\nRecovered : {COVID_SPECIFIC.recovered:,}'
            await ctx.send(embed=embed)
        elif COVID_SPECIFIC.error == 'no':
            j = COVID_SPECIFIC.country_code1
            i = COVID_SPECIFIC.country_code2
            await ctx.author.send(j)
            await ctx.author.send(i)

        else:
            await ctx.send(COVID_SPECIFIC.error)

bot.run(Token)

bot.run(Token)
