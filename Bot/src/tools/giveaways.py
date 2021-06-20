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
        self.questions = (
            'Which channel would you like to set this giveaway up in?',
            'How many winners would you like for this giveaway',
            'How long will this giveaway last for? Please use the format of `<TIME>[s/m/h/d]`, default is set to seconds.',
            'Are there any requirements? If so, react to this message with corresponding emoji, all options are listed below together with their emoji.',
            'What is the prize for this giveaway?',
            'Would you like a custom emoji in place of the default option "🎉", if not simply respond with `no`. Else send the emoji below. Warning: If using a discord custom emoji, please ensure the bot is in the server that has the emoji.',
            )
        
        self.scopes = {
            'server': 1,
            'message': 2,
            'invite': 3,
            'role': 4,
            'creation-date': 5,
            'join-date': 6,
            'exit': 7,
        }

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
