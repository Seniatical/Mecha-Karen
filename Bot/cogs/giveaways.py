import discord
from discord.ext import commands
import datetime
import os
from binascii import hexlify
import asyncio
import re

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client

        self.table = self.client['Giveaways']
        self.codes = self.table['codes']

        self.channel_converter = commands.TextChannelConverter()
        self.emoji_converter  = commands.PartialEmojiConverter()
        ## Using partial so i can accept default emoji's as well

        self.giveaways = {}
        self.questions = (
            'Which channel would you like to set this giveaway up in?',
            'How many winners would you like for this giveaway',
            'How long will this giveaway last for? Please use the format of `<TIME>[s/m/h/d/w]`, default is set to seconds.',
            'Are there any requirements? (y/n)',
            'What is the prize for this giveaway?',
            'Would you like a custom emoji in place of the default option "🎉", if not simply respond with `no`. Else send the emoji below. Warning: If using a discord custom emoji, please ensure the bot is in the server that has the emoji.'
            )
        
        self.scopes = {
            ## 'message': 2,
            ## 'invite': 3,

            ## Adding the message and invite option later when I get them done.

            'guild': {
                'scope': 1,
                'aliases': ['guilds']
                },
            'server': {
                'scope': 1,
                'aliases': ['servers']
                },
            ## This is for the reverse search.
            'role': {
                'scope': 2,
                'aliases': ['roles']
                },
            'creation-date': {
                'scope': 3,
                'aliases': ['creation']
                },
            'join-date': {
                'scope': 4,
                'aliases': ['join']
                },
            'exit': {
                'scope': 5,
                'aliases': []
                },
        }

        self.aliase_to_scope = {}

        for key, value in self.scopes.items():
            for aliase in value['aliases']:
                self.aliase_to_scope.update({aliase: key})

        self.scales = {
            's': 1,
            'm': 60,
            'h': (60 * 60),
            'd': ((60 * 60) * 24),
            'w': (((60 * 60) * 24) * 7)
            }

        self.marks = {
            's': 'second(s)',
            'm': 'minutes(s)',
            'h': 'hour(s)',
            'd': 'day(s)',
            'w': 'week(s)'
            }

        self.listed_scopes = ''

        for scope in self.scopes:
            self.listed_scopes += '%s|' % scope

            for aliase in self.scopes[scope]['aliases']:
                self.listed_scopes += '%s|' % aliase

        self.listed_scopes = self.listed_scopes[:-1].split('|')

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

    async def is_float(self, value):
        try:
            float(value)
            return '.' in value
        except ValueError:
            return False

    async def is_int(self, value):
        try:
            int(value)
        except ValueError:
            return False
        return True

    async def is_dupe_scope(self, scopes, scope):
        if scope == 'server' and ['guild', 'guilds'] in scopes:
            return True
        if scope == 'servers' and ['guild', 'guilds'] in scopes:
            return True
        
        if scope in scopes:
            return True

        ## Now were gonna do an aliase check
        for scope in scopes:
            sub_dict = self.scopes.get(scope)
            if not sub_dict:
                ## This just means its an aliase now
                ## this is a reverse key and aliase search. So it will pick up `guilds` `guild`
                return self.aliase_to_scope.get(scope) in scopes

            ## Now we need to pickup `guild` `guilds`
            if scope in sub_dict['aliases'] and scope in scopes:
                return True

        return False

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def giveaway(self, ctx):
        r"""
        Because each question needs a seperate response / action,
        I will have to do them manually as opposed to a for loop :c
        """
        message = await ctx.send('Setting up session, Please be ready to respond to the questions. You have **3 Seconds**, to get ready!\n> You will have up to 30 seconds to answer each question, ')
        ## Give them some time to prepare
        await asyncio.sleep(3)

        ## Getting the channel
        await message.edit(content=self.questions[0])

        async def get_channel():
            try:
                channel = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
            except asyncio.TimeoutError:
                return 'Timeout'

            try:
                channel = (await self.channel_converter.convert(ctx, channel.content))
            except commands.ChannelNotFound:
                return False
            return channel

        for i in range(3):
            channel = await get_channel()

            if channel == 'Timeout':
                return await message.edit(content='Response duration has exceeded **30 seconds**. This giveaway has been cancelled')
            elif not channel:
                await message.edit(content='Invalid channel provided, You have #%s attempts left before cancellation.' % (3 - (i + 1)))
            else:
                await message.edit(content='This giveaway will be setup in %s, respond with (y/n) to confirm.' % channel.mention)

                try:
                    check = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
                except asyncio.TimeoutError:
                    await message.edit(content='Answer wasn\'t provided, I will assume you have said yes.')
                    break

                if check.content.lower() == 'y':
                    break

                else:
                    await message.edit(content='This channel will not be used for your giveaway, please respond with a new channel. You have %s attempts left before cancellation.' % (3 - (i + 1)))

        if not channel:
            return await message.edit(content='A channel could not be established. This giveaway has been cancelled.')

        new_message = await ctx.send('This giveaway has been set in the channel %s.' % channel.mention)

        ## Getting the winners
        winners_message = await ctx.send(self.questions[1])

        async def get_winners():
            try:
                message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
            except asyncio.TimeoutError:
                return 'Timeout'

            check = await self.is_int(message.content)

            if not check:
                return False, message.content
            return True, message.content

        for i in range(3):
            winners = await get_winners()

            if winners == 'Timeout':
                return await winners_message.edit(content='Response duration has exceeded **30 seconds**. This giveaway has been cancelled')
            elif type(winners) == tuple:
                if not winners[0]:
                    await winners_message.edit(content='It appears that `%s` is not a valid number, please try again. You have %s attempts left.' % (winners[1], (3 - (i + 1))))
                else:
                    await winners_message.edit(content='Are you sure that you want to use this count for the giveaway? Respond with (y/n) to confirm.')
                
                    try:
                        check = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
                    except asyncio.TimeoutError:
                        await winners_message.edit(content='Answer wasn\'t provided, I will assume you have said yes.')
                        break

                    if check.content.lower() == 'y':
                        break

                    else:
                        await winners_message.edit(content='This count will not be used for your giveaway, please respond with a new count. You have %s attempts left before cancellation.' % (3 - (i + 1)))

        if not winners:
            return await winners_message.edit(content='A winner count could not be established. This giveaway has been cancelled.')

        await ctx.send('There will be a total of **%s** winners for this giveaway, If there less particpants than the amount provided. It will be scaled down accordingly.' % winners[1])
        winners = winners[1]

        ## Get the giveaway duration
        time_message = await ctx.send(self.questions[2])

        async def get_time_as_seconds():
            try:
                message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)
            except asyncio.TimeoutError:
                return 'Timeout'

            check = await self.is_int(message.content[:-1])
            ## Last letter of the message will have the scale
            ## e.g. 10S

            if not check:
                ## Well this means that they didnt follow it all
                return 'Invalid Format', message.content

            ## Now we check the scales
            if await self.is_int(message.content[-1]):
                scale = 's'
            else:
                scale = message.content[-1].lower()
                
            if not self.scales.get(scale):
                return 'Invalid Scale', message.content[-1]
                
            return (int(message.content[:-1]) * self.scales.get(message.content[-1])), message.content

        for i in range(3):
            seconds = await get_time_as_seconds()

            if winners == 'Timeout':
                return await winners_message.edit(content='Response duration has exceeded **30 seconds**. This giveaway has been cancelled')
            if seconds[0] == 'Invalid Format':
                await time_message.edit(content='It appears that, `%s` is not recognised as a number. You have %s attempts left before cancellation.' % (seconds[1], (3 - (i + 1))))

            elif seconds[0] == 'Invalid Scale':
                await time_message.edit(content='The unit, `%s`, is not a valid scale. Please choose from `[s/m/h/d/w]`. You have %s attempts left before cancellation.' % (seconds[1], (3 - (i + 1))))

            else:
                time_to_rest = seconds[0]
                
                await time_message.edit(content='The giveaway will run for **%s %s**? Respond with (y/n) to confirm.' % (seconds[1][:-1], self.marks.get(seconds[1][-1].lower())))

                try:
                    check = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
                except asyncio.TimeoutError:
                    await winners_message.edit(content='Answer wasn\'t provided, I will assume you have said yes.')
                    break

                if check.content.lower() == 'y':
                    break

                else:
                    await winners_message.edit(content='This time will not be used for your giveaway, please respond with a new time. You have %s attempts left before cancellation.' % (3 - (i + 1)))

        if not seconds:
            return await winners_message.edit(content='A time could not be established. This giveaway has been cancelled.')

        await ctx.send('The giveaway will run for **%s %s**.' % (seconds[1][:-1], self.marks.get(seconds[1][-1].lower())))

        ## Getting the giveaway requirement
        rq_message = await ctx.send(self.questions[3])

        try:
            message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id)

            if message.content.lower() == 'y':
                req = True
            else:
                req = False
        except asyncio.TimeoutError:
            req = False
    
        async def get_requirements():
            await ctx.send('Please list all of your requirements below using the format `R1, R2`.')
            
            pattern = '^({scopes})(, (?!\1)({scopes}))*$'.format(scopes='|'.join(self.listed_scopes))

            try:
                message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
            except asyncio.TimeoutError:
                return 'Timeout'

            match = re.match(pattern, message.content.lower())
            if not match:
                return False

            groups = match.groups()
            cleansed = []

            for group in groups:
                if not group:       continue
                if group.startswith(', '):      continue

                ## This is just to clean up there response to prevent double scoping
                if group in cleansed:       continue
                if await self.is_dupe_scope(cleansed, group):       continue
                
                cleansed.append(group)
            return cleansed

        scopes = None

        if req:
            for i in range(3):
                require = await get_requirements()
                if not require:
                    await rq_message.edit(content='Invalid list of the requirements given, you have %s attempts left before removal of this feature.' % (3 - (i + 1)))

                else:
                    await rq_message.edit(content='Chosen requirements: `%s`, respond with (y/n) to confirm.' % ', '.join(require))
                    try:
                        message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
                    except asyncio.TimeoutError:
                        await rq_message.edit(content='You didn\'t respond in time. I will assume you have said yes.')

                    if message.content.lower() == 'y':
                        scopes = require
                        break

                    else:
                        await rq_message.edit(content='Removing these scopes from the giveaway. You have %s attempts before removal of this feature.' % (3 - (i + 1)))
    
        if not scopes:
            await ctx.send('No requirements added for this giveaway.')
        else:
            await ctx.send('Adding **%s** requirements to this giveaway, Users will need to meet these before being allowed into the giveaway.' % len(scopes))

        ## Getting the prize
        prize_message = await ctx.send(self.questions[4])
        prize = None

        try:
            message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.send('A prize cannot be established. This giveaway has been cancelled.')

        await prize_message.edit(content='The prize for this giveaway is: %s.\n> Are you sure? (y/n)' % message.content)

        try:
            check = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)

            if check.content.lower() == 'y':
                prize = message.content
            else:
                prize = None
            
        except asyncio.TimeoutError:
            prize = message.content

        if not prize:
            temp = await ctx.send('What is your new prize?')
            for i in range(3):
                try:
                    message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
                except asyncio.TimeoutError:
                    return await ctx.send('Response timeout of **30 seconds** has exceeded. This giveaway has been cancelled')

                await temp.edit(content='The new prize for this giveaway is: %s\n> Are you sure? (y/n)' % message.content)

                try:
                    check = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)

                    if check.content.lower() == 'y':
                        prize = message.content
                        break

                    await temp.edit(content='What is your new prize? You have %s attempts till cancellation of this giveaway' % (3 - (i + 1)))
                    
                except asyncio.TimeoutError:
                    prize = message.content
                    break

        if not prize:
            return await ctx.send('A prize could not be established. This giveaway has been cancelled.')

        await ctx.send('The prize for this giveaway is: %s' % prize)

        ## And finally, getting the emoji
        emoji_message = await ctx.send('Would you like a custom emoji as your entery ticket ? (y/n)')
        emoji = None

        try:
            message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)

            if message.content.lower() == 'y':
                try:
                    em_msg = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id, timeout=30.0)
                    emoji = em_msg.split()[0]
                except asyncio.TimeoutError:
                    emoji = '🎉'

                try:
                    await emoji_message.add_reaction(emoji)
                except Exception:
                    await ctx.send('Invalid emoji provided, please make sure the emoji provided is in a server which the bot is in and most obviously. I have the permissions to add the reaction.\nI will use the default emoji of %s for this giveaway' % '🎉') 
            else:
                emoji = '🎉'
        except asyncio.TimeoutError:
            emoji = '🎉'

        message = await ctx.send('Using emoji "%s" for this giveaway.\nWriting up config files and generating new URL pattern. This may take a moment to complete.' % emoji)

def setup(bot):
    bot.add_cog(Giveaway(bot))
