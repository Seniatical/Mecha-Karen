import discord
from discord.ext import commands
import datetime
import datetime
import os
from binascii import hexlify

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client

        self.table = self.client['Giveaways']
        self.codes = self.table['codes']

        self.giveaways = {}

        for guild in bot.guilds:
            self.giveaways[guild.id] = {}

        bot.loop.create_task(self.load_giveaways())

    async def load_giveaways(self):
        for cached in self.codes.find():
            self.giveaways.update({
                int(cached['guild']): {
                    'code': cached['_id'],
                    'ending': cached['ending'],
                    'started': cached['starting'],
                    'message': cached['message'],
                    'channel': cached['channel']
                }})
                

    def gen_new_code(self, column):
        codes = [code['_id'] for code in self.codes.find()]
        code = hexlify(os.urandom(7)).decode()
        while code not in codes:
            code = hexlify(os.urandom(7)).decode()

        return code

def setup(bot):
    bot.add_cog(Giveaway(bot))
