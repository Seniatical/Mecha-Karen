import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
import time
from PIL import Image
import os
import random
from io import BytesIO

# is_avatar_animated()

class image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def trash(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/trash.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((130, 134))
        pfp2 = pfp2.resize((105, 109))
        im = im.copy()
        im.paste(pfp, (330, 185))
        im.paste(pfp2, (160, 30))
        im.save('./Images/trash2.jpg')
        await ctx.send(file=discord.File('./Images/trash2.jpg'))

    @commands.command()
    async def slap(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/slap.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((130, 134))
        pfp2 = pfp2.resize((105, 109))
        im = im.copy()
        im.paste(pfp, (50, 63))
        im.paste(pfp2, (297, 54))
        im.save('./Images/slapped.jpg')
        await ctx.send(file=discord.File('./Images/slapped.jpg'))

    @commands.command()
    async def spank(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/spank.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((250, 254))
        pfp2 = pfp2.resize((400, 404))
        im = im.copy()
        im.paste(pfp2, (870, 90))
        im.paste(pfp, (1400, 1050))
        im.save('./Images/spanked.jpg')
        await ctx.send(file=discord.File('./Images/spanked.jpg'))

    @commands.command()
    async def boot(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/ballKick.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((50, 54))
        pfp2 = pfp2.resize((50, 54))
        im = im.copy()
        im.paste(pfp, (183, 13))
        im.paste(pfp2, (33, 12))
        im.save('./Images/booted.jpg')
        await ctx.send(file=discord.File('./Images/booted.jpg'))

    @commands.command()
    async def obese(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/obese.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((130,134))
        im.paste(pfp, (390, 12))
        im.save('./Images/obesity.jpg')
        await ctx.send(file=discord.File('./Images/obesity.jpg'))


    @commands.command()
    async def bird(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/bird.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((180,184))
        im.paste(pfp, (590, 11))
        im.save('./Images/bird2.jpg')
        await ctx.send(file=discord.File('./Images/bird2.jpg'))

    @commands.command(aliases=['five'])
    async def highfive(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/high.jpeg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((319, 319))
        pfp2 = pfp2.resize((319, 319))
        im = im.copy()
        im.paste(pfp, (350,300))
        im.paste(pfp2, (1425,430))
        im.save('./Images/high2.jpg')
        await ctx.send(file=discord.File('./Images/high2.jpg'))

    @commands.command()
    async def delete(self, ctx, user : discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/delete.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((194,191))
        im.paste(pfp, (121, 137))
        im.save('./Images/delete2.jpg')
        await ctx.send(file=discord.File('./Images/delete2.jpg'))

def setup(bot):
    bot.add_cog(image(bot))
