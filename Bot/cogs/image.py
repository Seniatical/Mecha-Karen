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
from discord.ext.commands import BucketType, cooldown
from PIL import Image, ImageOps, ImageFilter
import os
from io import BytesIO
import cv2
import numpy as np
import math
import random
from wand.image import Image as swirler

class image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def trash(self, ctx, *, user: discord.Member = None):
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
        im.paste(pfp, (260, 120))
        im.paste(pfp2, (105, 7))
        im.save('./Images/trash2.jpg')
        await ctx.send(file=discord.File('./Images/trash2.jpg'))

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def slap(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/slap.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((310, 310))
        pfp2 = pfp2.resize((320, 320))
        im = im.copy()
        im.paste(pfp2, (465, 70))
        im.paste(pfp, (810, 350))
        im.save('./Images/slapped.jpg')
        await ctx.send(file=discord.File('./Images/slapped.jpg'))

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def spank(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/spank.jpg')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        asset2 = ctx.author.avatar_url_as(format=None, static_format='jpg', size=128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp = pfp.resize((230, 230))
        pfp2 = pfp2.resize((320, 320))
        im = im.copy()
        im.paste(pfp2, (750, 25))
        im.paste(pfp, (1200, 455))
        im.save('./Images/spanked.jpg')
        await ctx.send(file=discord.File('./Images/spanked.jpg'))

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def boot(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/boot.jpg')
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
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def obese(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/obese.jpg').convert('RGB').resize((900, 900))
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((139,139))
        im.paste(pfp, (386, 80))
        im.save('./Images/obesity.jpg')
        await ctx.send(file=discord.File('./Images/obesity.jpg'))

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def bird(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/bird.jpg').convert('RGB').resize((900, 900))
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((120, 120))
        im.paste(pfp, (300, 35))
        im.save('./Images/bird2.jpg')
        await ctx.send(file=discord.File('./Images/bird2.jpg'))

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def delete(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/delete.jpg').convert('RGB')
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((196,196))
        im.paste(pfp, (121, 137))
        im.save('./Images/delete2.jpg')
        await ctx.send(file=discord.File('./Images/delete2.jpg'))

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def invert(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img = ImageOps.invert(image=img)
        img.save('./Images/inverted.jpg')
        file = discord.File('./Images/inverted.jpg', filename='inverted.jpg')
        embed = discord.Embed(title='Inverted!', color=member.color).set_image(url='attachment://inverted.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def equalize(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img = ImageOps.equalize(image=img)
        img.save('./Images/equalize.jpg')
        file = discord.File('./Images/equalize.jpg', filename='equalize.jpg')
        embed = discord.Embed(title='Equalized!', color=member.color).set_image(url='attachment://equalize.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def grayscale(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img = ImageOps.grayscale(image=img)
        img.save('./Images/grayscale.jpg')
        file = discord.File('./Images/grayscale.jpg', filename='grayscale.jpg')
        embed = discord.Embed(title='Grayscaled!', color=member.color).set_image(url='attachment://grayscale.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def mirror(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img = ImageOps.mirror(image=img)
        img.save('./Images/mirror.jpg')
        file = discord.File('./Images/mirror.jpg', filename='mirror.jpg')
        embed = discord.Embed(title='Mirrored!', color=member.color).set_image(url='attachment://mirror.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def posterize(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        try:
            img = ImageOps.posterize(image=img, bits=1)
        except NotImplementedError:
            return await ctx.send('The Library currently doesnt support this image type! P Mode.')
        img.save('./Images/posterize.jpg')
        file = discord.File('./Images/posterize.jpg', filename='posterize.jpg')
        embed = discord.Embed(title='Posterized!', color=member.color).set_image(url='attachment://posterize.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def solarize(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        try:
            img = ImageOps.solarize(image=img, threshold=128)
        except NotImplementedError:
            return await ctx.send('The Library currently doesnt support this image type! P Mode.')
        img.save('./Images/solarize.jpg')
        file = discord.File('./Images/solarize.jpg', filename='solarize.jpg')
        embed = discord.Embed(title='Solarized!', color=member.color).set_image(url='attachment://solarize.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def transpose(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        try:
            img = ImageOps.exif_transpose(image=img)
        except NotImplementedError:
            return await ctx.send('The Library currently doesnt support this image type! P Mode.')
        img.save('./Images/exif_transpose.jpg')
        file = discord.File('./Images/exif_transpose.jpg', filename='exif_transpose.jpg')
        embed = discord.Embed(title='Transposed!', color=member.color).set_image(url='attachment://exif_transpose.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def flip(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        try:
            img = ImageOps.flip(image=img)
        except NotImplementedError:
            return await ctx.send('The Library currently doesnt support this image type! P Mode.')
        img.save('./Images/flip.jpg')
        file = discord.File('./Images/flip.jpg', filename='flip.jpg')
        embed = discord.Embed(title='Flipped!', color=member.color).set_image(url='attachment://flip.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def gamma(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img.save('./Images/gamma.jpg')
        img = cv2.imread(r"./Images/gamma.jpg")
        img = cv2.applyColorMap(img, cv2.COLORMAP_JET)
        img = Image.fromarray(img)
        img.save('./Images/gamma.jpg')
        file = discord.File('./Images/gamma.jpg', filename='gamma.jpg')
        embed = discord.Embed(title='Gammafied!', color=user.color).set_image(url='attachment://gamma.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def rainbow(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img.save('./Images/rainbow.jpg')
        img = cv2.imread(r"./Images/rainbow.jpg")
        img = cv2.applyColorMap(img, cv2.COLORMAP_RAINBOW)
        img = Image.fromarray(img)
        img.save('./Images/rainbow.jpg')
        file = discord.File('./Images/rainbow.jpg', filename='rainbow.jpg')
        embed = discord.Embed(title='Rainbow Filter', color=user.color).set_image(url='attachment://rainbow.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def autumn(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img.save('./Images/autumn.jpg')
        img = cv2.imread(r"./Images/autumn.jpg")
        img = cv2.applyColorMap(img, cv2.COLORMAP_AUTUMN)
        img = Image.fromarray(img)
        img.save('./Images/autumn.jpg')
        file = discord.File('./Images/autumn.jpg', filename='autumn.jpg')
        embed = discord.Embed(title='Autumn Filter', color=user.color).set_image(url='attachment://autumn.jpg')
        await ctx.send(file=file, embed=embed)
        
    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def inferno(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img.save('./Images/inferno.jpg')
        img = cv2.imread(r"./Images/inferno.jpg")
        img = cv2.applyColorMap(img, cv2.COLORMAP_INFERNO)
        img = Image.fromarray(img)
        img.save('./Images/inferno.jpg')
        file = discord.File('./Images/inferno.jpg', filename='inferno.jpg')
        embed = discord.Embed(title='Inferno Filter', color=user.color).set_image(url='attachment://inferno.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def twilight(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img.save('./Images/twilight.jpg')
        img = cv2.imread(r"./Images/twilight.jpg")
        img = cv2.applyColorMap(img, cv2.COLORMAP_TWILIGHT_SHIFTED)
        img = Image.fromarray(img)
        img.save('./Images/twilight.jpg')
        file = discord.File('./Images/twilight.jpg', filename='twilight.jpg')
        embed = discord.Embed(title='Twilight Filter', color=user.color).set_image(url='attachment://twilight.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def warp(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        ref = Image.open('./Images/ref.jpg')
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize(ref.size)
        img.save('./Images/warp.jpg')
        img = cv2.imread(r"./Images/warp.jpg", cv2.IMREAD_GRAYSCALE)
        rows, cols = img.shape
        img_output = np.zeros(img.shape, dtype=img.dtype)
        for i in range(rows):
            for j in range(cols):
                offset_x = int(15.0 * math.sin(1.5 * 2.36 * i / 100))
                offset_y = int(15.0 * math.cos(1.5 * 2.36 * j / 100))
                if i+offset_y < rows and j+offset_x < cols:
                    img_output[i,j] = img[(i+offset_y) % rows,(j+offset_x) % cols]
                else:
                    img_output[i,j] = 0
        img = Image.fromarray(img_output)
        img.save('./Images/warp.jpg')
        file = discord.File('./Images/warp.jpg', filename='warp.jpg')
        embed = discord.Embed(title='Warped Filter', color=user.color).set_image(url='attachment://warp.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def blur(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900,900))
        img_ = img.filter(ImageFilter.GaussianBlur(radius=10))
        img_.save('./Images/Blur.jpg')
        file = discord.File('./Images/Blur.jpg', filename='Blur.jpg')
        embed = discord.Embed(title='You now look like a foggy mirror!', color=member.color).set_image(url='attachment://Blur.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def swirl(self, ctx, member: discord.Member = None, degree=-90):
        member = ctx.author if not member else member
        img = Image.open(BytesIO(await member.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img.save('./Images/test.jpg')
        try:
            degree = int(degree)
            if degree > 360:
                return await ctx.send('Max Swirl factor for positive is **360**!')
            elif degree < -360:
                return await ctx.send('Max Swirl factor for negatives is **-360**!')
        except ValueError:
            return await ctx.send('Degrees must be a number!')
        with swirler(filename='./Images/test.jpg') as img:
            img.swirl(degree =degree)
            img.save(filename='./Images/swirl.jpg')
        file = discord.File('./Images/swirl.jpg', filename='swirl.jpg')
        embed = discord.Embed(title='Spun around and around!', color=member.color).set_image(url='attachment://swirl.jpg')
        await ctx.send(file=file, embed=embed)

def setup(bot):
    bot.add_cog(image(bot))
