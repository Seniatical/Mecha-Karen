import typing

import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from PIL import Image, ImageDraw
from io import BytesIO
import aiohttp
import vacefron
import MK
import numpy as np
import random
import cv2

from core._ import extract_
from core._.image.effects import *
from core._.image._ import sort_size, save_image

class _Image(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.converter = commands.MemberConverter()
        self.vac_api = vacefron.Client()
        self.client = MK.Async.Client(bot.env('API_TOKEN'))
        self.ses = aiohttp.ClientSession()
        self.cache = bot.cache
        self.loop = bot.loop
        self.beard_image = Image.open('./storage/images/beard.png')
        self.wasted_template = Image.open('./storage/images/wasted.png').resize((900, 900))

        self.emoji_c = commands.PartialEmojiConverter()

        bot.api_c = self.client

    @staticmethod
    def pixelate(image_to_pixelate: Image) -> Image:
        return image_to_pixelate.resize((32, 32), resample=Image.NEAREST).resize((1024, 1024), resample=Image.NEAREST)

    @staticmethod
    def quantize(image_to_quantize: Image) -> Image:
        return image_to_quantize.quantize()

    @commands.command(name='Trash')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def trash(self, ctx, *, argument: str = None):

        def execute(_author, _user):
            im = Image.open('./storage/images/trash.jpg')

            author = Image.open(_author).convert('RGBA').resize((130, 134))
            member = Image.open(_user).convert('RGBA').resize((105, 109))

            im.paste(author, (260, 120))
            im.paste(member, (105, 7))

            with BytesIO() as b:
                im.save(b, 'PNG')
                b.seek(0)
                file = discord.File(fp=b, filename='trash.png')
            return file

        author_av = BytesIO(await ctx.author.avatar.read())
        user_av = await extract_.get_stream(ctx, query=argument)

        if not user_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av, user_av)
        await future

        await ctx.send(
            embed=discord.Embed(title='Hes getting recycled', colour=random.randint(0x000000, 0xFFFFFF)).set_image(
                url='attachment://trash.png'),
            file=future.result())

    @commands.command(name='Slap')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def slap(self, ctx, *, argument: str = None):

        def execute(_author, _user):
            im = Image.open('./storage/images/slap.jpg')

            author = Image.open(_author).convert('RGBA').resize((310, 310))
            member = Image.open(_user).convert('RGBA').resize((320, 320))

            im = im.copy()
            im.paste(author, (465, 70))
            im.paste(member, (810, 350))

            with BytesIO() as buffer:
                im.save(buffer, format='PNG')
                buffer.seek(0)
                return discord.File(buffer, filename='slapped.png')

        author_av = BytesIO(await ctx.author.avatar.read())
        user_av = await extract_.get_stream(ctx, query=argument)

        if not user_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av, user_av)
        await future

        embed = discord.Embed(title='He just got SLAPPED!',
                              color=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://slapped.png')
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(name='Spank')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def spank(self, ctx, *, argument: str = None):

        def execute(_author, _user):
            im = Image.open('./storage/images/spank.jpg').convert('RGBA')

            author = Image.open(_author).convert('RGBA').resize((230, 230))
            member = Image.open(_user).convert('RGBA').resize((320, 320))

            im = im.copy()
            im.paste(member, (750, 25))
            im.paste(author, (1200, 455))

            with BytesIO() as buffer:
                im.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='spanked.png')
            return file

        author_av = await extract_.get_stream(ctx, query=argument)
        user_av = BytesIO(await ctx.author.avatar.read())

        if not author_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av, user_av)
        await future

        embed = discord.Embed(title='Who\'s being a naughty boy',
                              color=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://spanked.png')
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(name='Boot')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def boot(self, ctx, *, argument: str = None):

        def execute(_author, _user):
            im = Image.open('./storage/images/boot.jpg')

            _author = Image.open(_author).convert('RGBA').resize((50, 54))
            _user = Image.open(_user).convert('RGBA').resize((50, 54))

            im = im.copy()
            im.paste(_author, (183, 13))
            im.paste(_user, (33, 12))

            with BytesIO() as buffer:
                im.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='booted.png')
            return file

        author_av = await extract_.get_stream(ctx, query=argument)
        user_av = BytesIO(await ctx.author.avatar.read())

        if not author_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av, user_av)
        await future

        embed = discord.Embed(title='Right in the sacks',
                              color=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://booted.png')
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(name='Obese')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def obese(self, ctx, *, argument: str = None):

        def execute(_author):
            im = Image.open('./storage/images/obese.jpg').convert('RGBA').resize((900, 900))

            _author = Image.open(_author).convert('RGBA').resize((220, 220))
            im.paste(_author, (457, 135))

            with BytesIO() as buffer:
                im.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='obese.png')
            return file

        author_av = await extract_.get_stream(ctx, query=argument)

        if not author_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av)
        await future

        embed = discord.Embed(title='He\'s not that fat *yet*.',
                              color=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://obese.png')
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(name='Bird')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def bird(self, ctx, *, argument: str = None):

        def execute(_author):
            im = Image.open('./storage/images/bird.jpg').convert('RGBA').resize((900, 900))
            _author = Image.open(_author).convert('RGBA').resize((220, 220))
            im.paste(_author, (555, 60))

            with BytesIO() as buffer:
                im.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='bird.png')
            return file

        author_av = await extract_.get_stream(ctx, query=argument)

        if not author_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av)
        await future

        embed = discord.Embed(title='Somebody is preparing to migrate',
                              colour=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://bird.png')
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(name='Delete')
    @commands.bot_has_guild_permissions(send_messages=True, attach_files=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def delete(self, ctx, *, argument: str = None):

        def execute(_author):
            im = Image.open('./storage/images/delete.jpg').convert('RGB')

            _author = Image.open(_author).convert('RGBA').resize((196, 196))
            im.paste(_author, (121, 137))

            with BytesIO() as buffer:
                im.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='delete.png')
            return file

        author_av = await extract_.get_stream(ctx, query=argument)

        if not author_av:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, author_av)
        await future

        embed = discord.Embed(title='Moving file to the recycle bin',
                              color=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://delete.png')
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(name='Invert')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def invert(self, ctx, argument: str = None, animate: str = '--true', *size) -> typing.Union[discord.MessageReference, discord.Embed]:
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.invert, stream, animate, *size)
        embed = discord.Embed(title='Inverted!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Equalize')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def equalize(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.equalize, stream, animate, *size)
        embed = discord.Embed(title='Equalized!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Grayscale')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def grayscale(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.grayscale, stream, animate, *size)
        embed = discord.Embed(title='Grayscaled!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Mirror')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def mirror(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.mirror, stream, animate, *size)
        embed = discord.Embed(title='Mirrored!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Posterize')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def posterize(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.posterize, stream, animate, *size, {'bits': 1})
        embed = discord.Embed(title='Posterized!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Solarize')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def solarize(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.solarize, stream, animate, *size, {'threshold': 255})
        embed = discord.Embed(title='Solarized!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Transpose')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def transpose(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.exif_transpose, stream, animate, *size)
        embed = discord.Embed(title='Transposed!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Flip')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def flip(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        file = await self.loop.run_in_executor(None, IMAGEOPS, ImageOps.flip, stream, animate, *size)
        embed = discord.Embed(title='Flipped!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))

        try:
            await ctx.message.reply(file=file, embed=embed)
        except Exception:
            ## FILE TOO LARGE
            return await ctx.message.reply(content='Oh No, This file was too large!')

    @commands.command(name='Gamma')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def gamma(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('gamma', str(img))
        except Exception as e:
            print(e)
            return await ctx.send('Invalid image URL passed.')

        file = discord.File(fp=img, filename='gamma.png')
        embed = discord.Embed(title='Gammafied!', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://gamma.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Rainbow')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def rainbow(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('rainbow', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='autumn.png')
        embed = discord.Embed(title='Autumn Filter', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://autumn.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Autumn')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def autumn(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('autumn', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='autumn.png')
        embed = discord.Embed(title='Autumn Filter', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://autumn.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Inferno')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def inferno(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('hsv', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='inferno.png')
        embed = discord.Embed(title='Inferno Filter', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://inferno.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Twilight')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def twilight(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('twilight', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='twilight.png')
        embed = discord.Embed(title='Twilight Filter', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://twilight.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Warp')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def warp(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('warp', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='warp.png')
        embed = discord.Embed(title='Warped Filter', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://warp.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Blur')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def blur(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('blur', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='blur.png')
        embed = discord.Embed(title='You now look like a foggy mirror!',
                              color=random.randint(0x000000, 0xFFFFFF)).set_image(url='attachment://blur.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Swirl')
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def swirl(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('swirl', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')
        file = discord.File(fp=img, filename='swirl.png')
        embed = discord.Embed(title='Round and a round', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://swirl.png')
        await ctx.send(file=file, embed=embed)

    @commands.command(name='Achievement')
    @commands.cooldown(1, 10, BucketType.user)
    async def achievement(self, ctx, *, message: str = None):
        message = 'Nothing.' if not message else message
        message = message.replace(' ', '%20')
        url = 'https://minecraftskinstealer.com/achievement/{}/Achievement%20Earned!/{}'.format(random.randrange(40),
                                                                                                message)
        embed = discord.Embed(colour=discord.Colour.red()).set_image(url=url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cartoon(self, ctx, *, argument: str = None):
        img = await extract_.get_url(ctx, query=argument)
        try:
            img = await self.client.image('cartoon', str(img))
        except Exception:
            return await ctx.send('Invalid image URL passed.')

        file = discord.File(fp=img, filename='cartoon.png')
        embed = discord.Embed(title='Cartoon Filter', color=ctx.author.color).set_image(url='attachment://cartoon.png')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def beard(self, ctx, *args):
        if not args:
            user = ctx.author
            pos_x: str = '290'
            pos_y: str = '250'
            beard_x: str = '300'
            beard_y = '300'
        else:
            try:
                user = await self.converter.convert(ctx, args[0])
            except commands.errors.MemberNotFound:
                user = ctx.author
            if len(args) > 1:
                pos_x = args[1]
            else:
                pos_x = '290'
            if len(args) > 2:
                pos_y = args[2]
            else:
                pos_y = '250'
            if len(args) > 3:
                beard_x = args[3]
            else:
                beard_x = '300'
            if len(args) > 4:
                beard_y = args[4]
            else:
                beard_y = '300'
        try:
            positions = [pos_x, pos_y, beard_x, beard_y]
            new_pos = list(map(int, positions))
            if any([i for i in new_pos if i > 900 or i < 1]):
                return await ctx.send('Markers cannot be larger than 900 or less than 1')
        except ValueError:
            return await ctx.send('Markers to place or resize the beard must be numbers!')
        user = user or ctx.author

        raw_beard = self.beard_image

        beard = raw_beard.resize((new_pos[2], new_pos[3]))

        avatar = Image.open(BytesIO(await user.avatar.with_format(format='png').read())).convert(
            'RGBA').resize((900, 900))
        avatar.paste(beard, (new_pos[0], new_pos[1]), beard)

        with BytesIO() as buffer:
            avatar.save(buffer, format='PNG')
            buffer.seek(0)
            file = discord.File(buffer, filename='bearded.jpg')

        embed = discord.Embed(title=f'Given {user.display_name} a nice beard', color=user.color).set_image(
            url='attachment://bearded.jpg')
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wasted(self, ctx, user: discord.Member = None):
        user = user or ctx.author

        def execute(image):
            img = Image.open(image).convert('RGB').resize((900, 900))
            img = img.point(lambda p: p * 0.5)

            img.paste(self.wasted_template, (0, 0), self.wasted_template)

            with BytesIO() as buffer:
                img.save(buffer, 'PNG')
                buffer.seek(0)
                file = discord.File(fp=buffer, filename='wasted.jpg')
                return file

        image = await self.loop.run_in_executor(None,
                                                execute,
                                                BytesIO(await user.avatar.with_format(format='png').read())
                                                )
        await ctx.send(embed=discord.Embed(title='Wasted', colour=user.colour).set_image(url='attachment://wasted.jpg'),
                       file=image)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def gayify(self, ctx, argument: str = None, animate: str = '--true', *size):
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.send('Invalid image provided')

        file = await self.loop.run_in_executor(None, gayify_, stream, animate, *size)
        embed = discord.Embed(title=f'Gay Filter', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://{}'.format(file.filename))
        await ctx.send(file=file, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def distracted(self, ctx, user1: discord.Member = None, user2: discord.Member = None,
                         user3: discord.Member = None):
        m1 = user1 or ctx.author
        m2 = user2 or ctx.author
        m3 = user3 or ctx.author
        user = await self.vac_api.distracted_bf(m1.avatar.with_format(format='png'),
                                                m2.avatar.with_format(format='png'),
                                                m3.avatar.with_format(format='png'))
        image_out = discord.File(fp=await user.read(), filename="distracted.png")
        embed = discord.Embed(title=f'Oh no.', color=random.randint(0x000000, 0xFFFFFF)).set_image(
            url='attachment://distracted.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dos(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        data = await self.vac_api.dock_of_shame(user.avatar.with_format(format='png'))
        image_out = discord.File(fp=await data.read(), filename="dockofshame.png")
        embed = discord.Embed(title=f'SHAME THEM!', color=user.colour).set_image(url='attachment://dockofshame.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def drip(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        data = await self.vac_api.drip(user.avatar.with_format(format='png'))
        image_out = discord.File(fp=await data.read(), filename="drip.png")
        embed = discord.Embed(title=f'Speechless', color=user.colour).set_image(url='attachment://drip.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cr(self, ctx, *, text: str):
        user = await self.vac_api.car_reverse(text)
        image_out = discord.File(fp=await user.read(), filename="carreverse.png")
        embed = discord.Embed(title=f'Car Reverse Meme', color=ctx.author.colour).set_image(
            url='attachment://carreverse.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cmm(self, ctx, *, text: str):
        user = await self.vac_api.change_my_mind(text)
        image_out = discord.File(fp=await user.read(), filename="changemymind.png")
        embed = discord.Embed(title=f'Change My Mind.', color=ctx.author.colour).set_image(
            url='attachment://changemymind.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def heaven(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        data = await self.vac_api.heaven(user.avatar.with_format(format='png'))
        image_out = discord.File(fp=await data.read(), filename="heaven.png")
        embed = discord.Embed(title=f'They have ascended.', color=user.colour).set_image(url='attachment://heaven.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def table_flip(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        data = await self.vac_api.table_flip(user.avatar.with_format(format='png'))
        image_out = discord.File(fp=await data.read(), filename="tableflip.png")
        embed = discord.Embed(title=f'{user.display_name} looks fiesty.', color=user.colour).set_image(
            url='attachment://tableflip.png')
        await ctx.send(file=image_out, embed=embed)

    @commands.command(aliases=['color'], name='Colour')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def get_colour(self, ctx, colour):
        try:
            colour = int((str((await self.converter.convert(ctx, colour)).colour)).replace('#', '0x'), 16)
        except Exception:
            try:
                colour = int(colour.replace('#', '0x'), 16)
            except Exception:
                return await ctx.send('Invalid hex code provided.')
        with BytesIO() as b:
            new = Image.new(mode='RGB', size=(900, 900), color=colour)
            new.save(b, 'PNG')
            b.seek(0)
            await ctx.send(file=discord.File(fp=b, filename='{}.png'.format(colour)),
                           embed=discord.Embed(title='Created new colour:', colour=colour).set_image(
                               url='attachment://{}.png'.format(colour)))

    @commands.command(name='8bit')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bittify(self, ctx, argument: str = None, animate: str = '--true', *size) -> discord.Embed:
        _io = await extract_.get_stream(ctx, query=argument)

        if not image:
            return await ctx.send('Invalid image provided')

        def execute(_io, animate, size):
            avatar = Image.open(_io)
            duration = avatar.info.get('duration')
            loops = avatar.info.get('loop')

            if not size and not getattr(_io, 'discord', False):
                size = avatar.size
            else:
                size = sort_size(*size)

            if getattr(avatar, 'is_animated', False) and animate.lower() == '--true':
                frames = []
                for _ in range(avatar.n_frames):
                    avatar.seek(_)
                    frames.append(self.quantize(self.pixelate(avatar)).resize(size))
                return save_image(frames, filename='8bit.gif', duration=duration, loop=loops)

            eightbit = self.pixelate(avatar)
            eightbit = self.quantize(eightbit).resize(size)

            with BytesIO() as buffer:
                eightbit.save(buffer, format="PNG")
                buffer.seek(0)

                file = discord.File(buffer, filename="8bit.png")
            return file

        if not _io:
            return await ctx.send('Invalid image provided')

        future = self.loop.run_in_executor(None, execute, _io, animate, size)
        await future

        embed = discord.Embed(
            title="8-Bit filter",
            colour=ctx.author.colour
        )
        embed.set_image(url="attachment://{}".format(future.result().filename))
        await ctx.send(file=future.result(), embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def oil(self, ctx, *, argument: str = None):
        image = await extract_.get_stream(ctx, query=argument)

        if not image:
            return await ctx.send('Invalid image provided')

        def execute(image):
            image.seek(0)

            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.waitKey(1)

            try:
                oil = cv2.xphoto.oilPainting(image, 7, 1)
            except Exception:
                return False

            with BytesIO() as buffer:
                image = Image.fromarray(oil)
                image.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='oilpainting.png')
            return file

        future = self.loop.run_in_executor(None, execute, image)
        await future

        if not future.result():
            return await ctx.send('Oh No! Looks like your image cannot be drawn.')

        embed = discord.Embed(
            title="Oil Painting",
            colour=ctx.author.colour
        )
        embed.set_image(url="attachment://oilpainting.png")
        await ctx.send(file=future.result(), embed=embed)

    @commands.command(aliases=['watercolor'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def watercolour(self, ctx, *, argument: str = None):
        image = await extract_.get_stream(ctx, query=argument)

        if not image:
            return await ctx.send('Invalid image provided')

        def execute(image):
            image.seek(0)

            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.waitKey(1)

            try:
                water_colour = cv2.stylization(image, sigma_s=60, sigma_r=0.6)
            except Exception:
                return False

            with BytesIO() as buffer:
                image = Image.fromarray(water_colour)
                image.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='watercolour.png')
            return file

        future = self.loop.run_in_executor(None, execute, image)
        await future

        if not future.result():
            return await ctx.send('Oh No! Looks like your image cannot be drawn.')

        embed = discord.Embed(
            title="Watercolour Painting",
            colour=ctx.author.colour
        )
        embed.set_image(url="attachment://watercolour.png")
        return await ctx.send(file=future.result(), embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sketch(self, ctx, *, argument: str = None):
        image = await extract_.get_stream(ctx, query=argument)

        if not image:
            return await ctx.send('Invalid image provided')

        def execute(image):
            image.seek(0)

            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.waitKey(1)

            try:
                dst_gray, dst_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            except Exception:
                return False

            with BytesIO() as buffer:
                image = Image.fromarray(dst_gray)
                image.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='sketchnocolour.png')
            return file

        future = self.loop.run_in_executor(None, execute, image)
        await future

        if not future.result():
            return await ctx.send('Oh No! Looks like your image cannot be drawn.')

        embed = discord.Embed(
            title="Sketched your image",
            colour=ctx.author.colour
        )
        embed.set_image(url="attachment://sketchnocolour.png")
        return await ctx.send(file=future.result(), embed=embed)

    @sketch.command(aliases=['color'], name='colour')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def sketch_colour(self, ctx, *, argument: str = None):
        image = await extract_.get_stream(ctx, query=argument)

        if not image:
            return await ctx.send('Invalid image provided')

        def execute(image):
            image.seek(0)

            file_bytes = np.asarray(bytearray(image.read()), dtype=np.uint8)
            image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
            cv2.waitKey(1)

            try:
                dst_gray, dst_color = cv2.pencilSketch(image, sigma_s=60, sigma_r=0.07, shade_factor=0.05)
            except Exception:
                return False

            with BytesIO() as buffer:
                image = Image.fromarray(dst_color)
                image.save(buffer, format='PNG')
                buffer.seek(0)
                file = discord.File(buffer, filename='sketchcolour.png')
            return file

        future = self.loop.run_in_executor(None, execute, image)
        await future

        if not future.result():
            return await ctx.send('Oh No! Looks like your image cannot be drawn.')

        embed = discord.Embed(
            title="Sketched your image",
            colour=ctx.author.colour
        )
        embed.set_image(url="attachment://sketchcolour.png")
        return await ctx.send(file=future.result(), embed=embed)

    @commands.command()
    async def expand(self, ctx, user: discord.Member = None):
        user = user or ctx.author

        message = await ctx.send(embed=discord.Embed(description='<a:online:834143953221582927> | Building GIF',
                                                     colour=discord.Colour.green()))

        def execute(image):
            images = []

            width = 900
            center = width // 2
            color_1 = (0, 255, 0)
            background_colour = (255, 255, 255)
            max_radius = int(center * 1.5)
            step = 55

            avatar = Image.open(image).convert('RGB')

            for i in range(1, max_radius, step):
                im = Image.new('RGB', (width, width), background_colour)

                image = avatar.resize((width, width))

                npImage = np.array(image)
                h, w = im.size

                alpha = Image.new('L', image.size, 0)
                draw = ImageDraw.Draw(alpha)
                draw.pieslice((center - i, center - i, center + i, center + i), 0, 360, fill=255)

                npAlpha = np.array(alpha)
                npImage = np.dstack((npImage, npAlpha))

                image = Image.fromarray(npImage).convert('RGBA')

                im.paste(image, (0, 0), image)

                images.append(im)

            with BytesIO() as buffer:
                images[0].save(buffer, format='GIF', optimize=False, duration=150, append_images=images[1:],
                               save_all=True, quality=1, loop=0)
                buffer.seek(0)
                return discord.File(buffer, filename='expand.gif')

        image = BytesIO(await user.avatar.with_format(format='jpg').read())

        future = self.loop.run_in_executor(None, execute, image)
        await future

        gif_message = await ctx.send(file=future.result())

        return await message.edit(embed=discord.Embed(
            description='<:Done:835812226345598986> | [Message Link]({}) | [Image Link]({})'.format(
                gif_message.jump_url, gif_message.attachments[0].url),
            colour=discord.Colour.green()))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def glitch(self, ctx, argument: str = None, level: str = 'low', animated: str = '--true',
                     *size) -> typing.Union[typing.Optional[discord.Embed], discord.MessageReference]:
        image = await extract_.get_stream(ctx, query=argument)

        if not image:
            return await ctx.message.reply(content='Oh No, Looks like you passed an invalid image URL!')

        levels = {
            'low': 2,
            'medium': 5,
            'high': 10
        }
        try:
            level = levels.get(level.lower()) if level.lower() in levels else float(level)
        except Exception:
            level = 2

        if level < 0 or level > 10:
            return await ctx.send('Max level for glitching images starts at 0 and is capped at 10!')

        future = self.loop.run_in_executor(None, glitch_, image, level, animated, size)
        await future
        try:
            return await ctx.send(embed=discord.Embed(
                title='Glitch Effect',
                colour=random.randint(0x000000, 0xFFFFFF)
            ).set_image(url='attachment://glitched.gif'), file=future.result())
        except Exception:
            return await ctx.send('Oops, this level was abit too high for your image - please retry with a lower level')

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def image(self, ctx, *, query: str = None):
        if not query:
            return await ctx.send('Need to give an image to search for!')
        url = 'https://api.pexels.com/v1/search?query={}&per_page={}'.format(query, random.randint(1, 100))
        auth = '563492ad6f9170000100000106efa8d19a3a466bade44acec0b70304'
        r = requests.get(url, headers={'Authorization': auth}).json()
        try:
            await ctx.send(
                embed=discord.Embed(
                    title='Search results for {}'.format(
                        query.title()
                    ),
                    colour=discord.Color.red(),
                ).set_image(url=random.choice(r['photos'])['src']['large2x'])
            )
        except IndexError:
            return await ctx.send('No Image was Found Under the Context **{}**'.format(query.title()))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def spin(self, ctx, argument: str = None, animate: str = '--true') -> discord.Message:
        image = await extract_.get_stream(ctx, query=argument)
        if not image:
            return await ctx.send('Invalid image provided')

        future = await self.loop.run_in_executor(None, spin_, image, animate)
        return await ctx.send(embed=discord.Embed(
            title='Spun around and around',
            colour=random.randint(0x000000, 0xFFFFFF)
        ).set_image(url='attachment://spin.gif'), file=future)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def evilpatrick(self, ctx, argument: str = None) -> discord.MessageReference:
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Invalid image provided')

        def execute(stream):
            image = Image.open(stream).resize((150, 150)).convert('RGB')
            frames = []

            with BytesIO() as buffer:
                with Image.open('./storage/images/evil.gif') as _base:
                    for _ in range(_base.n_frames):
                        _base.seek(_)

                        temp = _base.copy().convert('RGBA')
                        temp.paste(image, (205, 20))

                        frames.append(temp)

                    frames[0].save(
                        buffer, 'GIF',
                        append_images=frames[1:],
                        loop=0, duration=(_base.info.get('duration') or 0),
                        save_all=True
                    )
                buffer.seek(0)
                return discord.File(fp=buffer, filename='evil.gif')
        image = await self.loop.run_in_executor(None, execute, stream)
        return await ctx.message.reply(
            embed=discord.Embed(
                title='Evil!',
                colour=discord.Colour.red()
            ).set_image(url='attachment://evil.gif'), file=image)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def salt(self, ctx, argument: str = None) -> discord.MessageReference:
        stream = await extract_.get_stream(ctx, query=argument)

        if not stream:
            return await ctx.message.reply(content='Invalid image provided')

        def execute(stream):
            image = Image.open(stream).resize((300, 300)).convert('RGB')
            frames = []

            with BytesIO() as buffer:
                with Image.open('./storage/images/salty.gif') as _base:
                    for _ in range(_base.n_frames):
                        _base.seek(_)

                        temp = _base.copy().resize((200, 200)).convert('RGBA')
                        image_ = image.copy()
                        image_.paste(temp, (120, 10), temp)

                        frames.append(image_)

                    frames[0].save(
                        buffer, 'GIF',
                        append_images=frames[1:],
                        loop=0, duration=(_base.info.get('duration') or 0),
                        save_all=True
                    )
                buffer.seek(0)
                return discord.File(fp=buffer, filename='salty.gif')
        image = await self.loop.run_in_executor(None, execute, stream)
        return await ctx.message.reply(
            embed=discord.Embed(
                title='Salty!',
                colour=discord.Colour.red()
            ).set_image(url='attachment://salty.gif'), file=image)

def setup(bot):
    bot.add_cog(_Image(bot))
