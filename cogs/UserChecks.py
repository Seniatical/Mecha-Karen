import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
import datetime
from discord.utils import escape_markdown
import time
import psutil
import random

class UserChecks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('User_Checks Cog is ready')

    @commands.command(aliases=['info', 'whois', 'Userinfo'])
    @cooldown(1, 3, BucketType.user)
    async def user(self, ctx, member: discord.Member):
        roles = [role for role in member.roles]
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name='Registered at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p'))
        embed.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
        embed.add_field(name='Bot?', value=f'{member.bot}')
        embed.add_field(name='Status?', value=f'{member.status}')
        embed.add_field(name='Top Role?', value=f'{member.top_role}')
        embed.add_field(name='Admin?', value=f'{member.guild_permissions.administrator}')
        embed.add_field(name='Mobile?', value=f'{member.is_on_mobile()}')
        embed.add_field(name='Name?', value=f'{member.display_name}')
        embed.add_field(name='VC?', value=f'{member.voice}')
        embed.add_field(name='Color?', value=f'{member.color}')
        embed.add_field(name='Original Avatar Color?', value=f'{member.default_avatar}')
        embed.add_field(name=f"Roles ({len(roles)})", value=" ".join([role.mention for role in roles]))
        embed.set_footer(icon_url=member.avatar_url,
                         text=f'ID: {member.id}\nRequested By: {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['avatar'])
    @cooldown(1, 3, BucketType.user)
    async def av(self, ctx, member: discord.Member):
        user = ctx.author
        embed = discord.Embed(
            title=f"{member}'s avatar",
            color=member.color, timestamp=datetime.datetime.utcnow(),
        )
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f'Requested by: {user}')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def server(self, ctx):
        roles = [role for role in ctx.author.guild.roles]
        embed = discord.Embed(
            title='Server Info',
            color= discord.Color.blue(), timestamp=datetime.datetime.utcnow()
        )
        embed.set_thumbnail(url=ctx.author.guild.icon_url)
        embed.set_author(name=ctx.author.guild.name)
        embed.add_field(name='Owner?', value=f'{ctx.author.guild.owner}')
        embed.add_field(name='Created At?', value=f"{ctx.author.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p')}")
        embed.add_field(name='Region?', value=f'{ctx.author.guild.region}')
        embed.add_field(name="Emoji's?", value=f'{len(ctx.author.guild.emojis)}')
        embed.add_field(name='Channels?', value=f'{len(ctx.author.guild.channels)}')
        embed.add_field(name='Roles?', value=f'{len(roles)}')
        embed.add_field(name='Members?', value=f'{len(ctx.author.guild.members)}')
        embed.add_field(name='Presences?', value=f'{ctx.author.guild.max_presences}')
        embed.add_field(name='Verification Level?', value=f'{ctx.author.guild.verification_level}')
        embed.add_field(name='AFK Channel?', value=f'{ctx.author.guild.afk_channel}')
        embed.add_field(name='Boosts?', value=f'{ctx.author.guild.premium_subscription_count}')
        embed.set_footer(text=f'Server ID: {ctx.author.guild.id}\nRequested By: {ctx.author}')
        await ctx.send(embed=embed)

    @commands.command()
    async def history(self, ctx):
        limit = 2147483646
        counter = 0
        async for message in ctx.channel.history(limit=limit):
            if message.author == self.bot.user:
                counter += 1
                if counter == limit:
                    await ctx.send('Your channel History is to Large!')
                else:
                    pass
        await ctx.send(counter)

def setup(bot):
    bot.add_cog(UserChecks(bot))
