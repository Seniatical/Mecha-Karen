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

## NOTE: need to finish this section

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
