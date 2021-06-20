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
import json
import os
import inspect
import datetime
from ast import literal_eval

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
        self.client = self.bot.client
        self.disabled = \
            ['remove', 'allow', 'help', 'prefix', 'change_prefix', 'cp', 'suggest', 'report',
             'refresh', 'sync', 'enable', 'disable', 'blacklist', 'unblacklist', 'blacklists']

    @commands.group(invoke_without_command=True, aliases=['prefixes'])
    @commands.cooldown(1, 10, commands.BucketType.channel)
    async def prefix(self, ctx) -> discord.Message:
        prefixes = (await self.bot.prefix(self.bot, ctx.message)).prefixes
        embed = discord.Embed(title='Prefixes', colour=discord.Colour.red())

        if prefixes[0] == '<@740514706858442792> ':
            prefixes.pop(0)
        description = []

        for i in range(len(prefixes)):
            description.append('**{}. {}**'.format((i + 1), prefixes[i]))
        embed.description = '\n\n'.join(description)

        await ctx.message.reply(embed=embed)
            
    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    async def disable(self, ctx, command: str):
        command_ = [i for i in self.bot.commands if i.name.lower() == command.lower()]

        if not command_:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Command **{}** not found!'.format(command),
                colour=discord.Colour.red()
            ), mention_author=False)
        if command_[0].name.lower() in self.disabled:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Command **{}** cannot be disabled!'.format(command),
                colour=discord.Colour.red()
            ), mention_author=False)

        client_handler = self.bot.client
        command_ = command_[0]
        table = client_handler['Bot']
        column = table['Guilds']

        data = column.find_one({'_id': ctx.guild.id})
        if command_.name.lower() in data['Disabled']:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Command **{}** is already disabled!'.format(command),
                colour=discord.Colour.red()
            ), mention_author=False)
        data['Disabled'].append(command_.name.lower())
        column.update_one({'_id': ctx.guild.id}, {'$set': {'Disabled': data['Disabled']}})
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Command **{}** has been disabled'.format(command_.name),
            colour=discord.Colour.red()
        ))

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    async def enable(self, ctx, command: str):
        command_ = [i for i in self.bot.commands if i.name.lower() == command.lower()]

        if not command_:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Command **{}** not found!'.format(command),
                colour=discord.Colour.red()
            ), mention_author=False)
        if command_[0].name.lower() in self.disabled:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Command **{}** not found!'.format(command),
                colour=discord.Colour.red()
            ), mention_author=False)

        client_handler = self.bot.client
        command_ = command_[0]
        table = client_handler['Bot']
        column = table['Guilds']
        data = column.find_one({'_id': ctx.guild.id})
        if command_.name.lower() not in data['Disabled']:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Command **{}** is already enabled!'.format(command),
                colour=discord.Colour.red()
            ), mention_author=False)
        data['Disabled'].pop(data['Disabled'].index(command_.name.lower()))
        column.update_one({'_id': ctx.guild.id}, {'$set': {'Disabled': data['Disabled']}})
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Command **{}** has been enabled'.format(command_.name),
            colour=discord.Colour.red()
        ))

    @commands.command(help='Track how long **Mecha Karen** has been online for.\n**Usage:**\n```\n-Uptime\n```')
    @commands.cooldown(1, 10, BucketType.user)
    async def uptime(self, ctx):
        delta_uptime = datetime.datetime.utcnow() - self.bot.launch_time
        total = delta_uptime.total_seconds()
        weeks = total // 604800
        total %= 604800
        days = total // 86400
        total %= 86400
        hours = total // 3600
        total %= 3600
        mins = total // 60

        shard = self.bot.get_shard(ctx.guild.shard_id)
        cluster = [i for i in self.bot.shards if self.bot.shards[i].id == ctx.guild.shard_id][0]
        latency = round((shard.latency * 1000))
        
        embed = discord.Embed(title="Uptime:", description=f"**{int(weeks)}** weeks, **{int(days)}** days, **{int(hours)}** hours and **{int(mins)}** minutes", color=discord.Colour.red())
        embed.add_field(name='Shard Info:', value=f'Cluster **{cluster}** has latency of `{latency} ms` with a shard count of **{shard.shard_count}**')
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Management(bot))
