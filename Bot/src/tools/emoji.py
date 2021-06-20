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
from io import BytesIO
import datetime

class Emoji(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def enlarge(self, ctx, emoji: str):
        try:
            _id = emoji.split(':')[-1][:-1]
        except IndexError:
            return await ctx.send('Invalid emoji provided')
        endpoint = 'https://cdn.discordapp.com/emojis/'
        try:
            endpoint += '{}.{}?v=1'.format(_id, 'png' if emoji[1].lower() != 'a' else 'gif')
        except IndexError:
            return await ctx.send('Invalid emoji provided')
        try:
            embed = discord.Embed(title=emoji.split(':')[-2], url=endpoint, colour=discord.Colour.green())
        except IndexError:
            return await ctx.send('Invalid emoji provided')
        embed.set_image(url=endpoint)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_emojis=True)
    @commands.has_guild_permissions(manage_emojis=True)
    async def steal(self, ctx, emoji: str = None, *, name: str = None):
        message = ctx.message
        
        if len(ctx.guild.emojis) == ctx.guild.emoji_limit:
            return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> You have reached the maximum allowance for emojis!', colour=discord.Colour.red()))
        
        if not message.attachments and not emoji:
            return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Need to give an emoji to add', colour=discord.Colour.red()))

        if message.attachments:
            if not emoji:
                return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Need to give a name for your emoji', colour=discord.Colour.red()))
                
            url = message.attachments[0].url
            try:
                data = await (await self.session.get(url)).read()
            except Exception:
                return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Invalid attachment provided', colour=discord.Colour.red()))
            try:
                cxn = await ctx.guild.create_custom_emoji(name=emoji[:32], image=data, reason=f'{ctx.author} has used the steal command')
            except Exception:
                return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Image was too large. Maximum filesize for emojis is 256.0 kb!', colour=discord.Colour.red()))

        else:
            try:
                _id = int(emoji.split(':')[-1][:-1])
                endpoint = 'https://cdn.discordapp.com/emojis/'
                endpoint += '{}.{}?v=1'.format(_id, 'png' if emoji[1].lower() != 'a' else 'gif')
                name = name or emoji.split(':')[-2]
                data = await (await self.session.get(endpoint)).read()
                
            except ValueError:
                try:
                    data = await (await self.session.get(emoji)).read()
                except Exception:
                    return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Invalid Image URL provided', colour=discord.Colour.red()))
                if not name:
                    return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Need to provide a name for your emoji', colour=discord.Colour.red()))

            try:
                cxn = await ctx.guild.create_custom_emoji(name=name[:32].replace(' ', '_'), image=data, reason=f'{ctx.author} has used the steal command')
            except Exception:
                return await ctx.send(embed=discord.Embed(description='<a:nope:787764352387776523> Image was too large. Maximum filesize for emojis is 256.0 kb!', colour=discord.Colour.red()))
                
        await ctx.send(embed=discord.Embed(description=f'{cxn} | New [emoji]({cxn.url}) created using the name `:{cxn.name}:`', colour=discord.Colour.green()))
        
def setup(bot):
    bot.add_cog(Emoji(bot))
