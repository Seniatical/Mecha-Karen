import time

import discord
from discord.ext import commands


class Quizzes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Quizzes Cog is ready')

    @commands.command()
    async def Take(self, ctx, name=None):
        quiz =['test', 'bingo', 'cash', 'fail']
        counter = 0
        if name == None:
            await ctx.send('Enter a quiz idiot')
        else:
            msg = await ctx.send(f'Starting Process')
            for counter in range(5):
                counter += 1
                start = time.perf_counter()
                await msg.edit(content=f"Searching for quiz named {name}... {counter}/5")
                end = time.perf_counter()
            if 'test' in quiz == True:
                await ctx.send(f'Quiz {name} has been found')
            else:
                await ctx.send(f'Quiz {name} doesnt exist')



def setup(bot):
    bot.add_cog(Quizzes(bot))
