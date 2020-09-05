import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
import datetime
import random
import words
import asyncio
import math

class games(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Games cog is ready')

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
    async def decipher(self, ctx):
        await ctx.send(f'**Welcome to decipher {ctx.author.name}!**')
        await ctx.send(f'In decipher you will be given a scrambled word. You must get the original word in less than 30 seconds!\n*You will have as many tries as you need!*')
        msg = await ctx.send('**Do you have what it takes to complete this challenge?\nIf so respond with `yes`**')
        def check(m):
            return m.content == 'yes'
        try:
            msg = await self.bot.wait_for('message',timeout=5.0 ,check=check)
            choice = random.choice(words.easy)
            x = list(choice)
            random.shuffle(x)
            await ctx.send('**⬇ The word you must decipher is ⬇**')
            await ctx.send(' '.join(map(str, x)))
            def check(m):
                return m.content == choice.lower()
            try:
                msg = await self.bot.wait_for('message',timeout=30.0,check=check)
                await ctx.send(f'**Congratulations {ctx.author}! You got the correct word.**')
            except asyncio.TimeoutError:
                await ctx.send('Your answer is **INCORRECT!**')
                await ctx.send(f'**The correct word was {choice}**')
        except asyncio.TimeoutError:
            msg.delete()
            await ctx.send('You never responded with **`yes`** in time!')

    @commands.command(aliases=['dice'])
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
        embed.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
        embed.add_field(name=member, value=dice2)
        embed.add_field(name='‏‏‎ ‎', value='Join our [Support Server](https://discord.gg/Q5mFhUM)')
        embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
        embed.set_author(name=ctx.author)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def maths(self, ctx):
        msg = await ctx.send('**Welcome to maths sim. Your goal is to get as many questions correct in the given time!**\n__There will be a 10 second time limit for every question__\n**Respond with `yes` to proceed.**')
        em = discord.Embed(title='Final Results', color=discord.Color.gold())
        def check(m):
            return m.content == 'yes'.lower()

        try:
            choice1=random.randrange(50)
            choice2=random.randrange(50)
            await self.bot.wait_for('message', timeout=10.0, check=check)
            await msg.delete()
            msg = await ctx.send('**Lets start easy then!**')
            embed = discord.Embed(
                title='Easy',
                color=discord.Color.green()
            )
            embed.add_field(name='What is:', value=f'{choice1} + {choice2}')
            msg = await ctx.send(embed=embed)
            result = choice1 + choice2
            def check(m):
                return m.content == f'{result}'
            try:
                choice1=random.randrange(50)
                choice2=random.randrange(50)
                await self.bot.wait_for('message', timeout=10.0, check=check)
                await ctx.send('**Correct!**')
                embed = discord.Embed(title='Easy',color=discord.Color.green())
                embed.add_field(name='What is:', value=f'{choice1} - {choice2}')
                result = choice1 - choice2
                await ctx.send(embed=embed)
                def check(m):
                    return m.content == f'{result}'
                try:
                    choice1=random.randrange(12)
                    choice2=random.randrange(12)
                    await self.bot.wait_for('message', timeout=10.0, check=check)
                    await ctx.send('**Correct!**\nYour doing well.')
                    embed=discord.Embed(title='Easy', color=discord.Color.green())
                    embed.add_field(name='What is:', value=f'{choice1} x {choice2}')
                    result = choice1 * choice2
                    await ctx.send(embed=embed)
                    def check(m):
                        return m.content == f'{result}'
                    try:
                        choice1=random.randrange(100)
                        choice2=random.randrange(10)
                        await self.bot.wait_for('message', timeout=10.0, check=check)
                        await ctx.send('**Correct!** Your doing really well. 2 More easy ones and we will see if your worthy!')
                        embed=discord.Embed(title='Easy', color=discord.Color.green())
                        embed.add_field(name='What is:', value=f'{choice1} ÷ {choice2}')
                        embed.set_footer(text='Give the base number without rounding.\nExample: 12.45565\nAnswer: 12')
                        result = choice1 / choice2
                        result = int(result)
                        await ctx.send(embed=embed)
                        def check(m):
                            return m.content == f'{result}'
                        try:
                            choice1=random.randrange(1, 50)
                            await self.bot.wait_for('message', timeout=10.0, check=check)
                            await ctx.send('**Correct!** You seem to be a worthy opponent.')
                            embed=discord.Embed(title='Easy', color=discord.Color.green())
                            embed.add_field(name='What is:', value=f'√{choice1}')
                            embed.set_footer(text='Give the base number without rounding.\nExample: 12.45565\nAnswer: 12')
                            result = int(math.sqrt(choice1))
                            await ctx.send(embed=embed)
                            def check(m):
                                return m.content == f'{result}'
                            try:
                                choice1=random.randrange(100)
                                await self.bot.wait_for('message', timeout=10.0, check=check)
                                await ctx.send('**Correct!** You have 1 more question left before your receive the `Competitors` rank!')
                                embed=discord.Embed(title='Easy', color=discord.Color.green())
                                embed.add_field(name='What is:', value=f'{choice1}²')
                                result = choice1**2
                                def check(m):
                                    return m.content == f'{result}'
                                try:
                                    await self.bot.wait_for('message', timeout=10.0, check=check)
                                except asyncio.TimeoutError:
                                    em.add_field(name='Awful.', value=f'{ctx.author.mention} got `5/6` questions correct. **Give them special lessons!**')
                                    await ctx.send(embed=em)
                            except asyncio.TimeoutError:
                                em.add_field(name='Awful.', value=f'{ctx.author.mention} got `4/5` questions correct. **Give them special lessons!**')
                                await ctx.send(embed=em)
                        except asyncio.TimeoutError:
                            em.add_field(name='Disgraceful.', value=f'{ctx.author.mention} got `3/4` questions correct. **SEND THEM TO SCHOOL**')
                            await ctx.send(embed=em)
                    except asyncio.TimeoutError:
                        await msg.delete()
                        em.add_field(name='Disgraceful.', value=f'{ctx.author.mention} got `2/3` questions correct. **SEND THEM TO SCHOOL**')
                        await ctx.send(embed=em)
                except asyncio.TimeoutError:
                    await msg.delete()
                    em.add_field(name='Disgraceful.', value=f'{ctx.author.mention} got `1/2` questions correct. **SEND THEM TO SCHOOL**')
                    await ctx.send(embed=em)
            except asyncio.TimeoutError:
                await msg.delete()
                em.add_field(name='Disgraceful.', value=f'{ctx.author.mention} got `0/1` questions correct. **SEND THEM TO SCHOOL**')
                await ctx.send(embed=em)
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send('You never responded with `yes`. In the given time!')


def setup(bot):
    bot.add_cog(games(bot))
