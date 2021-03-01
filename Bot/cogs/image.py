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
from discord.ext.commands import BucketType, cooldown
from PIL import Image, ImageOps, ImageFilter
import os
from io import BytesIO
from wand.image import Image as swirler
import aiohttp
import glob
import MK

class image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.warp = threading.Thread
        self.converter = commands.MemberConverter()
        self.client = MK.Client('$TOKEN YER LAD')   ## not my token so dont try :p
        self.args_format = bot.arg()

    @commands.command(name='Trash')
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
        file = discord.File('./Images/trash2.jpg', filename='trash2.jpg')
        embed = discord.Embed(title='{} Has Recycled {}!'.format(ctx.author.display_name, user.display_name), color=user.color).set_image(url='attachment://trash2.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Slap')
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
        file = discord.File('./Images/slapped.jpg', filename='slapped.jpg')
        embed = discord.Embed(title='{} Has Slapped {}!'.format(ctx.author.display_name, user.display_name), color=user.color).set_image(url='attachment://slapped.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Spank')
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
        file = discord.File('./Images/spanked.jpg', filename='spanked.jpg')
        embed = discord.Embed(title='{} Has Spanked {}!'.format(ctx.author.display_name, user.display_name), color=user.color).set_image(url='attachment://spanked.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Boot')
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
        file = discord.File('./Images/booted.jpg', filename='booted.jpg')
        embed = discord.Embed(title='{} Has Ended {} Kids!'.format(ctx.author.display_name, user.display_name), color=user.color).set_image(url='attachment://booted.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Obese')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def obese(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/obese.jpg').convert('RGB').resize((900, 900))
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((220,220))
        im.paste(pfp, (457, 135))
        im.save('./Images/obesity.jpg')
        file = discord.File('./Images/obesity.jpg', filename='obesity.jpg')
        embed = discord.Embed(title='{} Has Gained *a bit* of weight.'.format(user.display_name), color=user.color).set_image(url='attachment://obesity.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Bird')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def bird(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        im = Image.open('./Images/bird.jpg').convert('RGB').resize((900, 900))
        asset = user.avatar_url_as(format=None, static_format='jpg', size=128)
        data = BytesIO(await asset.read())
        pfp = Image.open(data)
        pfp = pfp.resize((220, 220))
        im.paste(pfp, (555, 60))
        im.save('./Images/bird2.jpg')
        file = discord.File('./Images/bird2.jpg', filename='bird2.jpg')
        embed = discord.Embed(title='{} Has Prepared to Migrate.'.format(user.display_name), color=user.color).set_image(url='attachment://bird2.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Delete')
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
        file = discord.File('./Images/delete2.jpg', filename='delete2.jpg')
        embed = discord.Embed(title='Preparing to remove {}'.format(user.display_name), color=user.color).set_image(url='attachment://delete2.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Invert')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def invert(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('invert', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='inverted.png')
        embed = discord.Embed(title='Inverted!', color=member.color).set_image(url='attachment://inverted.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Equalize')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def equalize(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('equalize', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='equalized.png')
        embed = discord.Embed(title='Equalized!', color=member.color).set_image(url='attachment://equalized.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Grayscale')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def grayscale(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('greyscale', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='greyscaled.png')
        embed = discord.Embed(title='Grayscale!', color=member.color).set_image(url='attachment://greyscaled.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Mirror')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def mirror(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('mirror', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='mirror.png')
        embed = discord.Embed(title='Mirrored!', color=member.color).set_image(url='attachment://mirror.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Posterize')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def posterize(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('posterize', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='posterize.png')
        embed = discord.Embed(title='Posterized!', color=member.color).set_image(url='attachment://posterize.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Solarize')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def solarize(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('solarize', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='solarize.png')
        embed = discord.Embed(title='Solarized!', color=member.color).set_image(url='attachment://solarize.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Transpose')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def transpose(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('transpose', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='transpose.png')
        embed = discord.Embed(title='Transposed!', color=member.color).set_image(url='attachment://transpose.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Flip')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def flip(self, ctx, *, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('flip', str(member.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='flip.png')
        embed = discord.Embed(title='Flipped!', color=member.color).set_image(url='attachment://flip.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Gamma')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def gamma(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = await self.client.image('gamma', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='gamma.png')
        embed = discord.Embed(title='Gammafied!', color=user.color).set_image(url='attachment://gamma.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Rainbow')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def rainbow(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = await self.client.image('rainbow', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='rainbow.png')
        embed = discord.Embed(title='Rainbow Filter', color=user.color).set_image(url='attachment://rainbow.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Autumn')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def autumn(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = await self.client.image('autumn', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='autumn.png')
        embed = discord.Embed(title='Autumn Filter', color=user.color).set_image(url='attachment://autumn.png')
        await ctx.send(file=file, embed=embed)
        
    @commands.command(name='Inferno')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def inferno(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = await self.client.image('inferno', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='inferno.png')
        embed = discord.Embed(title='Inferno Filter', color=user.color).set_image(url='attachment://inferno.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Twilight')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def twilight(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = await self.client.image('twilight', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='twilight.png')
        embed = discord.Embed(title='Twilight Filter', color=user.color).set_image(url='attachment://twilight.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Warp')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def warp(self, ctx, *, user: discord.Member = None):
        user = ctx.author if not user else user
        img = await self.client.image('warp', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='warp.png')
        embed = discord.Embed(title='Warped Filter', color=user.color).set_image(url='attachment://warp.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Blur')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def blur(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        img = await self.client.image('warp', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='blur.png')
        embed = discord.Embed(title='You now look like a foggy mirror!', color=member.color).set_image(url='attachment://blur.png')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cartoon(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        img = await self.client.image('cartoon', str(user.avatar_url_as(static_format='png')))
        file = discord.File(fp=img, filename='cartoon.png')
        embed = discord.Embed(title='Cartoon Filter', color=user.color).set_image(url='attachment://cartoon.png')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wasted(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        img = img.point(lambda p: p * 0.5)
        _filter = Image.open('./Images/wasted.jpg').resize((900, 900))
        img.paste(_filter, (0, 0), _filter)
        img.save('./Images/userwasted.jpg')
        file = discord.File('./Images/userwasted.jpg', filename='userwasted.jpg')
        embed = discord.Embed(title='Wasted', color=user.color).set_image(url='attachment://userwasted.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gayify(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        img = Image.open(BytesIO(await user.avatar_url_as(static_format='jpg', size=1024).read())).convert('RGB').resize((900, 900))
        _filter = Image.open('./Images/gay.jpg').resize((900, 900))
        img.paste(_filter, (0, 0), _filter)
        img.save('./Images/gayified.jpg')
        file = discord.File('./Images/gayified.jpg', filename='gayified.jpg')
        embed = discord.Embed(title=f'Looks like {user.display_name} is gay', color=user.color).set_image(url='attachment://gayified.jpg')
        await ctx.send(file=file, embed=embed)
        
def setup(bot):
    bot.add_cog(image(bot))
