import discord
from discord.ext import commands

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client
        
        self.cache = bot.cache
        
        if not self.cache.cache.get('suggestions'):
            self.cache.cache.update({'suggestions': {}})
            print('Created New Sub-branch - CACHE[HELPERS] | Suggestions .. suggestions')

        bot.loop.create_task(self.update_cache())

    async def update_cache():
        ## group = await self.bot.loop.run_in_executor(None, lambda: self.client.find())
        pass
        
def setup(bot):
    pass