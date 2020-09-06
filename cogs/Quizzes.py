import time

import discord
from discord.ext import commands


class Quizzes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Quizzes Cog is ready')

    '''
    This section is under completion.
    Wait your asses.
    '''

def setup(bot):
    bot.add_cog(Quizzes(bot))
