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
import aiohttp
import time
import random
import json
from core._ import extract_

class Cache_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.container = bot.cache
        self.session = aiohttp.ClientSession()

        self.converter = commands.MemberConverter()
        self.message_c = commands.MessageConverter()
        self.channel_c = commands.TextChannelConverter()
        self.emoji_c = commands.PartialEmojiConverter()

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cache(self, ctx, category: str = 'image', slot: str = '1', user: discord.Member = None):
        start = time.time()
        if category.lower() not in ['image', 'message', 'user', 'quote']:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> | Invalid category provided, please choose from `IMAGE`, `MESSAGE`, `USER`, `QUOTE`',
                colour=discord.Colour.red()
            ))
        try:
            if slot == 'all':
                slot = 0
            slot = int(slot)
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> | Slot must be a number not a string',
                colour=discord.Colour.red()
            ))
        user = user or ctx.author
        category = (category.lower() + 's')
        data = (await self.container.get_value(user.id))[category]
        embed = discord.Embed(colour=user.colour, title=f'{category[:-1]} Cache:')

        if not data:
            embed.description = 'This cache slot is currently empty, add more to it by using command:\n`-cache set <object> [category] [slot]`'
            return await ctx.send(embed=embed)
        if category == 'images':
            if slot != 0:
                try:
                    _set = data[slot - 1]
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                    ))

                url = _set['url']
                filename = _set['filename'] or url.split('/')[-1].split('?')[0]

                check = await self.session.get(url)
                if check.status != 200:
                    embed.description = 'Your image that is being stored is no longer usable.\nPlease consider using `-cache remove image {}`'.format(
                        slot)
                    embed.add_field('Image Status',
                                    value='**Failing**, returned status code **{}**'.format(check.status))
                else:
                    embed.url = url
                    embed.description = f'Your image was found in my internal cache taking a total time of **{round(time.time() - start, 5)}**s'
                    embed.add_field(name='Filename', value=filename)
                    embed.set_image(url=url)
                    embed.set_footer(
                        text='Slot Num: #{} | Queue ID: #{}'.format(slot, random.randint(0x000000, 0xFFFFFF)))
                return await ctx.send(embed=embed)

            temp = []
            for _set in data:
                url = _set['url']
                filename = _set['filename'] or url.split('/')[-1].split('?')[0]
                is_valid = await self.session.get(url)
                if is_valid.status != 200:
                    message = f'Image status is currently **failing**, returning a status code of **{is_valid.status}**'
                else:
                    message = f'Image status is currently **OK**, returning a status code of **{is_valid.status}** taking **{round(time.time() - start, 5)}**s to complete'
                msg = '[{}]({})\n{}'.format(filename, url, message)
                temp.append(msg)
            embed.description = '\n\n'.join(temp)
            await ctx.send(embed=embed)

        elif category == 'messages':
            if slot != 0:
                try:
                    _set = data[slot - 1]
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                    ))
                channel = self.bot.get_channel(_set['channel'])
                if not channel:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | This message\'s channel can no longer be found',
                        colour=discord.Colour.red()
                    ))
                try:
                    message = await channel.fetch_message(_set['id'])
                except (discord.errors.NotFound, discord.errors.Forbidden, discord.errors.HTTPException):
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | This message can no longer be found',
                        colour=discord.Colour.red()
                    ))
                embed = discord.Embed(colour=message.author.colour)
                embed.set_author(name=message.author, icon_url=message.author.avatar)
                embed.set_footer(text='Message sent in {}'.format(message.guild))
                embed.timestamp = message.created_at

                embed.add_field(name='Jump', value='[Click here]({})\n'.format(message.jump_url))

                if message.content:
                    embed.description = message.content[:1000]

                ## if message.stickers:
                ## file = discord.File(fp=await (message.stickers[0].image_url).read(), filename='sticker.png')
                ## embed.set_image(url='')

                if message.attachments:
                    if message.attachments[0].url.split('.')[-1] in ['gif', 'png', 'jpg', 'jpeg',
                                                                     'webp'] and not message.stickers:
                        embed.set_image(url=message.attachments[0].url)

                if message.embeds:
                    embed = message.embeds[0]
                    _dict = embed.to_dict()
                    form = json.dumps(_dict, indent=4)
                    embed.add_field(name='Embed', value=('```json\n' + form + '\n```'))

                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(colour=ctx.author.colour)
                for _set in data:
                    channel = self.bot.get_channel(_set['channel'])
                    if not channel:
                        embed.add_field(name='{}. Failing'.format((data.index(_set) + 1)),
                                        value='Cannot locate the message\'s channel', inline=False)
                        continue
                    try:
                        message = await channel.fetch_message(_set['id'])
                    except (discord.errors.NotFound, discord.errors.Forbidden, discord.errors.HTTPException):
                        embed.add_field(name='{}. Failing'.format((data.index(_set) + 1)),
                                        value='Cannot locate the message', inline=False)
                        continue
                    embed.add_field(name='{}. {}'.format((data.index(_set) + 1), message.guild),
                                    value=f'[Click here]({message.jump_url})', inline=False)
                await ctx.send(embed=embed)

        else:
            return await ctx.send('Coming soon!')

    @cache.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def set(self, ctx, _object: str, category: str = 'image', slot: str = 'new'):

        if category.lower() not in ['image', 'message', 'user', 'quote']:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> | Invalid category provided, please choose from `IMAGE`, `MESSAGE`, `USER`, `QUOTE`',
                colour=discord.Colour.red()
            ))
        slot = slot.lower()
        if slot != 'new':
            try:
                slot = int(slot)
            except ValueError:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> | Slot number must be a number not a string',
                    colour=discord.Colour.red()
                ))

        if category.lower() == 'image':
            category = (category + 's')
            data = (await self.container.get_value(ctx.author.id))[category]

            _object = str(await extract_.get_url(ctx, query=_object))

            if not _object:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> | Image URL not found',
                    colour=discord.Colour.red()
                ))

            if slot == 'new':
                data.append({'url': _object, 'filename': None})
            else:
                try:
                    data[slot - 1] = {'url': _object, 'filename': None}
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                    ))
            await self.container.update_cache(ctx.author.id, data, 0)

            return await ctx.send(embed=discord.Embed(
                title='New Image Added:',
                url=_object,
                colour=discord.Colour.green()
            ).set_image(url=_object))

        elif category.lower() == 'message':
            category = (category + 's')
            data = (await self.container.get_value(ctx.author.id))[category]
            try:
                channel, message = _object.split('/')
            except ValueError:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> | Please use the format `CHANNEL/MESSAGE`',
                    colour=discord.Colour.red()
                ))

            try:
                channel = await self.channel_c.convert(ctx, channel)
            except Exception:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> | Channel not found',
                    colour=discord.Colour.red()
                ))

            try:
                message = await self.message_c.convert(ctx, message)
            except Exception:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> | Message not found',
                    colour=discord.Colour.red()
                ))

            slot = slot.lower()
            if slot != 'new':
                try:
                    slot = int(slot)
                except ValueError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number must be a number not a string',
                        colour=discord.Colour.red()
                    ))

            if slot == 'new':
                data.append({'channel': channel.id, 'id': message.id})
            else:
                try:
                    data[slot - 1] = {'channel': channel.id, 'id': message.id}
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                    ))
            await self.container.update_cache(ctx.author.id, data, 1)

            return await ctx.send(embed=discord.Embed(
                description='Added new [Message]({}) to your cache'.format(message.jump_url),
                colour=discord.Colour.green()
            ))

        else:
            return await ctx.send('Coming soon!')

    @cache.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remove(self, ctx, category: str, slot: str):
        slot = slot.lower()
        if category.lower() not in ['image', 'message', 'user', 'quote']:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> | Invalid category provided, please choose from `IMAGE`, `MESSAGE`, `USER`, `QUOTE`',
                colour=discord.Colour.red()
            ))
        embed = discord.Embed(title='Removed from cache', colour=discord.Colour.green())
        if category.lower() == 'image':
            category = (category.lower() + 's')
            data = (await self.container.get_value(ctx.author.id))[category]
            if slot == 'all':
                for i in range((len(data) - 1)):
                    data.pop(i)
                embed.description = f'Cleared {category[:-1].title()} cache'
            else:
                try:
                    slot = int(slot)
                except ValueError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number must be a number not a string',
                        colour=discord.Colour.red()
                    ))
                try:
                    previous = data.pop((slot - 1))
                    embed.description = 'Cleared [{}]({}) from the image cache'.format(
                        (previous['filename'] or previous['url'].split('/')[-1].split('?')[0]), previous['url'])
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                    ))
            await self.container.update_cache(ctx.author.id, data, 0)
            return await ctx.send(embed=embed)

        elif category.lower() == 'message':
            category = (category.lower() + 's')
            data = (await self.container.get_value(ctx.author.id))[category]
            embed = discord.Embed(colour=discord.Colour.green())
            if slot == 'all':
                for i in range((len(data) - 1)):
                    data.pop(i)
                embed.description = f'Cleared {category[:-1].title()} cache'
            else:
                try:
                    slot = int(slot)
                except ValueError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number must be a number not a string',
                        colour=discord.Colour.red()
                    ))
                try:
                    data.pop((slot - 1))
                    embed.description = 'Cleared this message from the image cache'
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                    ))
            await self.container.update_cache(ctx.author.id, data, 1)
            return await ctx.send(embed=embed)

        else:
            await ctx.send('Coming soon!')


def setup(bot):
    bot.add_cog(Cache_Commands(bot))
