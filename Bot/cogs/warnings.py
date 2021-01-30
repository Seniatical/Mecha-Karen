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
import datetime

class warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def warn(self, ctx, user: discord.Member, *, reason: str = 'Not provided.'):
        if user.top_role > ctx.author.top_role and not ctx.author == ctx.guild.owner:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn members with a higher role then you!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if user.bot:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn bots!',
                colour=discord.Colour.red()
            ), mention_author=False)     
        if user == ctx.author:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn yourself!',
                colour=discord.Colour.red()
            ), mention_author=False)

        table = self.client['Bot']
        column = table['Warns']

        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})
        if not warns:
            column.insert_one({'_id': f'{ctx.guild.id}/{user.id}', 'warnings': []})
        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})

        warns['warnings'].append({
                                'warned_at': datetime.datetime.utcnow().strftime('%d/%m/%Y - %I:%M %p'),
                                'moderator': f'{ctx.author} ({ctx.author.id})',
                                'reason': reason
        })
        column.update_one({'_id':  f'{ctx.guild.id}/{user.id}'}, {'$set': {'warnings': warns['warnings']}})

        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Successfully logged warning for {}'.format(user),
            colour=discord.Colour.red()
            ), mention_author=False)

    @commands.command(aliases=['warns'])
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def warnings(self, ctx, user: discord.Member):
        table = self.client['Bot']
        column = table['Warns']

        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})

        if not warns:
            return await ctx.send(embed=discord.Embed(
                description="<a:nope:787764352387776523> The user **{}** doesn't have any warns".format(user),
                colour=discord.Colour.red()
            ), mention_author=False)
        
        warns_ = len(warns['warnings'])
        
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title='📖 Logs:'.format(warns),
            timestamp=datetime.datetime.utcnow()).set_footer(
            text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_author(icon_url=user.avatar_url, name=user)
        
        for i in range(warns_):
            reason = warns['warnings'][i]['reason']
            mod = warns['warnings'][i]['moderator']
            time = warns['warnings'][i]['warned_at']
            embed.add_field(
                name='#{} | Warn | {}'.format(str(i+1), time),
                value='Responsible Mod: {}\nReason: {}'.format(mod, reason), inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def delwarn(self, ctx, user: discord.Member, warn: str):
        try:
            warn = int(warn)
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Number provided must be a number not letters!',
                colour=discord.Colour.red()
            ))

        table = self.client['Bot']
        column = table['Warns']
        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})

        if not warns:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> User doesnt have any warns!',
                colour=discord.Colour.red()
            ))
        try:
            warns['warnings'].pop(warn-1)
        except IndexError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Warn number not found!',
                colour=discord.Colour.red()
            ))
        if len(warns['warnings']) == 0:
            column.delete_one({'_id': f'{ctx.guild.id}/{user.id}'})
        else:
            column.update_one({'_id': f'{ctx.guild.id}/{user.id}'}, {'$set': {'warnings': warns['warnings']}})
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.green(),
            description='<a:Passed:757652583392215201> Removed warn #{} for user **{}**'.format(warn, user)
            ))
        
def setup(bot):
    bot.add_cog(warnings(bot))
