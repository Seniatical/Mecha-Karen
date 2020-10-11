import time
import asyncio
import random
import json
import os

import discord
from discord.ext import commands
from discord.ext.commands import cooldown, BucketType

os.chdir(r'C:\\Users\\isa1b.DESKTOP-GMQ5DPV.000.001\\PycharmProjects\\Discord Bot')

async def load_movie_account(user):
    guilds = await get_movie_data()
    if user.id in guilds:
        return False
    else:
        guilds[str(user.id)] = {}
        guilds[str(user.id)]['Level'] = '1'

        with open('JSON/Quiz_Data.json', 'w') as f:
            json.dump(guilds, f, indent=4)
        return True

async def get_movie_data():
    with open('JSON/Quiz_Data.json', 'r') as f:
        guilds = json.load(f)
    return guilds

class Quizzes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['MV', 'Movie_C', 'MC', 'M_check'])
    async def movie_check(self, ctx, user : discord.Member=None):
        global msg
        if user == None:
            user = ctx.author
        if user.bot == True:
            await ctx.send('I cannot check bots!')
        else:
            await load_movie_account(user)
            guilds = await get_movie_data()
            data = guilds[str(user.id)]['Level']
            if user != ctx.author:
                data1 = guilds[str(ctx.author.id)]['Level']
                if int(data) > int(data1):
                    msg = 'They are currently higher then you! Beat them now!'
                elif int(data1) == int(data):
                    msg = 'Your drawed with them! Win 1 more to get passed them!'
                else:
                    msg = 'Your beating them. Have mercy!'
            else:
                if int(data) > 10:
                    msg = 'You have achieved the maximum quiz level!'
                else:
                    msg = 'Try reach the ending! Only {} quizzes left.'.format(10 - int(data))
            embed = discord.Embed(
                title=f"{user.display_name}'s Quiz Level!",
                color=user.color,
                description=f'**{user.display_name}** is currently on quiz level ***`{data}`***!'
            )
            embed.set_footer(text=msg)
            await ctx.send(embed=embed)

    @commands.command()
    async def check(self, ctx):
        await load_movie_account(ctx.author)
        await ctx.send(load_movie_account(ctx.author))

    @commands.command()
    @cooldown(1, 300, BucketType.user)
    async def Take(self, ctx, name=None):
        user = ctx.author
        quizzes = ['food', 'movie', 'movies']
        if name == None:
            await ctx.send('Enter a quiz idiot')
        else:
            name = name.lower()
            msg = await ctx.send(f'Starting Process')
            for counter in range(3):
                counter += 1
                correct = 0
                start = time.perf_counter()
                await msg.edit(content=f"Searching for quiz named {name}... {counter}/3")
                end = time.perf_counter()
            if name in quizzes:
                await ctx.send('Quiz Found\nStarting Now')
                if name == 'movie' or name == 'movies':
                    await load_movie_account(ctx.author)
                    users = await get_movie_data()
                    if users[str(user.guild.id)][str(user.id)]["Level"] == 1:
                        counter = 0
                        msg = await ctx.send('1. What Milkshake Flavor did John Travolta Drink In Pulp Fiction?')
                        def check(m):
                            if m.author.id == user.id and m.content.lower() == 'vanilla':
                                return True
                            return False
                        try:
                            await self.bot.wait_for('message', timeout=15.0, check=check)
                            correct += 1
                            await ctx.send('Correct!')
                            msg = await ctx.send('What Martin Scorsese Movie inspired Joker?')
                            def check(m):
                                if m.author.id == user.id and m.content.lower() == 'the king of comedy' or user.id and m.content.lower() == 'taxi driver':
                                    return True
                                return False
                            try:
                                await ctx.send('Correct!')
                                await self.bot.wait_for('message', timeout=15.0, check=check)
                                msg = await ctx.send('In The Matrix, does Neo take the blue pill or the red pill?')
                                def check(m):
                                    if m.author.id == user.id and m.content.lower() == 'red':
                                        return True
                                    return False
                                try:
                                    await self.bot.wait_for('message', timeout=15.0, check=check)
                                    await ctx.send('Correct!')
                                    msg = await ctx.send('Who directed Parasite – the first foreign-language film to win the Academy Award for Best Picture?')
                                    def check(m):
                                        if m.author.id == user.id and m.content.lower() == 'bong joon-ho' or user.id and m.content.lower() == 'bong joon ho':
                                            return True
                                        return False
                                    try:
                                        await self.bot.wait_for('message', timeout=15.0, check=check)
                                        await ctx.send('Correct!')
                                        msg = await ctx.send('Which Oscar-winning actress is the voice of Helen Parr (Elastigirl) in The Incredibles?')
                                        def check(m):
                                            if m.author.id == user.id and m.content.lower() == 'holly hunter':
                                                return True
                                            return False
                                        try:
                                            await self.bot.wait_for('message', timeout=10.0, check=check)
                                            await ctx.send('Correct')
                                            msg = await ctx.send('Name the 2015 film spinoff to the Rocky series starring Michael B. Jordan.')
                                            def check(m):
                                                if m.author.id == user.id and m.content.lower() == 'creed':
                                                    return True
                                                return False
                                            try:
                                                await self.bot.wait_for('message', timeout=15.0, check=check)
                                                await ctx.send('Correct!')
                                                msg = await ctx.send('Meryl Streep won a Best Actress BAFTA for which 2011 political drama?')
                                                def check(m):
                                                    if m.author.id == user.id and m.content.lower() == 'the iron lady':
                                                        return True
                                                    return False
                                                try:
                                                    await self.bot.wait_for('message', timeout=15.0, check=check)
                                                    await ctx.send('Correct!')
                                                    msg = await ctx.send('BD Wong voices Captain Li Shang in the animated musical Mulan, but which 70’s teen heartthrob provided the character’s singing voice?')
                                                    def check(m):
                                                        if m.author.id == user.id and m.content.lower() == 'donny osmond':
                                                            return True
                                                        return False
                                                    try:
                                                        await self.bot.wait_for('message', timeout=15.0, check=check)
                                                        await ctx.send('Correct!')
                                                        msg = await ctx.send('Which actor broke two toes whilst filming The Lord of the Rings: The Two Towers?')
                                                        def check(m):
                                                            if m.author.id == user.id and m.content.lower() == 'viggo mortensen':
                                                                return True
                                                            return False
                                                        try:
                                                            await self.bot.wait_for('message', timeout=15.0, check=check)
                                                            await ctx.send('Correct!')
                                                            msg = await ctx.send('Name a movie in which Meg Ryan and Tom Hanks have starred together. (3 Options!)')
                                                            def check(m):
                                                                if m.author.id == user.id and m.content.lower() == 'joe versus the volcano' or user.id and m.content.lower() == 'sleepless in seattle' or user.id and m.content.lower() == 'you’ve got mail' or user.id and m.content.lower() == 'you have got mail':
                                                                    return True
                                                                return True
                                                        except asyncio.TimeoutError:
                                                            await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Viggo Mortensen`!**')
                                                    except asyncio.TimeoutError:
                                                        await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Donny Osmond`!**')
                                                except asyncio.TimeoutError:
                                                    await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `The Iron Lady`!**')
                                            except asyncio.TimeoutError:
                                                await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Creed`!**')
                                        except asyncio.TimeoutError:
                                            await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Holly Hunter`!**')
                                    except asyncio.TimeoutError:
                                        await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Boon Joon-Ho`!**')
                                except asyncio.TimeoutError:
                                    await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Red`!**')
                            except asyncio.TimeoutError:
                                await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `The King of Comedy` or `Taxi Driver`!**')
                        except asyncio.TimeoutError:
                            await ctx.send(f'You got {str(correct)}/10 questions correct.\n**Answer was `Vanilla`!**')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 2:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 3:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 4:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 5:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 6:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 7:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 8:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 9:
                        await ctx.send('Coming Soon!')
                    elif users[str(user.guild.id)][str(user.id)]["Level"] == 10:
                        await ctx.send('Coming Soon!')
            else:
                await msg.delete()
                await ctx.send('Quiz not found!')

def setup(bot):
    bot.add_cog(Quizzes(bot))
