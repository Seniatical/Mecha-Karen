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

from discord.ext.commands import when_mentioned_or

class Prefix:
    def __init__(self, prefixes, *, mention: bool = True):
        self.prefixes = prefixes
        self.mention = mention

    def __iter__(self):
        if not type(self.prefixes) == list:
            self.prefixes = [self.prefixes]

        return iter(self.prefixes)

class PrefixHandler:
    def __init__(self, column):
        self.column = column
        self.cache = {}
        self.guild_data = {
            '_id': str(), 'prefix': '-', 'Disabled': [],
            'StarChannel': int(), 'StarCount': int(),
            'Events': [], 'mention': True
        }

    async def __call__(self, bot, message):
        if message.guild.id in self.cache:
            return self.cache[message.guild.id]

        data = await bot.loop.run_in_executor(None, self.column.find_one, {'_id': message.guild.id})
        if not data:
            data = self.guild_data.copy()
            data['_id'] = message.guild.id
            await bot.loop.run_in_executor(None, self.column.insert_one, data)

            prefixes_ = ['-']
        else:
            prefixes_ = data['prefix']

        if not type(prefixes_) == list:
            prefixes_ = [prefixes_]

        if data.get('mention'):
            prefixes = when_mentioned_or(*prefixes_)(bot, message)
            prefix = Prefix(prefixes)
        else:
            prefix = Prefix(prefixes_, mention=False)
            
        self.cache.update({message.guild.id: prefix})

        return prefix
