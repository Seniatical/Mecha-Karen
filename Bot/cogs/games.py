import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import datetime
import random
import asyncio
import math

from Others import words

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 5, BucketType.user)
    async def RPS(self, ctx, choice=None):
        if choice == None:
            embed=discord.Embed(
                title='You gotta give a choice!',
                color=discord.Color.red(),
                description=f'{ctx.author.mention} you never gave a valid choice. the choice you gave was {choice}. The valid options are:\n`rock` `paper` `scissor`'
            )
            await ctx.send(embed=embed)
        else:
            x = choice.lower()
            option = ['rock', 'paper', 'scissor']
            op = random.choice(option)
            if x == 'rock':
                if op == 'rock':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: rock\n\nWe both got rock! So its a tie. Good Game {ctx.author.name}!!!')
                elif op == 'paper':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: paper\n\nYou chose paper. Paper wraps rock. So i win!')
                elif op == 'scissor':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: scissors\n\nYou Won!!! Rock beats scissors. Good Game {ctx.author.name}!!!')
            elif x == 'scissor':
                if op == 'rock':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: rock\n\nRock smashes scissors. You loose haha!')
                elif op == 'paper':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: paper\n\nYou Win! Scissors cut paper. So you win {ctx.author}')
                elif op == 'scissor':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: scissors\n\nIts a tie. Good Game {ctx.author.name}!!!')
            elif x == 'paper':
                if op == 'rock':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: rock\n\nYou win as paper wraps rock!!!')
                elif op == 'paper':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karen: paper\n\nIts a tie. We bot picked paper!')
                elif op == 'scissor':
                    await ctx.send(f'{ctx.author.name}: {choice}\nMecha Karne: scissor\n\nYou Loose! Scissors cut paper.')
            else:
                embed=discord.Embed(
                    title='You gotta give a choice!',
                    color=discord.Color.red(),
                    description=f'{ctx.author.mention} you never gave a valid choice. the choice you gave was {choice}. The valid options are:\n`rock` `paper` `scissor`'
                )
                await ctx.send(embed=embed)

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
            await self.bot.wait_for('message',timeout=30.0,check=check)
            await ctx.send(f'**Congratulations {ctx.author}! You got the correct word.**')
        except asyncio.TimeoutError:
            await ctx.send('Your answer is **INCORRECT!**')
            await ctx.send(f'**The correct word was {choice}**')

    @commands.command(aliases=['dice'])
    @commands.cooldown(1, 10, BucketType.member)
    async def roll(self, ctx, member : discord.Member=None):
        dice = random.randrange(7)
        dice2 = random.randrange(7)
        embed = discord.Embed(
            title='Dice Roll!',
            color=discord.Color.teal()
        )
        embed.add_field(name=ctx.author, value=dice)
        if member != None:
            pass
        else:
            member = 'Mecha Karen'
        embed.add_field(name=member, value=dice2, inline=False)
        embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
        embed.set_author(name=ctx.author)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.member)
    async def flip(self, ctx, user_choice : str=None):
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
            
def setup(bot):
    bot.add_cog(games(bot))

