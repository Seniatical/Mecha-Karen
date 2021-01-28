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
from discord.ext.commands import cooldown, BucketType
import datetime
import random
import asyncio
import math
import json
import time
import numpy as np
import _asyncio

from Others import words
from Helpers import boards

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.running = dict()

    @commands.command(name='RPS')
    @commands.cooldown(1, 15, BucketType.user)
    async def rps(self, ctx, choice=None):
        embed = discord.Embed(
            description='React to one of the 3 given options below.',
            colour=discord.Colour.green(),
            title='Rock Paper Scissors!'
        )
        msg = await ctx.send(embed=embed)
        options = ['🪨', '🧻', '✂️']
        for i in options:
            await msg.add_reaction(i)
        option = []

        def check(m):
            if m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) in options:
                option.append(str(m.emoji))
                return True
            return False

        try:
            await self.bot.wait_for('raw_reaction_add', timeout=20.0, check=check)

            embed = discord.Embed(colour=discord.Colour.red(), description='Good Game **{}**.'.format(ctx.author))
            karens_opt = random.choice(options)

            if karens_opt == option[0]:
                embed.title = 'Draw!'
                embed.add_field(name=ctx.author.display_name, value=option[0])
                embed.add_field(name=self.bot.user.display_name, value=karens_opt)
            elif karens_opt == '🪨':
                if option[0] == '🧻':
                    embed.title = 'You win!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name=self.bot.user.display_name, value=karens_opt)
                else:
                    embed.title = 'You loose!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name=self.bot.user.display_name, value=karens_opt)
            elif karens_opt == '🧻':
                if option[0] == '✂️':
                    embed.title = 'You win!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name=self.bot.user.display_name, value=karens_opt)
                else:
                    embed.title = 'You loose!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name=self.bot.user.display_name, value=karens_opt)
            else:
                if option[0] == '🪨':
                    embed.title = 'You win!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name=self.bot.user.display_name, value=karens_opt)
                else:
                    embed.title = 'You loose!'
                    embed.add_field(name=ctx.author.display_name, value=option[0])
                    embed.add_field(name=self.bot.user.display_name, value=karens_opt)
            await msg.clear_reactions()
            await msg.edit(embed=embed)

        except asyncio.TimeoutError:
            await msg.clear_reactions()
            await msg.edit(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def decipher(self, ctx, opt='Easy'):
        options = ['easy', 'medium', 'hard', 'impossible']
        if not opt.lower() in options:
            await ctx.send('Give a valid difficulty.\n**Current Difficulties:**\n> `Easy` `Medium` `Hard` `Impossible`')
            return
        choice = opt.lower()
        if choice == 'easy':
            choice = random.choice(words.easy)
        elif choice == 'medium':
            choice = random.choice(words.medium)
        elif choice == 'hard':
            choice = random.choice(words.hard)
        elif choice == 'impossible':
            choice = random.choice(words.impossible)
        x = list(choice)
        random.shuffle(x)
        await ctx.send('**⬇ The word you must decipher is ⬇**')
        await ctx.send(' '.join(map(str, x)))

        def check(m):
            user = ctx.author
            if m.author.id == user.id and m.content.lower() == choice.lower():
                return True
            return False
        try:
            start = time.time()
            await self.bot.wait_for('message',timeout=30.0,check=check)
            end = time.time()
            await ctx.send(embed=discord.Embed(
                title='Congratulations!',
                colour=discord.Colour.green(),
                description='You were able to guess my word within **{:.2f}**s <a:tada:787761454564114444>'.format(end-start),
                timestamp=ctx.message.created_at
            ).set_footer(text='Well Done!', icon_url=self.bot.user.avatar_url))
        except asyncio.TimeoutError:
            await ctx.send(embed=discord.Embed(
                title='Failure...',
                colour=discord.Colour.red(),
                description='You weren\'t able to guess my word. Better luck next time, my word was **{}**'.format(choice),
                timestamp=ctx.message.created_at
            ).set_footer(text='You lost!', icon_url=self.bot.user.avatar_url))

    @commands.command(aliases=['dice'])
    @commands.cooldown(1, 10, BucketType.member)
    async def roll(self, ctx, member: discord.Member = None):
        dice = random.randrange(7)
        dice2 = random.randrange(7)
        embed = discord.Embed(
            title='Dice Roll!',
            color=discord.Color.teal()
        )
        embed.add_field(name=ctx.author, value=str(dice))
        if member != None:
            pass
        else:
            member = 'Mecha Karen'
        embed.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
        embed.add_field(name=member, value=str(dice2))
        embed.add_field(name='‏‏‎ ‎', value='Join our [Support Server](https://discord.gg/Q5mFhUM)')
        embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
        embed.set_author(name=ctx.author)
        await ctx.send(embed=embed)

    @commands.command()
    async def snipe(self, ctx):
        with open('JSON/snipe.json', 'r') as k:
            word = json.load(k)
        try:
            try:
                x = word[str(ctx.channel.id)]
                avatar = self.bot.get_user(int(x['avatar']))
                embed = discord.Embed(
                    description=x['message']
                )
                embed.set_author(name=x['author'], icon_url=avatar.avatar_url)
                embed.set_footer(text='Today at ' + x['created_at'])
                await ctx.send(embed=embed)
                with open('JSON/snipe.json', 'w') as f:
                    word.pop(str(ctx.channel.id))
                    json.dump(word, f, indent=4)
            except AttributeError:
                raise KeyError
        except KeyError:
            await ctx.send('There is nothing to snipe!')

    @commands.command()
    async def coin(self, ctx, user_choice: str = None):
        choices = ('heads', 'head', 'tails', 'tail')
        if user_choice == None or user_choice.lower() not in choices:
            await ctx.send('Give a valid choice of **Heads** or **Tails**')
            return
        bot_choice = random.choice(choices)
        embed = discord.Embed(
                title='Heads and Tails',
                colour=ctx.author.colour or self.bot.user.colour
            )
        embed.add_field(name='{}'.format(ctx.author), value=user_choice)
        embed.add_field(name='{}'.format(self.bot.user), value=bot_choice)
        if user_choice.lower() == bot_choice or user_choice.lower() == bot_choice + 's':
            embed.description = 'You WIN!'
        else:
            embed.description = 'You lost.'
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def minesweeper(self, ctx):
        global num, score, board
        msg = await ctx.send('**Generating the board now**!')
        board = 3 * 3
        items = ['💣', '🔟', '💯']
        ## our map range for our board
        ranges = list(range(board))   ## Know were going map the board index with this
        bomb = random.randint(0, 9)
        ranges[bomb] = items[0]
        max_pts = random.choice(ranges)
        while max_pts == bomb and isinstance(max_pts, int):
            max_pts = random.choice(ranges)
            try:
                int(max_pts)
            except ValueError:
                max_pts = 0
                continue
        ranges[max_pts] = items[2]
        for i in ranges:
            if isinstance(i, int):
                ranges[i] = items[1]
        board = '''
⬛⬛⬛
⬛⬛⬛
⬛⬛⬛
        '''
        score = 0
        embed = discord.Embed(
            title='Score: {}'.format(score),
            colour=discord.Color.green(),
            description=board
        )
        await msg.edit(embed=embed, content=None)
        await msg.add_reaction('1️⃣')
        await msg.add_reaction('2️⃣')
        await msg.add_reaction('3️⃣')
        await msg.add_reaction('4️⃣')
        await msg.add_reaction('5️⃣')
        await msg.add_reaction('6️⃣')
        await msg.add_reaction('7️⃣')
        await msg.add_reaction('8️⃣')
        await msg.add_reaction('9️⃣')
        await msg.add_reaction('❎')
        num = 0

        def check(m):
            global num
            if m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '1️⃣':
                num = 1
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '2️⃣':
                num = 2
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '3️⃣':
                num = 3
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '4️⃣':
                num = 4
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '5️⃣':
                num = 5
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '6️⃣':
                num = 6
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '7️⃣':
                num = 7
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '8️⃣':
                num = 8
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '9️⃣':
                num = 9
                return True
            elif m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) == '❎':
                num = 'end'
                return True
            return False

        async def game():
            global num, score, board
            while True:
                await self.bot.wait_for('raw_reaction_add', check=check)
                if score == 170:
                    embed_ = msg.embeds[0]
                    embed_.title = 'You Won ({} pts)'.format(score)
                    await msg.edit(embed=embed)
                    await msg.clear_reactions()
                    break
                if num == 'end':
                    embed_ = msg.embeds[0]
                    embed_.title = 'Score: {} (Game Over)'.format(score)
                    await msg.edit(embed=embed_)
                    await msg.clear_reactions()
                    break
                elif num == 1:
                    board_pos = ranges[0]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[0] = ranges[0]
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[0] = ranges[0]
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('1️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[0] = ranges[0]
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('1️⃣', ctx.author)

                elif num == 2:
                    board_pos = ranges[1]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[1] = board_pos
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[1] = board_pos
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('2️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[1] = board_pos
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('2️⃣', ctx.author)

                elif num == 3:
                    board_pos = ranges[2]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[2] = board_pos
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[2] = board_pos
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('3️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[1])
                        temp_row[2] = board_pos
                        temp[1] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('3️⃣', ctx.author)

                elif num == 4:
                    board_pos = ranges[3]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[0] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[0] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('4️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[0] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('4️⃣', ctx.author)

                elif num == 5:
                    board_pos = ranges[4]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[1] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[1] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('5️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[1] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('5️⃣', ctx.author)

                elif num == 6:
                    board_pos = ranges[5]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[2] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[2] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('6️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[2])
                        temp_row[2] = board_pos
                        temp[2] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('6️⃣', ctx.author)

                elif num == 7:
                    board_pos = ranges[6]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[0] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[0] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('7️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[0] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('7️⃣', ctx.author)

                elif num == 8:
                    board_pos = ranges[7]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[1] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[1] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('8️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[2] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('8️⃣', ctx.author)

                elif num == 9:
                    board_pos = ranges[8]
                    if board_pos == '💣':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[2] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        embed_.title = 'Score: {} (Game Over)'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.clear_reactions()
                        break
                    elif board_pos == '🔟':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[2] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 10
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('9️⃣', ctx.author)
                    elif board_pos == '💯':
                        embed_ = msg.embeds[0]
                        temp = board.split('\n')
                        temp_row = list(temp[3])
                        temp_row[2] = board_pos
                        temp[3] = ''.join(temp_row)
                        board = '\n'.join(temp)
                        embed_.description = board
                        score += 100
                        embed_.title = 'Score: {}'.format(score)
                        await msg.edit(embed=embed_)
                        await msg.remove_reaction('9️⃣', ctx.author)
        self.bot.loop.create_task(game())

    @commands.command()
    @commands.cooldown(1, 120, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_messages=True, embed_links=True)
    async def hangman(self, ctx, difficulty: str = 'Easy'):
        if ctx.channel.id in self.running:
            return await ctx.send('There is a game already running!')
        self.running[ctx.channel.id] = True
        dif = difficulty.lower()
        if dif not in ['easy', 'medium', 'hard']:
            ctx.commands.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Choose a valid difficulty from `Easy | Medium | Hard`',
                colour=discord.Colour.red()
            ), mention_author=False)
        global letter, attempts, guesses
        start = time.time()
        if dif == 'easy':
            word = random.choice(words.easy)
        elif dif == 'medium':
            word = random.choice(words.medium)
        elif dif == 'hard':
            word = random.choice(words.hard)
        attempts = 0
        display = boards.hangman[attempts]
        embed = discord.Embed(
            title='Hangman! (Game Active)',
            colour=discord.Colour.green(),
            description='```\n' + display + '\n```',
            timestamp=datetime.datetime.utcnow()
        )
        lives = ['❤️' for i in range(9)]
        spaces = ['?' for i in range(len(word))]
        embed.add_field(name='How to Play?', value='You have 9 attempts to try and guess the word i am thinking of. If wish to stop playing type `end` and the game will end. All 3 difficulties are do-able so have fun!')
        embed.add_field(name='Lives Left:', value=' '.join(lives), inline=False)
        embed.add_field(name='Spaces:', value=' '.join(spaces), inline=False)
        embed.add_field(name='Guesses:', value='_')
        msg = await ctx.send(embed=embed)
        letter = []
        guesses = []

        def check(m):
            global letter
            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id:
                letter.append(m)
                return True
            return False
        print(word)

        async def game():
            global attempts, letter, guesses
            win = False
            while attempts != 9:
                try:
                    await self.bot.wait_for('message', check=check, timeout=30.0)
                except asyncio.TimeoutError:
                    break

                if letter[0].content.lower() == 'end':
                    end = time.time()
                    embed_ = msg.embeds[0]
                    embed_.title = 'Hangman! (Game Ended)'
                    embed_.colour = discord.Colour.red()
                    embed_.set_footer(text='Game lasted {:.2f} s'.format(end-start), icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed_, content='You never got my word, I was thinking of **{}**.'.format(word))
                    break

                elif letter[0].content.lower() in guesses:
                    embed_ = msg.embeds[0]
                    await letter[0].delete()
                    letter.pop(0)
                    embed_.colour = discord.Colour.red()
                    embed_.set_footer(text='You have already guessed this word.', icon_url=ctx.author.avatar_url)
                    await msg.edit(embed=embed_)
                    continue

                elif letter[0].content.lower() in word and len(letter[0].content.lower()) == 1:
                    await letter[0].delete()
                    guesses.append(letter[0].content.lower())
                    embed_ = msg.embeds[0]
                    word_mapper = embed_.fields[-2].value.split()
                    for i in range(len(word_mapper)):
                        if word[i] == letter[0].content.lower():
                            word_mapper[i] = letter[0].content.lower()
                    embed_.set_field_at(-2, name='Spaces:', value=' '.join(word_mapper), inline=False)
                    embed_.set_field_at(-1, name='Guesses:', value=', '.join(guesses), inline=False)
                    letter.pop(0)
                    if ''.join(word_mapper) == word:
                        embed_.colour = discord.Colour.green()
                        embed_.title = 'Hangman! (Game Completed)'
                        lives_left = embed_.fields[1].value.split()
                        remaining_lives = 0
                        for i in lives_left:
                            if i == '❤️':
                                remaining_lives += 1
                        win = True
                        embed_.set_footer(text='You guessed my word with {} lives left!'.format(remaining_lives),
                                          icon_url=self.bot.user.avatar_url)
                        await msg.edit(embed=embed_)
                        break
                    await msg.edit(embed=embed_)

                elif letter[0].content.lower() != word or letter[0].content.lower() not in word:
                    await letter[0].delete()
                    guesses.append(letter[0].content.lower())
                    embed_ = msg.embeds[0]
                    embed_.set_footer(text='I wasn\'t thinking of {}'.format(letter[0].content), icon_url=self.bot.user.avatar_url)
                    embed_.colour = discord.Colour.red()
                    lives_left = embed_.fields[1].value.split()[::-1]
                    for i in range(len(lives_left)):
                        if lives_left[i] == '❤️':
                            lives_left[i] = '🖤'
                            break
                    attempts += 1
                    embed_.description = '```\n' + boards.hangman[attempts] + '\n```'
                    letter.pop(0)
                    embed_.set_field_at(1, name='Lives Left:', value=' '.join(lives_left[::-1]), inline=False)
                    embed_.set_field_at(-1, name='Guesses:', value=', '.join(guesses), inline=False)
                    await msg.edit(embed=embed_)

                elif letter[0].content.lower() == word:
                    embed_ = msg.embeds[0]
                    embed_.colour = discord.Colour.green()
                    embed_.title = 'Hangman! (Game Completed)'
                    lives_left = embed_.fields[1].value.split()
                    remaining_lives = 0
                    for i in lives_left:
                        if i == '❤️':
                            remaining_lives += 1
                    win = True
                    embed_.set_footer(text='You guessed my word with {} lives left!'.format(remaining_lives),
                                      icon_url=self.bot.user.avatar_url)
                    await msg.edit(embed=embed_)
                    break

                if attempts == 5:
                    embed_ = msg.embeds[0]
                    current_progress = embed_.fields[-2].value.split()
                    is_val = len([i for i in current_progress if i == '?'])
                    if is_val < 1:
                        continue
                    embed_.set_footer(
                        text='You seem to be struggling I have given your 1 letter!',
                        icon_url=self.bot.user.avatar_url)
                    embed_.colour = discord.Colour.green()
                    word_index = random.choice([i for i in range(len(embed_.fields[-2].value.split()))])
                    while word[word_index] == '?':
                        word_index = random.choice([i for i in range(len(embed_.fields[-2].value.split()))])
                    letter_ = word[word_index]
                    guesses.append(letter_)
                    word_mapper = embed_.fields[-2].value.split()
                    word_mapper[word_index] = letter_
                    new_ = ' '.join(word_mapper)
                    embed_.set_field_at(-2, name='Spaces:', value=new_)
                    embed_.set_field_at(-1, name='Guesses:', value=', '.join(guesses), inline=False)
                    await msg.edit(embed=embed_)

            if not win:
                await ctx.send('You were not able to guess my word, I was thinking of **{}**'.format(word))

        self.bot.loop.create_task(game())
        
    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_messages=True, embed_links=True)
    async def fight(self, ctx, user: discord.Member = None):
        global user2, user1, go_first
        if not user or user == ctx.author:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='Need to give a user to fight!',
                colour=discord.Colour.red()
            ))
        if user.bot:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='You have to fight an actual user!',
                colour=discord.Colour.red()
            ))

        msg = await ctx.send(embed=discord.Embed(
            description='Setting up the match! {} VS {}'.format(ctx.author, user),
            colour=discord.Colour.red()
        ))
        await msg.add_reaction('👊'), await msg.add_reaction('🛡️'), await msg.add_reaction('🚪')
        holder = []
        user1 = 100
        user2 = 100


        def check1(m):
            if m.user_id == ctx.author.id and m.message_id == msg.id and str(m.emoji) in ['🚪', '🛡️', '👊']:
                holder.append(str(m.emoji))
                return True
            return False

        def check2(m):
            if m.user_id == user.id and m.message_id == msg.id and str(m.emoji) in ['🚪', '🛡️', '👊']:
                holder.append(str(m.emoji))
                return True
            return False
        
        async def user_2():
            global user2, user1
            try:
                await self.bot.wait_for('raw_reaction_add', timeout=20.0, check=check2)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return await msg.edit(embed=discord.Embed(
                    description='Looks like **{}** doesn\'t want to fight...'.format(user),
                    colour=discord.Colour.red()
                ))
            emoji = holder.pop(0)
            if emoji == '🚪':
                await msg.clear_reactions()
                return await msg.edit(embed=discord.Embed(
                    description='Looks like **{}** doesn\'t want to fight...'.format(user),
                    colour=discord.Colour.red()
                ))
            elif emoji == '🛡️':
                if user2 == 100:
                    await user_2()
                    await msg.edit(embed=discord.Embed(
                        description='Your still on **100** HP! Retry again...',
                        colour=discord.Colour.red()
                    ))
                    await msg.remove_reaction(emoji, ctx.author)
                else:
                    increase = random.randrange(100-user2)
                    user2 += increase
                    await msg.edit(embed=discord.Embed(
                        description='You gained **{}** HP'.format(increase),
                        colour=discord.Colour.green()
                    ))
                    await msg.remove_reaction(emoji, ctx.author)
            elif emoji == '👊':
                dmg = random.randrange(15, 30)
                if user1 - dmg < 0:
                    await msg.clear_reactions()
                    return await msg.edit(embed=discord.Embed(
                        description='**{}** smacked up **{}** and won!'.format(user, ctx.author),
                        colour=discord.Colour.green()
                    ))
                else:
                    user1 -= dmg
                    await msg.edit(embed=discord.Embed(
                        description='**{}** smacks **{}** and deals **{}** damage.'.format(user, ctx.author, dmg)
                    ))
                await msg.remove_reaction(emoji, ctx.author)

        async def user_1():
            global user2, user1
            try:
                await self.bot.wait_for('raw_reaction_add', timeout=20.0, check=check1)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                return await msg.edit(embed=discord.Embed(
                    description='Looks like **{}** doesn\'t want to fight...'.format(ctx.author),
                    colour=discord.Colour.red()
                ))
            emoji = holder.pop(0)
            if emoji == '🚪':
                await msg.clear_reactions()
                return await msg.edit(embed=discord.Embed(
                    description='Looks like **{}** doesn\'t want to fight...'.format(ctx.author),
                    colour=discord.Colour.red()
                ))
            elif emoji == '🛡️':
                try:
                    increase = random.randrange(100-user1)
                except ValueError:
                    await msg.edit(embed=discord.Embed(
                        description='Your still on **100** HP! Retry again...',
                        colour=discord.Colour.red()
                    ))
                    await asyncio.sleep(2)
                    await user_2()
                user1 += increase
                await msg.edit(embed=discord.Embed(
                    description='You gained **{}** HP'.format(increase),
                    colour=discord.Colour.green()
                ))
                await msg.remove_reaction(emoji, ctx.author)
            elif emoji == '👊':
                dmg = random.randrange(15, 30)
                if user2 - dmg <= 0:
                    await msg.clear_reactions()
                    return await msg.edit(embed=discord.Embed(
                        description='**{}** smacked up **{}** and won!'.format(ctx.author, user),
                        colour=discord.Colour.green()
                    ))

                else:
                    user2 -= dmg
                    await msg.edit(embed=discord.Embed(
                        description='**{}** smacks **{}** and deals **{}** damage.'.format(ctx.author, user, dmg)
                    ))
                await msg.remove_reaction(emoji, ctx.author)

        go_first = True
        if random.choice(['y', 'n']) == 'y':
            go_first = False

        async def game_loop():
            x = 0
            await msg.edit(embed=discord.Embed(
                description='**{}** Your up.'.format(user if x % 2 == 0 else ctx.author)
            ).set_footer(text='{}: {} | {}: {}'.format(ctx.author, user1, user, user2)))
            while True:
                if x % 2 == 0:
                    await user_2()
                else:
                    await user_1()
                x += 1
                await asyncio.sleep(2)
                await msg.edit(embed=discord.Embed(
                    description='**{}** Your up.'.format(user if x % 2 == 0 else ctx.author)
                ).set_footer(text='{}: {} | {}: {}'.format(ctx.author, user1, user, user2)))
        self.bot.loop.create_task(game_loop())
