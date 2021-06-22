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
from discord.ext.commands import (
    Context,
    EmojiConverter,
    MemberConverter,

    MemberNotFound,
    EmojiNotFound
)
import typing
from io import BytesIO

EmojiConverter = EmojiConverter()
MemberConverter = MemberConverter()

cache = None
session = None

content_types = (
    'image/gif',
    'image/png',
    'image/jpg',
    'image/jpeg'
)

async def get_url(ctx: Context, **optional) -> typing.Union[str, typing.Optional[discord.Message], typing.Optional[bool]]:
    raw: str = optional.get('param') or optional.get('query')

    if raw:
        if raw.lower() == 'sample':
            return 'https://media1.tenor.com/images/505e4a6c227a15e7d3a813354d3229f4/tenor.gif?itemid=4520105'
        if raw.lower() == 'icon':
            return ctx.guild.icon
        if raw.lower() == 'karen':
            return ctx.me.avatar

    message: discord.Message = ctx.message
    url: str = ''

    if not raw:
        message: typing.Optional[discord.Message] = getattr(message.reference, 'resolved', None)

        if message:
            try:
                embed: discord.Embed = message.embeds[0]
            except IndexError:
                embed: discord.Embed = None

            if message.attachments:
                attachment: discord.Attachment = message.attachments[0]

                url = attachment.url

                if not url.endswith(('.png', '.jpg', '.gif', '.jpeg')):
                    url = ''

            if embed and not url:
                url: str = embed.image.url
                if url == discord.Embed.Empty:
                    url = embed.thumbnail.url
                if url == discord.Embed.Empty:
                    url = embed.author.icon_url
                if url == discord.Embed.Empty:
                    url = embed.footer.icon_url

    else:
        try:
            user: discord.Member = await MemberConverter.convert(ctx=ctx, argument=raw)
            url = user.avatar
        except MemberNotFound:
            try:
                emoji: discord.Emoji = await EmojiConverter.convert(ctx=ctx, argument=raw)
                url = emoji.url
            except EmojiNotFound:
                try:
                    attachment: discord.Attachment = message.attachments[0]
                    url = attachment.url

                    if not url.endswith(('.png', '.jpg', '.gif', '.jpeg')):
                        url = ''

                except IndexError:
                    try:
                        response = await session.get(raw)
                        if response.content_type in content_types:
                            url = raw
                    except Exception:
                        if raw.lower().startswith('from cache'):
                            check = ctx.bot.cache.cache.get(ctx.author.id)
                            if not check:
                                return ctx.author.avatar

                            images = check.get('images')
                            if not images:
                                return ctx.author.avatar

                            try:
                                to_choose = images[int(raw.split()[-1])]
                            except (ValueError, IndexError):
                                to_choose = images[0]
                            url = to_choose['url']

    return url or ctx.author.avatar

async def get_stream(ctx: Context, **options) -> typing.Optional[BytesIO]:
    image = await get_url(ctx=ctx, **options)

    try:
        if type(image) == discord.Asset:
            _ = await image.read()
        else:
            response = await session.get(image)

            if response.content_type not in content_types:
                return None

            _ = await response.read()

        stream = BytesIO(_)


        discord_cdn = ('https://cdn.discordapp.com/avatars', 'https://cdn.discordapp.com/')
        if str(image).startswith(discord_cdn):
            stream.discord = True
    except Exception:
        stream = None

    return stream
