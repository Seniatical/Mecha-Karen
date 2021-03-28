import discord
from discord.ext import commands
import datetime
import datetime
import os
from binascii import hexlify
import asyncio

class Giveaway(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client

        self.table = self.client['Giveaways']
        self.codes = self.table['codes']

        self.channel_converter = commands.TextChannelConverter()

        self.giveaways = {}
        self.questions = (
            'Which channel would you like to set this giveaway up in?',
            'How many winners would you like for this giveaway',
            'How long will this giveaway last for? Please use the format of `<TIME>[s/m/h/d]`, default is set to seconds.',
            'Are there any requirements? If so, react to this message with corresponding emoji, all options are listed below together with their emoji.',
            'What is the prize for this giveaway?',
            'Would you like a custom emoji in place of the default option "🎉", if not simply respond with `no`. Else send the emoji below. Warning: If using a discord custom emoji, please ensure the bot is in the server that has the emoji.'
            )
        
        self.scopes = {
            'server': 1,
            ## 'message': 2,
            ## 'invite': 3,

            """ Adding the message and invite option later when I get them done. """
            
            'role': 4,
            'creation-date': 5,
            'join-date': 6,
            'exit': 7,
        }

        self.scales = {
            's': 1,
            'm': 60,
            'h': (60 * 60),
            'd': ((60 * 60) * 24),
            'w': (((60 * 60) * 24) * 7)
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

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def giveaway(self, ctx):
        r"""
        Because each question needs a seperate response / action,
        I will have to do them manually as opposed to a for loop :c
        """
        message = await ctx.send('Setting up session, Please be ready to respond to the questions. You have **3 Seconds**, to get ready!\n> You will have up to 30 seconds to answer each question, ')
        ## Give them some to prepare
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
                if  not winners[0]:
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

        new_message = await ctx.send(questions[2])

def setup(bot):
    bot.add_cog(Giveaway(bot))
