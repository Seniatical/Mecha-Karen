import discord
from discord.ext import commands
import aiohttp
import time
import random
from Utils import Truncater, Truncate.convert

class Truncate(Truncater):
    def __init__(self, object):
        self.object = object
        super().__init__(
            const='__import__("discord.py").ext.commands.Bot',
            form=dict
        )
        
    @convert
    async def start(self):
        super().start(self.object)

class Cache_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.container = bot.cache
        self.session = aiohttp.ClientSession()
        self.converter = commands.MemberConverter()
        self.trunc = Truncate(bot.cache)
        
    @commands.Cog.listener()
    async def on_ready(self):
        try:
            await self.trunc.start()
        except Truncater.errors.CLOGGED as launch_error:
            raise launch_error
        
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cache(self, ctx, category: str = 'image', slot: str = '1', user: discord.Member = None):
        start = time.time()
        if category.lower() not in ['image', 'message', 'user', 'quote']:
            return await ctx.send(embed=discord.Embed(
                description = '<a:nope:787764352387776523> | Invalid category provided, please choose from `IMAGE`, `MESSAGE`, `USER`, `QUOTE`',
                colour=discord.Colour.red()
                ))
        try:
            if slot == 'all':
                slot = 0
            slot = int(slot)
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                description = '<a:nope:787764352387776523> | Slot must be a number not a string',
                colour=discord.Colour.red()
                ))
        user = user or ctx.author
        category = (category.lower() + 's')
        data = (await self.container.get_value(ctx.author.id))[category]
        embed = discord.Embed(colour=user.colour, title=f'{category[:-1]} Cache:')
        if not data:
            embed.description = 'This cache slot is currently empty, add more to it by using command:\n`-cache set <category> [slot]`'
            return await ctx.send(embed=embed)
        if category == 'images':
            if slot != 0:
                try:
                    set = data[slot - 1]
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description = '<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                        ))
        
                url = set['url']
                filename = set['filename'] or url.split('/')[-1].split('?')[0]

                check = await self.session.get(url)
                if check.status != 200:
                    embed.description = 'Your image that is being stored is no longer usable.\nPlease consider using `-cache remove image {}`'.format(slot)
                    embed.add_field('Image Status', value='**Failing**, returned status code **{}**'.format(check.status))
                else:
                    embed.url = url
                    embed.description = f'Your image was found in my internal cache taking a total time of **{round(time.time() - start, 5)}**s'
                    embed.add_field(name='Filename', value=filename)
                    embed.set_image(url=url)
                    embed.set_footer(text='Slot Num: #{} | Queue ID: #{}'.format(slot, random.randint(0x000000, 0xFFFFFF)))
                return await ctx.send(embed=embed)

            temp = []
            for set in data:
                url = set['url']
                filename = set['filename'] or url.split('/')[-1].split('?')[0]
                is_valid = await self.session.get(url)
                if is_valid.status != 200:
                    message = f'Image status is currently **failing**, returning a status code of **{is_valid.status}**'
                else:
                    message = f'Image status is currently **OK**, returning a status code of **{is_valid.status}** taking **{round(time.time() - start, 5)}**s to complete'
                msg = '[{}]({})\n{}'.format(filename, url, message)
                temp.append(msg)
            embed.description = '\n\n'.join(temp)
            await ctx.send(embed = embed)
        else:
            return await ctx.send('Coming soon!')

    @cache.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def set(self, ctx, object: str, category: str = 'image', slot: str = 'new'):
        shortened = object[:1024]
        start = time.time()
        
        if category.lower() not in ['image', 'message', 'user', 'quote']:
            return await ctx.send(embed=discord.Embed(
                description = '<a:nope:787764352387776523> | Invalid category provided, please choose from `IMAGE`, `MESSAGE`, `USER`, `QUOTE`',
                colour=discord.Colour.red()
                ))
        slot = slot.lower()
        if slot != 'new':
            try:
                slot = int(slot)
            except ValueError:
                return await ctx.send(embed=discord.Embed(
                    description = '<a:nope:787764352387776523> | Slot number must be a number not a string',
                    colour=discord.Colour.red()
                    ))
        
        if category.lower() == 'image':
            category = (category + 's')
            data = (await self.container.get_value(ctx.author.id))[category]
            
            try:
                user = await self.converter.convert(ctx, object)
                object = str(user.avatar_url)
            except Exception:
                pass
            
            if ctx.message.attachments:
                object = ctx.message.attachments[0].url
            
            try:
                check = await self.session.get(object)
                await check.read()
            except Exception:
                return await ctx.send(embed=discord.Embed(
                    description = '<a:nope:787764352387776523> | Image URL not found',
                    colour=discord.Colour.red()
                    ))

            if slot == 'new':
                data.append({'url': object, 'filename': None})
            else:
                try:
                    data[slot - 1] = {'url': object, 'filename': None}
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description = '<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                        ))
            await self.container.update_cache(ctx.author.id, data, 0)
                
            return await ctx.send(embed=discord.Embed(
                title = 'New Image Added:',
                url = object,
                colour = discord.Colour.green()
                ).set_image(url=object))
        else:
            return await ctx.send('Coming soon!')

    @cache.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def remove(self, ctx, category: str, slot: str):
        slot = slot.lower()
        if category.lower() not in ['image', 'message', 'user', 'quote']:
            return await ctx.send(embed=discord.Embed(
                description = '<a:nope:787764352387776523> | Invalid category provided, please choose from `IMAGE`, `MESSAGE`, `USER`, `QUOTE`',
                colour=discord.Colour.red()
                ))
        embed = discord.Embed(title='Removed from cache', colour=discord.Colour.green())
        if category.lower() == 'image':
            category = (category.lower() + 's')
            data = (await self.container.get_value(ctx.author.id))[category]
            if slot == 'all':
                for i in range((len(data) - 1)):
                    data = []
                embed.description = f'Cleared {category[:-1].title()} cache'
            else:
                try:
                    slot = int(slot)
                except ValueError:
                    return await ctx.send(embed=discord.Embed(
                        description = '<a:nope:787764352387776523> | Slot number must be a number not a string',
                        colour=discord.Colour.red()
                        ))
                try:
                    previous = data.pop((slot - 1))
                    embed.description = 'Cleared [{}]({}) from the image cache'.format((previous['filename'] or previous['url'].split('/')[-1].split('?')[0]), previous['url'])
                except IndexError:
                    return await ctx.send(embed=discord.Embed(
                        description = '<a:nope:787764352387776523> | Slot number not found',
                        colour=discord.Colour.red()
                        ))
            await self.container.update_cache(ctx.author.id, data, 0)
            return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Cache_Commands(bot))
