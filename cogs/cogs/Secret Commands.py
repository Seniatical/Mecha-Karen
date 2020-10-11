import discord
from discord.ext import commands
import datetime
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown, get
import time
from time import gmtime
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import os
import random
import requests

from Others import *

class SecretCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def F(self, ctx, *args):
        x = ' '.join(map(str, args))
        await ctx.send('<:F_:745287381816574125>')
        if x == '':
            await ctx.send(f'**{ctx.author.name}** has payed their respects')
        else:
            await ctx.send(f'**{ctx.author.name}** has paid respects for **{x}**')

    @commands.command()
    async def vanish(self, ctx):
        await ctx.message.add_reaction('✅')
        time.sleep(0.5)
        await ctx.author.kick(reason='You have vanished')
        await ctx.author.send('You have vanished')

    @commands.command()
    async def wild(self, ctx):
        await ctx.send('<:wild:748867833638944799>')
        await ctx.send(f'This is {ctx.author.mention} in the future')

    @commands.command()
    async def fail(self, ctx):
        await ctx.send('<:fail:751827644190031984>')

    @commands.command(hidden=True)
    async def cat(self, ctx):
        """Gives you a random cat."""
        async with ctx.session.get('https://api.thecatapi.com/v1/images/search') as resp:
            if resp.status != 200:
                return await ctx.send('No cat found :(')
            js = await resp.json()
            await ctx.send(embed=discord.Embed(title='Random Cat').set_image(url=js[0]['url']))

    @commands.command()
    async def therapy(self, ctx):
        await ctx.send('https://imgur.com/DwzL2JL\n{} has recieved there therapy treatment'.format(ctx.author.mention))

    @commands.command()
    async def time(self, ctx, country=None):
        if country == None:
            if datetime.datetime.utcnow().hour > 12:
                past_noon = ' PM'
            else:
                past_noon = ' AM'
            if datetime.datetime.utcnow().hour < 10:
                deck = '0' + str(datetime.datetime.utcnow().hour)
            else:
                deck = str(datetime.datetime.utcnow().hour)
            await ctx.send('> ' + deck + ":" + str(datetime.datetime.utcnow().minute) + past_noon)
        else:
            await ctx.send('Time is\n> ' + datetime.datetime.now().strftime("%H:%M") + '\nTimezone is UTC')

    @commands.command()
    async def date(self, ctx):
        date = str(datetime.datetime.today().date())
        final_date = date.split('-')
        final_date = f'The date today is:\n> {final_date[2]}/{final_date[1]}/{final_date[0]}\n'
        await ctx.send(final_date)

    @commands.command()
    async def afk(self, ctx):
        user = ctx.author.display_name
        await ctx.author.edit(nick=f'[AFK] {user}')

    @commands.command(aliases=['Action'])
    async def actions(self, ctx):
            guild = ctx.author.guild
            entries = await guild.audit_logs(limit=None, user=guild.me).flatten()
            await ctx.send('The server has made {} moderation actions.'.format(len(entries)))

def setup(bot):
    bot.add_cog(SecretCommands(bot))
