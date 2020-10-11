import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType
from discord.ext import tasks
import datetime
import random
import asyncio
import math
import json

from Others import *

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
    async def decipher(self, ctx):
        await ctx.send(f'**Welcome to decipher {ctx.author.name}!**')
        await ctx.send(f'In decipher you will be given a scrambled word. You must get the original word in less than 30 seconds!\n*You will have as many tries as you need!*')
        msg = await ctx.send('**Do you have what it takes to complete this challenge?\nIf so respond with `yes`**')
        def check(m):
            user = ctx.author
            if m.author.id == user.id and m.content.lower() == 'yes':
                return True
            return False
        try:
            msg = await self.bot.wait_for('message',timeout=5.0 ,check=check)
            choice = random.choice(words.easy)
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
                msg = await self.bot.wait_for('message',timeout=30.0,check=check)
                await ctx.send(f'**Congratulations {ctx.author}! You got the correct word.**')
            except asyncio.TimeoutError:
                await ctx.send('Your answer is **INCORRECT!**')
                await ctx.send(f'**The correct word was {choice}**')
        except asyncio.TimeoutError:
            msg.delete()
            await ctx.send('You never responded with **`yes`** in time!')

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
        embed.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
        embed.add_field(name=member, value=dice2)
        embed.add_field(name='‏‏‎ ‎', value='Join our [Support Server](https://discord.gg/Q5mFhUM)')
        embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
        embed.set_author(name=ctx.author)
        await ctx.send(embed=embed)

    @commands.command(aliases=['math'])
    @commands.cooldown(1, 10, BucketType.user)
    async def maths(self, ctx):
        user = ctx.author
        msg = await ctx.send('**Welcome to maths sim. Your goal is to get as many questions correct in the given time!**\n__There will be a 10 second time limit for every question__\n**Respond with `yes` to proceed.**')
        em = discord.Embed(title='Final Results', color=discord.Color.gold())
        def check(m):
            if m.author.id == user.id and m.content.lower() == 'yes':
                return True
            return False
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
                if m.author.id == user.id and m.content.lower() == f'{result}':
                    return True
                return False
            try:
                choice1=random.randrange(50, 100)
                choice2=random.randrange(1, 50)
                await self.bot.wait_for('message', timeout=10.0, check=check)
                await ctx.send('**Correct!**')
                embed = discord.Embed(title='Easy',color=discord.Color.green())
                embed.add_field(name='What is:', value=f'{choice1} - {choice2}')
                result = choice1 - choice2
                msg = await ctx.send(embed=embed)
                def check(m):
                    if m.author.id == user.id and m.content.lower() == f'{result}':
                        return True
                    return False
                try:
                    choice1=random.randrange(12)
                    choice2=random.randrange(12)
                    await self.bot.wait_for('message', timeout=10.0, check=check)
                    await ctx.send('**Correct!**\nYour doing well.')
                    embed=discord.Embed(title='Easy', color=discord.Color.green())
                    embed.add_field(name='What is:', value=f'{choice1} x {choice2}')
                    result = choice1 * choice2
                    msg = await ctx.send(embed=embed)
                    def check(m):
                        if m.author.id == user.id and m.content.lower() == f'{result}':
                            return True
                        return False
                    try:
                        choice1=random.randrange(1, 100)
                        choice2=random.randrange(1, 10)
                        await self.bot.wait_for('message', timeout=10.0, check=check)
                        await ctx.send('**Correct!** Your doing really well. 2 More easy ones and we will see if your worthy!')
                        embed=discord.Embed(title='Easy', color=discord.Color.green())
                        embed.add_field(name='What is:', value=f'{choice1} ÷ {choice2}')
                        embed.set_footer(text='Give the base number without rounding.\nExample: 12.45565\nAnswer: 12')
                        msg = await ctx.send(embed=embed)
                        result = choice1 / choice2
                        result = int(result)
                        def check(m):
                            if m.author.id == user.id and m.content.lower() == f'{round(result)}':
                                return True
                            return False
                        try:
                            choice1=random.randrange(1, 50)
                            await self.bot.wait_for('message', timeout=15.0, check=check)
                            await ctx.send('**Correct!** You seem to be a worthy opponent.')
                            embed=discord.Embed(title='Easy', color=discord.Color.green())
                            embed.add_field(name='What is:', value=f'√{choice1}')
                            embed.set_footer(text='Give the base number without rounding.\nExample: 12.45565\nAnswer: 12')
                            msg = await ctx.send(embed=embed)
                            result = math.sqrt(choice1)
                            def check(m):
                                if m.author.id == user.id and m.content.lower() == f'{round(result)}':
                                    return True
                                return False
                            try:
                                choice1=random.randrange(10)
                                await self.bot.wait_for('message', timeout=10.0, check=check)
                                await ctx.send('**Correct!** You have 1 more question left before your receive the `Basic Knowledge` rank!')
                                embed=discord.Embed(title='Easy', color=discord.Color.green())
                                embed.add_field(name='What is:', value=f'{choice1}²')
                                msg = await ctx.send(embed=embed)
                                result = choice1**2
                                def check(m):
                                    if m.author.id == user.id and m.content.lower() == f'{result}':
                                        return True
                                    return False
                                try:
                                    await self.bot.wait_for('message', timeout=10.0, check=check)
                                    await ctx.send(f'**Correct!** {ctx.author} has gained the `Basic Knowledge` Rank!')
                                    role = discord.utils.get(ctx.guild.roles, name="Basic Knowledge")
                                    guild = ctx.guild
                                    if role not in guild.roles:
                                        perms = discord.Permissions(send_messages=True, speak=True)
                                        await guild.create_role(name="Basic Knowledge", permissions=perms, colour=discord.Color.teal())
                                        await ctx.author.add_roles(role)
                                    else:
                                        await ctx.author.add_roles(role)
                                    await ctx.send('**We will now be moving onto a harder topic. This time you will have double the time or `30` seconds**')
                                    await ctx.send('*It is advised that you have a calculator nearby as some these questions will require 1. A scientific one is recommended*')
                                    msg = await ctx.send(f'**{ctx.author.mention} do you with to carry on? Respond with `yes`**')
                                    def check(m):
                                        if m.author.id == user.id and m.content.lower() == 'yes':
                                            return True
                                        return False
                                    try:
                                        length = random.randint(1, 50)
                                        await self.bot.wait_for('message', timeout=30.0, check=check)
                                        await ctx.send(f'**{ctx.author} has accepted Mecha Karens Challenge!**')
                                        embed = discord.Embed(title='Medium', color=discord.Color.gold())
                                        embed.add_field(name='What is:', value=f'A square has a perimeter of {length}cm. What is the length of 1 side?')
                                        msg = await ctx.send(embed=embed)
                                        result = length / 4
                                        def check(m):
                                            if m.author.id == user.id and m.content.lower() == f'{result}':
                                                return True
                                            return False
                                        try:
                                            length = random.randrange(50)
                                            height = random.randrange(50)
                                            await self.bot.wait_for('message', timeout=30.0, check=check)
                                            await ctx.send('**Correct!** Your a man of knowledge. 4 more questions till you recieve the `Challenger`')
                                            embed = discord.Embed(title='Medium', color=discord.Color.gold())
                                            embed.add_field(name='What is:', value=f'If i have a rectangle with the length of {length} and the height of {height}. What is the area?')
                                            msg = await ctx.send(embed=embed)
                                            result = length * height
                                            def check(m):
                                                if m.author.id == user.id and m.content.lower() == f'{result}':
                                                    return True
                                                return False
                                            try:
                                                radius = random.randrange(100)
                                                await self.bot.wait_for('message', timeout=30.0, check=check)
                                                await ctx.send('**Correct!** You seem to be a hard one. 3 more questions till you recieve the `Challenger` rank!')
                                                embed = discord.Embed(title='Medium', color=discord.Color.gold())
                                                embed.add_field(name='What is:', value=f'If i have a circle with a radius of {radius}. What is the circumference of the circle?')
                                                embed.set_footer(text='If the number is huge dont round it instead give the base number.\nExample answer: 53.954567875433\nAnswer: 53')
                                                result = math.pi * radius * 2
                                                result = int(result)
                                                msg = await ctx.send(embed=embed)
                                                def check(m):
                                                    if m.author.id == user.id and m.content.lower() == f'{result}':
                                                        return True
                                                    return False
                                                try:
                                                    radius = random.randrange(50)
                                                    await self.bot.wait_for('message', timeout=30.0, check=check)
                                                    await ctx.send('**Correct!** This cant be. Your surely going to fail now!!!')
                                                    embed = discord.Embed(title='Medium', color=discord.Color.gold())
                                                    embed.add_field(name='What is:', value=f'If a sphere has a radius of {radius}. What is the volume of the sphere?w')
                                                    msg = await ctx.send(embed=embed)
                                                    result = ((pi/3) * 4) * radius ** 3
                                                    def check(m):
                                                        if msg.id == msg.id and user.id and m.content.lower() == f'{result}':
                                                            return True
                                                        return False
                                                    try:
                                                        H = random.randrange(100)
                                                        W = random.randrange(100)
                                                        await self.bot.wait_for('message', timeout=30.0, check=check)
                                                        await ctx.send('**Correct!** Impossible. 1 more questiong till your recieve the `Challenger` rank!')
                                                        embed = discord.Embed(title='Medium', color=discord.Color.gold())
                                                        embed.add_field(name='What is:', value=f'If i have a cone with the height {H} and a width of {W}. What is the volume of the cone?')
                                                        msg = await ctx.send(embed=embed)
                                                        result = math.pi * H * H * (W/3)
                                                        def check(m):
                                                            if msg.id == msg.id and user.id and m.content.lower() == f'{result}':
                                                                return True
                                                            return False
                                                        try:
                                                            await self.bot.wait_for('message', timeout=30.0, check=check)
                                                            await ctx.send(f'**Correct!** {ctx.author.mention} has recieved the `Challenger` rank!')
                                                            role = discord.utils.get(ctx.guild.roles, name="Challenger")
                                                            guild = ctx.guild
                                                            if role not in guild.roles:
                                                                perms = discord.Permissions(send_messages=True, speak=True)
                                                                await guild.create_role(name="Challenger", permissions=perms, colour=discord.Color.gold())
                                                                await ctx.author.add_roles(role)
                                                            else:
                                                                await ctx.author.add_roles(role)
                                                            msg = await ctx.send(f'**Congratulations {user}. These next questions are the toughest of the toughest. In the next `5` questions you will be competing for the `Mathematicians` rank**\n*These questions are much harder than before. It is advised that you have paper and a scientific calculator nearby. Since these questions are harder. You will have 1 min to complete them!*')
                                                            def check(m):
                                                                if msg.id == msg.id and user.id and m.content.lower() == 'yes':
                                                                    return True
                                                                return False
                                                            try:
                                                                await self.bot.wait_for('message', check=check)
                                                                await ctx.send('Not added yet!!!. Stay tuned. Math freak!')
                                                            except asyncio.TimeoutError:
                                                                em.add_field('<:fail:751827644190031984>', value=f'{ctx.author.mention} got `10/11` questions correct. **A good attempt. But still they are a failure**')
                                                                await ctx.send(embed=em)
                                                        except asyncio.TimeoutError:
                                                            em.add_field('<:fail:751827644190031984>', value=f'{ctx.author.mention} got `10/11` questions correct. **A good attempt. But still they are a failure**')
                                                            await ctx.send(embed=em)
                                                    except asyncio.TimeoutError:
                                                        em.add_field('<:fail:751827644190031984>', value=f'{ctx.author.mention} got `9/10` questions correct. **A good attempt. But still they are a failure**')
                                                        await ctx.send(embed=em)
                                                except asyncio.TimeoutError:
                                                    em.add_field('<:fail:751827644190031984>', value=f'{ctx.author.mention} got `8/9` questions correct. **A good attempt. But still they are a failure**')
                                                    await ctx.send(embed=em)
                                            except asyncio.TimeoutError:
                                                em.add_field('<:fail:751827644190031984>', value=f'{ctx.author.mention} got `7/8` questions correct. **There parents are not going to be happy about that**')
                                                await ctx.send(embed=em)
                                        except asyncio.TimeoutError:
                                            em.add_field('<:fail:751827644190031984>', value=f'{ctx.author.mention} got `6/7` questions correct. **There parents are not going to be happy about that**')
                                            await ctx.send(embed=em)
                                    except asyncio.TimeoutError:
                                        await ctx.send(f'{ctx.author.mention} rejected the option to continue!')
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

    @commands.command()
    async def snipe(self, ctx):
        with open('JSON/snipe.json', 'r') as k:
            word = json.load(k)
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
        except KeyError:
            await ctx.send('There is nothing to snipe!')

def setup(bot):
    bot.add_cog(games(bot))
