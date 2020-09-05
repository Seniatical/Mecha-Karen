import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import os

class Management(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Management Cog is ready')

    @commands.command(aliases=['Management', 'Manage', 'HM', 'HelpManage'])
    @commands.has_guild_permissions(administrator=True)
    async def HelpManagement(self, ctx):
        embed = discord.Embed(
            title='Manage Mecha Karen',
            color=discord.Color.blue()
        )
        embed.add_field(name='**Cogs and Disclaimer**',
                        value='**Current Cogs:**\n*Economy*\n*ImageManipulation*\n*Images*\n*Moderation*\n*Motivation*\n*UserChecks*\n*Help*\n*Fun*\n\n**Although you can disable the help cog. It is not recommended to do so!**\n*These Cogs are case-sensitive! This issue will be resolved in the future.*')
        await ctx.send(embed=embed)
        embed = discord.Embed(
            title='Manage Mecha Karen',
            color=discord.Color.teal(),
        )
        embed.add_field(name='**Commands:**',
                        value='All Cogs are active by default\n\n`-Load {Cog Name}`: This loads the cog thats been disabled!\n\n`-Unload {Cog Name}` : This disables a cog. These cogs can be re-enabled after being disabled.\n\n*Cog name is the case-sensitive part!!!*')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Management(bot))
