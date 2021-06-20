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
import os
import json
import io
from PIL import Image, ImageDraw
import asyncio
import datetime
import aiohttp
import time


async def ending(count: int = 0):
    if count == 0:
        return 'The first member!'
    x = str(count)
    if '1' in x[-1]:
        ending = 'ˢᵗ'
    elif '2' in x[-1]:
        ending = 'ⁿᵈ'
    elif '3' in x[-1]:
        ending = 'ʳᵈ'
    else:
        ending = 'ᵗʰ'
    return '%s' % ending

def simplify(days):
    year = days // 365
    days %= 365
    months = days // 30
    days %= 30
    return '%s Year(s), %s Month(s) and %s day(s) ago.' % (year, months, days)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.channel = 

    @commands.Cog.listener()
    async def on_ready(self):
        async def myloop():
            while True:
                primary = self.bot.get_channel(789874799379742811)
                await primary.edit(name='MK Members | {}'.format(len(self.bot.users)))
                secondary = self.bot.get_channel(789952098938126336)
                await secondary.edit(name='MK Servers | {}'.format(len(self.bot.guilds)))
                secondary = self.bot.get_channel(789952098938126336)
                await asyncio.sleep(30)
                await secondary.edit(name='Members | {}'.format(len(self.bot.get_guild(740523643980873789).members)))
                
        self.bot.loop.create_task(myloop())

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 839184636948774963:
            await member.add_roles(member.guild.get_role(839202886796968017))

        if member.guild.id != 740523643980873789:
            return
        channel = self.bot.get_channel(776198796357926922)
        
        await channel.send(embed=discord.Embed(
            title='Welcome!',
            description='Welcome {} to {}. You are our {}{} member!'.format(member.mention, member.guild.name, member.guild.member_count, await ending(len(member.guild.members))),
            colour=discord.Colour.red()
        ), content='{}, To access the server, React with ✅ in <#741292472784912425> to <@!740514706858442792> Message!'.format(member.mention))

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(776198796357926922)
        if channel not in member.guild.channels:
            return
        await channel.send(f'**{member}** ({member.id}) has left us. Hope you come back soon!')

def setup(bot):
    bot.add_cog(Events(bot))
