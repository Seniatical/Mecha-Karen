# !/usr/bin/python

"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0
A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.
FULL LICENSE CAN BE FOUND AT:
    https://www.apache.org/licenses/LICENSE-2.0.html
Any violation to the license, will result in moderate action
You are legally required to mention (original author, license, source and any changes made)
"""

import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
from discord import File
import random
import os

from utility.quotes import words, images

class Motivation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.speech_paths = []

        for file in os.listdir('./storage/speeches'):
            if os.path.isdir(file):
                for _file in os.listdir(f'./storage/speeches/{file}'):
                    self.speech_paths.append(file + _file)
            else:
                self.speech_paths.append('./speeches/' + file)

    @commands.command(aliases=['Quotes'])
    @cooldown(1, 10, BucketType.user)
    async def quote(self, ctx):
        return await ctx.send(embed=discord.Embed(
            description=random.choice(words),
            colour=discord.Colour.gold()
        ))

    @commands.command(aliases=['VQ', 'ImgQ', 'IQuote'])
    @cooldown(1, 15, BucketType.user)
    async def imagequote(self, ctx):
        return await ctx.send(embed=discord.Embed(
            colour=discord.Colour.gold(),
        ).set_image(url=random.choice(images)))

    @commands.command(aliases=['Speeches'])
    @cooldown(1, 120, BucketType.user)
    async def speech(self, ctx):
        return await ctx.send(content='Enjoy this speech to listen to!',
                              file=discord.File(random.choice(self.speech_paths), filename='speech.mp3'))

def setup(bot):
    bot.add_cog(Motivation(bot))
