import discord
from discord.ext import commands
import os
import subprocess
import re

class Usage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Usage Cog is ready!')

def setup(bot):
    bot.add_cog(Usage(bot))
