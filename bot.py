# Imports
import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import json
import random
import datetime
import time

import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, MissingRequiredArgument
import os
from asyncio import sleep
import praw
from discord.utils import get
import asyncio
from collections import defaultdict
from os import walk

from aiofiles import open

import Bio
import Co
import IMG
import Jokes
import Memes
import Numbers
import Quotes
import Status
import Token
import art
import gender

# End of Imports
# Events and Variables
bot = commands.Bot(command_prefix='-', case_insensitive=True)
Token = Token.token
os.chdir('C:\\Users\\isa1b.DESKTOP-GMQ5DPV.000.001\\PycharmProjects\\Discord Bo')

bot.remove_command('help')

async def status():
    while True:
        await bot.wait_until_ready()
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='-Help | Use -Help Invite to invite Mecha Karen :O'))
        await sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'To {len(bot.commands)} Commands | {len(bot.users)} Users | {len(bot.guilds)} Servers'))
        await sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"My next updates."))
        await sleep(10)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='Any Errors. Join the support server and report!'))
@bot.event
async def on_ready():
    print(f'{bot.user} has Awoken!\n')
bot.loop.create_task(status())

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

@bot.command(aliases=['stat'])
@cooldown(1, 3, BucketType.user)
async def stats(ctx):
    embed = discord.Embed(
        title='Mecha Karen Current Stats:',
        color=discord.Color.red(), timestamp=datetime.datetime.utcnow(),
    )
    embed.add_field(name='Servers?', value=f'{len(bot.guilds)}')
    embed.add_field(name='Commands?', value=f'{len(bot.commands)}')
    embed.add_field(name='Users?', value=f'{len(bot.users)}')
    embed.add_field(name='Cogs?', value=f'{len(bot.cogs)}')
    embed.add_field(name='Case Insensitive?', value=f'{bot.case_insensitive}')
    embed.add_field(name="Emoji's?", value=f'{len(bot.emojis)}')
    embed.add_field(name='Cached Messages?', value=f'{len(bot.cached_messages)}')
    embed.add_field(name='Prefix?', value=f'{bot.command_prefix}')
    embed.add_field(name='Extensions?', value=f'{len(bot.extensions)}')
    embed.add_field(name='All Commands?', value=f'{len(bot.all_commands)}')
    embed.add_field(name='Help Command?', value=f'Help')
    embed.add_field(name='Extra Events?', value=f'{len(bot.extra_events)}')
    embed.add_field(name='Voice Clients?', value=f'{len(bot.voice_clients)}')
    embed.add_field(name='Bot Latency?', value=f'{round(bot.latency * 1000, 2)}')
    await ctx.send(embed=embed)

@bot.command()
async def cog(ctx):
    embed = discord.Embed(
        title='Current Cogs',
        color=discord.Color.red()
    )
    embed.add_field(name='Working Cogs', value='\n*Economy*\n*ImageManipulation*\n*Images*\n*Moderation*\n*Motivation*\n*UserChecks*\n*Help*\n*Fun*')
    await ctx.send(embed=embed)


# noinspection PyTypeChecker
@bot.command(aliases=['Animal'])
@commands.cooldown(1, 5, BucketType.user)
async def Animals(ctx):
    embed = discord.Embed(
        title='Menu!',
        color=discord.Color.green(),
        description='**Welcome to the Interactive Menu of `Animals`. In this section you can view all animals you can simulate into!**\nWhen using command `-Simulate` You must include the animal after!\n```You can all mention a user to simulate them too!\nThis works by doing:\n```\n`-Simulate bird @_-*™#7139` The animal must be defined first!\n**Animals are case sensitive to avoid any confusion they are lower cases**'
    )
    embed.add_field(name='This is the Starting Page', value='There a currently 2 Categories!')
    embed.set_footer(text='THESE ARE CASE SENSITIVE')
    msg = await ctx.send(embed=embed)
    def reaction_check1(m):
        user = ctx.author
        if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "➡️":
            return True
        return False

    try:
        await msg.add_reaction("➡️")
        await bot.wait_for('raw_reaction_add', timeout=20.0, check=reaction_check1)
        await msg.edit(embed=embed.set_field_at(index=0, name='Welcome To Insects!', value=f'`ants`, `beetle` `bees` `fly` `ladybird` `Mosquito` `flea` `butterfly` `dragonfly` `snail` `slug`', inline=True))
        await msg.clear_reaction('➡️')
        await msg.add_reaction("➡️")
        await bot.wait_for('raw_reaction_add', timeout=20.0, check=reaction_check1)
        await msg.edit(embed=embed.set_field_at(index=0, name='Welcome to Flying Animals!', value=f'`bird` `bat` `squirrel` `goose` `swan` `eagle` `crane` `kiwi`', inline=True))
        await msg.clear_reaction('➡️')
        await msg.add_reaction("➡️")
        await bot.wait_for('raw_reaction_add', timeout=20.0, check=reaction_check1)
        await msg.edit(embed=embed.set_field_at(index=0, name='Welcome to Land Animals!', value=f'`hippo` `lion` `tiger` `frog` `elephant` `gorilla` `monkey` `panda` `snake` `sloth` `koala` `crocodile` `reindeer` `bear` `wolf` `llama`', inline=True))
        await msg.clear_reaction('➡️')
        await msg.add_reaction("➡️")
        await bot.wait_for('raw_reaction_add', timeout=20.0, check=reaction_check1)
        await msg.edit(embed=embed.set_field_at(index=0, name='Welcome to Aquatic Animals!', value=f'`fish` `shark` `clam` `penguin` `seal` `narwhal` `starfish` `octopus`', inline=True))
        await msg.clear_reaction('➡️')
        await msg.add_reaction("➡️")
        await bot.wait_for('raw_reaction_add', timeout=20.0, check=reaction_check1)
        await msg.delete()
        await ctx.send(f'{ctx.author} has closed the Animals menu')
    except asyncio.TimeoutError:
        await msg.delete()
        await ctx.send(f"You never reacted in time! The interactive Menu for Animals was shutdown")

@bot.command(aliases=['bal', 'amount'])
async def balance(ctx, user : discord.Member=None):
    if user != None:
        user = user
    else:
        user = ctx.author
    await open_account(user)
    users = await get_bank_data()

    wal = users[str(user.id)]["wallet"]
    bank = users[str(user.id)]["bank"]
    embed = discord.Embed(
        title=f"{user}'s Balance:",
        color=discord.Color.green(), timestamp=datetime.datetime.utcnow()
    )
    embed.add_field(name='Wallet:', value=wal)
    embed.set_thumbnail(url=user.avatar_url)
    embed.add_field(name='‎‏‏‎ ‎‎', value='‏‏‎ ‎')
    embed.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
    embed.add_field(name='Bank:', value=bank)
    embed.set_footer(text=f'Requested by: {ctx.author}\n')
    await ctx.send(embed=embed)

@bot.command()
@commands.cooldown(1, 45, BucketType.user)
async def beg(ctx):
    user = ctx.author
    users = await get_bank_data()
    amount = random.randint(0, 500)
    names = ['Bob', 'God', 'The drug dealer', 'Your mom', 'Girl you dated', 'Some kid']
    if amount >0:
        await ctx.send(f'{random.choice(names)} gave you {amount} coins!')
    else:
        await ctx.send('You tried and failed LMFAO')

    users[str(user.id)]["wallet"] += amount
    with open('economy.json', 'w') as f:
        json.dump(users, f)

@bot.command()
async def cheat(ctx, amount=None, *, user : discord.Member=None):
    if user == None:
        user = ctx.author
    elif user == True:
        if user.guild != ctx.guild:
            await ctx.send('User is not in this guild')
        else:
            pass
    x = amount.isnumeric()
    if x == True:
        pass
    elif x <0:
        await ctx.send(f'{ctx.author} its evil to deduct amounts lmao!')
    else:
        await ctx.send('You trying to get words?')
    if ctx.author.id != 475357293949485076:
        await ctx.send('**You are not the creator of the bot!**')
    else:
        await ctx.send(f"{amount} coins will be going into {user}'s Bank!!!")
        users = await get_bank_data()

        users[str(user.id)]["wallet"] += int(amount)
        with open('economy.json', 'w') as f:
            json.dump(users, f)

async def open_account(user):

    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 0

    with open('economy.json', 'w') as f:
        json.dump(users, f)
    return True

async def get_bank_data():
    with open('economy.json', 'r') as f:
        users = json.load(f)
    return users

@bot.command(aliases=['GW'])
@commands.has_guild_permissions(administrator=True)
async def giveaway(ctx, duration=None, *args):
    global winner
    def convert(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)

    def check(m):
        return str(reaction.emoji) == '🎉' and user != bot.user
    x = ' '.join(map(str, args))
    if not duration.isnumeric():
        await ctx.send('The amount of time left is not a number!')
    else:
        embed = discord.Embed(
            title=x,
            color=discord.Color.teal(),
        )
        embed.add_field(name=f'React with‏‏‎ ‎:tada:‏‏‎ ‎to enter the giveaway\n\nEnds in:{convert(duration)}\n\nHosted by {ctx.author}', value='‏‏‎ ‎')
        embed.set_footer(text=f'Ends at • the time im doing')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('🎉')
        await bot.wait_for('on_raw_reaction_add', check=check)
        enters = []
        while True:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=duration, check=check)
                if reaction and user:
                  if str(user.id) in enters:
                    continue

                  else:
                    enters.append(str(user.id))
            except asyncio.TimeoutError:
                winner = random.choice(enters)
    await ctx.send(winner)

@bot.command()
async def convert(ctx, number=0):
    def convert1(seconds):
        seconds = seconds % (24 * 3600)
        hour = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return "%d:%02d:%02d" % (hour, minutes, seconds)
    await ctx.send(f'{number} seconds in Seconds, Minutes and Hours is:')
    await ctx.send(f'`{convert1(number)}`')


bot.run(Token)
