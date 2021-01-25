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
from Utils import db
import json
import datetime

class warnings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def warn(self, ctx, user: discord.Member = None, *, reason: str = None):
        if not user:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Need to provide a user to warn!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if user.top_role > ctx.author.top_role:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn members with a higher role then you!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if user == ctx.author:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn yourself!',
                colour=discord.Colour.red()
            ), mention_author=False)
        if not reason:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Need to provide a reason for the warn!',
                colour=discord.Colour.red()
            ), mention_author=False)

        action = db.record(
            'SELECT ModAction FROM guild WHERE GuildID = ?', ctx.guild.id) or (0,)
        current_warns = db.record(
            'SELECT warnings FROM guild WHERE GuildID = ?', ctx.guild.id) or (None,)
        if not current_warns[0]:
            former = {
                user.id: {
                    1: {
                        'moderator': str(ctx.author),
                        'reason': reason,
                        'warned_at': datetime.datetime.utcnow().strftime('%d/%m/%Y - %I:%M %p'),
                        'num': action[0]+1
                    }
                }
            }
            stringed = json.dumps(former)
            db.execute(
                'UPDATE guild SET warnings = ? WHERE GuildID = ?', stringed, ctx.guild.id)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> **Successfully** logged warning for {}'.format(user.mention),
                colour=discord.Colour.green()
            ))
        else:
            data = current_warns[0]
            dict_ = json.loads(data)
            if str(user.id) not in dict_:
                dict_[str(user.id)] = {
                    1: {
                        'moderator': str(ctx.author),
                        'reason': reason,
                        'warned_at': datetime.datetime.utcnow().strftime('%d/%m/%Y - %I:%M %p'),
                        'num': action[0]+1
                    }
                }
            else:
                dict_[str(user.id)][str(len(dict_[str(user.id)])+1)] = {
                    'moderator': str(ctx.author),
                    'reason': reason,
                    'warned_at': datetime.datetime.utcnow().strftime('%d/%m/%Y - %I:%M %p'),
                    'num': action[0]+1
                    }
            stringed = json.dumps(dict_)
            db.execute(
                'UPDATE guild SET warnings = ? WHERE GuildID = ?', stringed, ctx.guild.id)
            db.execute(
                'UPDATE guild SET ModAction = ? WHERE GuildID = ?', action[0]+1, ctx.guild.id)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> **Successfully** warned **{}**'.format(user),
                colour=discord.Colour.green()
            ))
        db.commit()

    @commands.command(aliases=['warns'])
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def warnings(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        warnings_ = db.record(
            'SELECT warnings FROM guild WHERE GuildID = ?', ctx.guild.id) or (None,)
        if not warnings_[0]:
            await ctx.send(embed=discord.Embed(
                description='**The user {} has no warnings.**'.format(user),
                colour=discord.Colour.red()
            ))
        else:
            dict_ = json.loads(warnings_[0])
            try:
                user_ = dict_[str(user.id)]
            except KeyError:
                return await ctx.send(embed=discord.Embed(
                    description="<a:nope:787764352387776523> The user **{}** doesn't have any warns".format(user),
                    colour=discord.Colour.red()
                ))
            warns = len(dict_[str(user.id)])
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title='📖 Logs:'.format(warns),
                timestamp=datetime.datetime.utcnow()).set_footer(
                text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            embed.set_author(icon_url=user.avatar_url, name=user)
            for i in range(len(user_)):
                reason = dict_[str(user.id)][str(i+1)]['reason']
                mod = dict_[str(user.id)][str(i+1)]['moderator']
                time = dict_[str(user.id)][str(i+1)]['warned_at']
                embed.add_field(
                    name='#{} | Warn | {}'.format(str(i+1), time),
                    value='Responsible Mod: {}\nReason: {}'.format(mod, reason), inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 15, commands.BucketType.user)
    async def delwarn(self, ctx, user: discord.Member = None, warn: str = '0'):
        if warn == '0':
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Need to provide a warn number!',
                colour=discord.Colour.red()
            ))
        try:
            warn = int(warn)
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Number provided must be a number not letters!',
                colour=discord.Colour.red()
            ))
        if not user:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Provide a member!',
                colour=discord.Colour.red()
            ))
        warns = db.record(
            'SELECT warnings FROM guild WHERE GuildID = ?', ctx.guild.id) or (None,)
        if not warns[0]:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> User doesnt have any warns!',
                colour=discord.Colour.red()
            ))
        warns = json.loads(warns[0])
        if len(warns[str(user.id)]) < warn or warn < 1:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Warn number was not found!',
                colour=discord.Colour.red()
            ))
        if user == ctx.author:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot remove your own warns!'
            ))
        del warns[str(user.id)][str(warn)]
        if len(warns[str(user.id)]) == 0:
            del warns[str(user.id)]
        stringed = json.dumps(warns)
        db.execute(
            'UPDATE guild SET warnings = ? WHERE GuildID = ?', stringed, ctx.guild.id)
        db.commit()
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Deleted warning number **{}** for user **{}**.'.format(warn, user),
            colour=discord.Colour.green()
        ))


def setup(bot):
    bot.add_cog(warnings(bot))
