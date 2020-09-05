import discord
from discord.ext import commands
from discord import utils
import asyncio

class Tests(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Tests cog is ready')

    @commands.command()
    async def new(self, ctx):
        msg = discord.Embed(title='Pleb', color=discord.Color.red(), description='Hello')
        await ctx.send(msg)

def setup(bot):
    bot.add_cog(Tests(bot))
