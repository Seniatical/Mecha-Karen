# !/usr/bin/python

"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0

A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.

FULL LISENCE CAN BE FOUND:
    https://www.apache.org/licenses/LICENSE-2.0.html

Any voilations to the lisence, will result in moderate action

Your required to mention (original author, lisence, source, any changes made)
"""

import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
import random

from Others import Quotes, IMG

class motivation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['Quotes'])
    @cooldown(1, 10, BucketType.user)
    async def Quote(self, ctx):
        embed = discord.Embed(
            title='Quotes',
            color=discord.Color.gold()
        )
        embed.add_field(name='Inspirational Quotes', value=f'{random.choice(Quotes.Ins)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['VQ', 'ImgQ', 'IQuote'])
    @cooldown(1, 15, BucketType.user)
    async def ImgQuote(self, ctx):
        embed = discord.Embed(
            title='Visual Motivation',
            color=discord.Color.gold()
        )
        embed.set_image(url=f'{random.choice(Quotes.img)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['Speeches'])
    @cooldown(1, 120, BucketType.user)
    async def Speech(self, ctx):
        embed = discord.Embed(
            title='Motivation',
            color=discord.Color.gold()
        )

        embed.add_field(name='**Speeches**', value=(
            '**Be motivated. Dont let anybody decide your future. Be strong and follow what you love.**‏‏'))
        await ctx.send(embed=embed)
        await ctx.send(file=File(f'{random.choice(IMG.speech)}'))

    @commands.command(aliases=['Gspeech', 'gs'])
    @cooldown(1, 180, BucketType.user)
    async def GreatSpeech(self, ctx):
        embed = discord.Embed(
            title='Motivation',
            color=discord.Color.gold()
        )

        embed.add_field(name='**Speeches**', value=(
            '**Your stronger than you think. Dont keep your dream in your mind. Show it. Prove the world what your made of.**‏‏'))
        await ctx.send(embed=embed)
        await ctx.send(file=File(f'{random.choice(IMG.speech)}'))

def setup(bot):
    bot.add_cog(motivation(bot))
