import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed, File
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import os
import random

class ImageManipulation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('ImageManip Cog is ready')

    '''
    Trash!!!
    # YUP YUP YUP
    '''
    @commands.command()
    async def Trash(self, ctx, member : discord.Member=None):
        if member == None:
            avatar = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')
        else:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save(f"./Images/Avatar.jpg")
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')

        im1 = Image.open('./Images/bin.jpg')

        img_path = './Images/Avatar.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 130

        new_height = 134

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname.jpg", quality=95)

        img_path = './Images/Avatar2.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 105

        new_height = 109

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname2.jpg", quality=95)

        back_im = im1.copy()
        mrl = Image.open('./Images/outputname.jpg')
        mr = Image.open('./Images/outputname2.jpg')
        back_im.paste(mrl, (330, 185))
        back_im.paste(mr, (160, 30))
        back_im.save('./Images/trash.png', quality=95)
        await ctx.send(file=discord.File('./Images/trash.png'))
    '''
    END OF TRASH!!!
    NU NU NU
    '''
    '''
    SLAP!!!
    YUP YUP YUP
    '''
    @commands.command()
    async def Slap(self, ctx, member : discord.Member=None):
        if member == None:
            avatar = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')
        else:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')

        im1 = Image.open('./Images/slap.jpg')

        img_path = './Images/Avatar.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 130

        new_height = 134

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname.jpg", quality=95)

        img_path = './Images/Avatar2.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 105

        new_height = 109

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname2.jpg", quality=95)

        back_im = im1.copy()
        mrl = Image.open('./Images/outputname.jpg')
        mr = Image.open('./Images/outputname2.jpg')
        back_im.paste(mrl, (50, 63))
        back_im.paste(mr, (297, 54))
        back_im.save('./Images/slapped.jpg', quality=95)
        await ctx.send(file=discord.File('./Images/slapped.jpg'))
    '''
    End of Slap
    NU NU NU
    '''
    '''
    Spank
    YE YE YE
    '''
    @commands.command()
    async def Spank(self, ctx, member : discord.Member=None):
        if member == None:
            avatar = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')
        else:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')

        im1 = Image.open('./Images/spank.jpg')

        img_path = './Images/Avatar.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 250

        new_height = 254

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname.jpg", quality=95)

        img_path = './Images/Avatar2.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 400

        new_height = 404

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname2.jpg", quality=95)

        back_im = im1.copy()
        mrl = Image.open('./Images/outputname.jpg')
        mr = Image.open('./Images/outputname2.jpg')
        back_im.paste(mr, (870, 90))
        back_im.paste(mrl, (1400, 1050))
        back_im.save('./Images/spanked.jpg', quality=95)
        await ctx.send(file=discord.File('./Images/spanked.jpg'))
    '''
    End of Slap
    NU NU NU
    '''
    '''
    Boot
    YE YE YE
    '''
    @commands.command()
    async def Boot(self, ctx, member : discord.Member=None):
        if member == None:
            avatar = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')
        else:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
            avatar2 = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar2.save('./Images/Avatar2.jpg')

        im1 = Image.open('./Images/ballKick.jpg')

        img_path = './Images/Avatar.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 50

        new_height = 54

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname.jpg", quality=95)

        img_path = './Images/Avatar2.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 50

        new_height = 54

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname2.jpg", quality=95)

        back_im = im1.copy()
        mrl = Image.open('./Images/outputname.jpg')
        mr = Image.open('./Images/outputname2.jpg')
        back_im.paste(mrl, (183, 13))
        back_im.paste(mr, (33, 12))
        back_im.save('./Images/booted.jpg', quality=95)
        await ctx.send(file=discord.File('./Images/booted.jpg'))
    '''
    End of Boot
    NU NU NU
    '''
    '''
    Start of something
    YE YE YE
    '''
    @commands.command()
    async def Obese(self, ctx, member : discord.Member=None):
        if member == None:
            avatar = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
        elif member == ctx.author:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
        else:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')

        im1 = Image.open('./Images/obese.jpg')

        img_path = './Images/Avatar.jpg'
        img = Image.open(img_path)

        width, height = img.size
        asp_rat = width/height

        new_width = 130

        new_height = 134

        new_rat = new_width/new_height

        if (new_rat == asp_rat):
            img = img.resize((new_width, new_height), Image.ANTIALIAS)

        else:
            new_height = round(new_width / asp_rat)
            img = img.resize((new_width, new_height), Image.ANTIALIAS)
        img.save("./Images/outputname.jpg", quality=95)

        back_im = im1.copy()
        mrl = Image.open('./Images/outputname.jpg')
        back_im.paste(mrl, (390, 12))
        back_im.save('./Images/obesity.jpg', quality=95)
        await ctx.send(file=discord.File('./Images/obesity.jpg'))
        '''
            End of Something
            NU NU NU
        '''
        '''
            Start of something
            YE YE YE
        '''

        '''
            End of Something
            NU NU NU
        '''
        '''
            Start of something
            YE YE YE
        '''


def setup(bot):
    bot.add_cog(ImageManipulation(bot))
