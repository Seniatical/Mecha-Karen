import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import os
import random

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

class SecretCommands(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Secret Command Cog is ready')

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def Creator(self, ctx):
        embed = discord.Embed(
            title='**The Creator**',
            color=discord.Color.blue()
        )
        embed.set_author(name='_-*™#7139',
                         icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256')
        embed.add_field(name='**Created Karen**', value='Wed, 5 August 2020, 10:21 AM UTC')
        embed.add_field(name='‏‏‎ ', value='‏‏‎ ')
        embed.add_field(name='‏‏‎ ‏‏**Registered**', value='Sat, 4 August 2018, 05:40 PM UTC')
        embed.add_field(name='**Skills**',
                        value='**1.** Boring as fuck\n**2.** Can program\n**3.** Once calculated star patterns using Python\n**4.** A Minimalist\n**5.** Like to push myself to my limits')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def F(self, ctx):
        await ctx.send('<:F_:745287381816574125>')
        await ctx.send(f'**{ctx.author.name}** has payed there respects')

    @commands.command()
    async def vanish(self, ctx):
        await ctx.message.add_reaction('✅')
        time.sleep(0.5)
        await ctx.author.kick(reason='You have vanished')
        await ctx.author.send('You have vanished')

    @commands.command()
    async def wild(self, ctx):
        await ctx.send('<:wild:748867833638944799>')

def setup(bot):
    bot.add_cog(SecretCommands(bot))
