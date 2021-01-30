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
from Utils.FORMERS import star, create_embed

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = self.bot.client
        self.table = self.client['Bot']
        self.column = self.table['Starboard']
        self.guild = self.table['Guilds']

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global count
        if payload.emoji.name == '⭐':
            channel = self.guild.find_one({'_id': payload.guild_id})['StarChannel']
            if not channel:
                return
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if payload.member.id == message.author.id or message.author.bot or channel == payload.channel_id:
                return await message.remove_reaction(payload.emoji, payload.member)
            star_message = self.column.find_one({'_id': f'{payload.guild_id}/{payload.message_id}'})
            star_limit = self.guild.find_one({'_id': payload.guild_id})['StarCount'] or 0
            for reaction in message.reactions:
                if reaction.emoji == '⭐':
                    count = reaction.count
                    break
                
            if count < star_limit:
                return
            
            star_channel = self.bot.get_channel(channel)
            embed, mes = create_embed(message, count)
            
            if not star_message:
                try:
                    star_mes = await star_channel.send(content=mes, embed=embed)
                except discord.errors.HTTPException:
                    embed = discord.Embed(description='[Original Message]({})'.format(message.jump_url), colour=discord.Colour.red()).set_author(icon_url=message.author.avatar_url, name=message.author)
                    embed.set_footer(text='Missing Field, Cannot Load Original Message!', icon_url=self.bot.user.avatar_url)
                    star_mes = await star_channel.send(embed=embed, content=mes)
                self.column.insert_one({'_id': f'{payload.guild_id}/{payload.message_id}', 'MessageID': payload.message_id})
                
            else:
                star_message = await star_channel.fetch_message(star_message['MessageID'])
                if not star_message:
                    self.column.delete_one({'_id': f'{payload.guild_id}/{payload.message_id}'})
                try:
                    await star_message.edit(content=mes, embed=embed)
                except discord.errors.HTTPException:
                    embed = discord.Embed(description='[Original Message]({})'.format(message.jump_url), colour=discord.Colour.red()).set_author(icon_url=message.author.avatar_url, name=message.author)
                    embed.set_footer(text='Missing Field, Cannot Load Original Message!', icon_url=self.bot.user.avatar_url)
                    await star_message.edit(embed=embed, content=mes)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def setboard(self, ctx, channel: discord.TextChannel):
        self.guild.update_one({'_id': ctx.guild.id}, {'$set': {'StarChannel': channel.id}})
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> New Starboard has been set for {}'.format(channel.mention),
            colour=discord.Colour.green()
        ))

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def setstarlimit(self, ctx, count_: str):
        try:
            count_ = int(count_)
        except ValueError:
            ctx.command.reset_command(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Star limit must be a number not letters!',
                colour=discord.Colour.red()
            ))
        if count_ < 0:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Star limit cannot be less than 0!'
            ))
        self.guild.update_one({'_id': ctx.guild.id}, {'$set': {'StarCount': count_}})
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> New Starboard limit is {}.'.format(count_),
            colour=discord.Colour.green()
        ))

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def starboard(self, ctx):
        data = self.guild.find_one({'_id': ctx.guild_id})
        channel = data['StarChannel']
        star_lim = data['StarCount']
        
        if isinstance(channel, int):
            channel_ = self.bot.get_channel(channel)
            if not channel_:
                channel_ = 'Not Set'
        else:
            channel_ = 'Not Set'
        status = 'Status: Active <:4941_online:787764205256310825>' if channel_ != 'Not Set' else 'Status: Inactive <:offline:787764149706031104>'
        colour = discord.Colour.green() if channel_ != 'Not Set' else discord.Colour.red()
        embed = discord.Embed(
            title=status,
            colour=colour,
            timestamp=ctx.message.created_at).set_footer(text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name='Channel:', value=channel_.mention if channel_ != 'Not Set' else channel_)
        embed.add_field(name='Star Limit:', value='**{}**'.format('1' if not star_lim else star_lim))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(starboard(bot))
