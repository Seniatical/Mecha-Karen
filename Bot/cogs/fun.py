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

import random
import datetime
import time

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import os
import requests
from requests.utils import requote_uri
import aiohttp
import asyncio
from Helpers import functions
import math

from Others import IMG, Bio, Channel, Co, gender, Jokes, Numbers, Numbers2, Quotes, Stuff, words

async def ship(name1, name2):
    vowels = ['a','e','i','o','u','y']
    count1 = -1
    count2 = -1
    mid1 = math.ceil(len(name1)/2)-1
    mid2 = math.ceil(len(name2)/2)-1
    noVowel1 = False
    noVowel2 = False
    
    i = mid1
    while i >= 0:
        count1 += 1
        if name1[i].lower() in vowels:
            i = -1
        elif i == 0:
            noVowel1 = True
        i -= 1

    i = mid2
    while i < len(name2):
        count2 += 1
        if name2[i].lower() in vowels:
            i = len(name2)
        elif i == len(name2) - 1:
            noVowel2 = True
        i += 1

    name = ""
    if noVowel1 and noVowel2:
        name = name1[:mid1+1]
        name += name2[mid2:]
    elif count1 <= count2:
        name = name1[:mid1-count1+1]
        name += name2[mid2:]
    else:
        name = name1[:mid1+1]
        name += name2[mid2+count2:]
    return name

class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.m_converter = commands.MemberConverter()
        self.times = dict()
        self.session = aiohttp.ClientSession()
        ## self.client = bot.api_c
        self.sched = {}

    async def convert(self, num) -> str:
        if num >= (60*60):
            hours = num // (60*60)
            num %= (60*60)
            mins = num // 60
            return '**{}** Hrs and **{}** Mins.'.format(hours, mins)
        elif num > 60:
            mins = num // 60
            num %= 60
            return '**{}** Mins and **{}** Seconds.'.format(mins, num)
        else:
            return '**{}** Seconds.'.format(num)

    @commands.Cog.listener()
    async def on_message(self, message) -> object:
        if message.guild.id not in [740523643980873789, 798546507715444746]:
            return
        if message.channel.id not in [772048764587606017, 819142185438019634]:
            return
        
        reference = getattr(message, 'reference', None)
        if not reference:
            return
        
        raw_message = reference.resolved
        if not raw_message:
            return
        
        if (message.content.startswith('!') and message.guild.id == 819142185438019634) or (message.content.startswith('-') and message.guild.id == 772048764587606017):
            return
        
        last_used = self.sched.get(message.author.id)
        if last_used:
            if (time.time() - last_used) < 5:
                return
            self.sched.pop(message.author.id)
        else:
            self.sched.update({message.author.id: time.time()})
        
        if raw_message.author.id == self.bot.user.id:
            ctx = await self.bot.get_context(message)
            await ctx.trigger_typing()
            
            res = await self.session.post(
                'https://api.mechakaren.xyz/v1/chatbot',
                headers = {'Authorization': 'idk mate'},
                json = {'message': message.content}
            )
            try:
                real = await res.json()
            except Exception:
                return
            return await message.reply(content=real['response']['answer'] or 'Hello There.')
    
    @commands.command(aliases=['slots', 'bet'], name='Slot')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} | {b} | {c} ]\n{ctx.author.name}**,"

        if a == b == c:
            await ctx.send(embed=discord.Embed(title='Slot Machine:',
                                               description=slotmachine + ' has gotten 3/3 he wins!!! :tada:',
                                               colour=discord.Colour.red()))
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(embed=discord.Embed(title='Slot Machine:',
                                               description=slotmachine + ' has gotten 2/3 he wins!!! :tada:',
                                               colour=discord.Colour.red()))
        else:
            await ctx.send(embed=discord.Embed(title='Slot Machine:',
                                               description=slotmachine + ' has gotten 0/3 he looses. :pensive:',
                                               colour=discord.Colour.red()))

    @commands.command(aliases=['Latency'], name='Ping')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        msg = await ctx.send("Gathering Information...")
        times = []
        counter = 0
        embed = discord.Embed(colour=discord.Colour.red())
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Trying Ping{('.'*counter)} {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            if speed < 160:
                embed.add_field(name=f"Ping {counter}:", value=f"🟢 | {speed}ms", inline=True)
            elif speed > 170:
                embed.add_field(name=f"Ping {counter}:", value=f"🟡 | {speed}ms", inline=True)
            else:
                embed.add_field(name=f"Ping {counter}:", value=f"🔴 | {speed}ms", inline=True)
                
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms")
        embed.add_field(name="Normal Speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.add_field(name='Buffer', value=f'{self.bot.buffer.ping(packets=1, wait_for=False, timeout=20000, unit='ms')}ms')

##        start = time.perf_counter()
##        async with aiohttp.ClientSession() as session:
##            async with session.get('https://api.mechakaren.xyz/') as r:
##                pass
##        end = time.perf_counter()
##        
##        embed.add_field(name="API Latency", value=f'{round((end - start) * 1000)}ms')
##
##        start = time.perf_counter()
##        async with aiohttp.ClientSession() as session:
##            async with session.get('https://mechakaren.xyz/') as r:
##                pass
##        end = time.perf_counter()
##        embed.add_field(name="Website Latency", value=f'{round((end - start) * 1000)}ms')
                           
## Useless testing - Inaccurate pings
        
        embed.set_footer(text=f"Total estimated elapsed time: {round(sum(times))}ms")
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar_url)
        
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

    @commands.command(name='Useless')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def useless(self, ctx):
        user = ctx.author
        await ctx.send('Hello ' + user.name)
        await ctx.send('Type `press` to press the useless button.')

        def check(m):
            if m.author.id == user.id and m.content.lower() == 'press':
                return True
            return False
        try:
            await self.bot.wait_for('message', timeout=10.0, check=check)
            await ctx.send(embed=discord.Embed(
                title='Button has been pressed!',
                description='Button has been pressed by {}'.format(ctx.author),
                colour=discord.Colour.green()
            ).set_image(url='http://66.media.tumblr.com/d1483298e112b3bf08d35a2bd345a097/tumblr_n5ig6cjyk81t2csv8o2_500.gif'))
        except asyncio.TimeoutError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Button press has failed.',
                colour=discord.Colour.red()
            ))

    @commands.command(aliases=['le'], name='LifeExpectancy')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lifeexpectancy(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        counter = random.randint(1, 150)
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'**{counter} yrs old!**'
        )
        await ctx.send(embed=embed)

    @commands.command(name='BWeight')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bweight(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        weight = ['Pinweight\t(44 - 46 Kg)', 'Light Flyweight\t(Below 48Kg)', 'Flyweight\t(49 - 52 Kg)', 'Bantamweight\t(52 - 53.5 Kg)', 'Featherweight\t(54 - 57 Kg)', 'Lightweight\t(59 - 61 Kg)', 'Lighter welterweight\t(54 - 67 Kg)', 'Welterweight\t(64 - 69 Kg)', 'Middleweight\t(70 - 73 Kg)', 'Light heavyweight\t(76 - 80 Kg)', 'Heavyweight\t(Above 81 Kg)', 'Super Heavyweight\t(Above 91 Kg)']
        choice = random.choice(weight)
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'{choice}'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['Weight', 'WI'], name='WeighIn')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weighin(self, ctx, user: discord.Member = None):
        if user == None:
            user = ctx.author
        weight = random.randint(1, 200)
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'**`{weight}` Kg**'
        )
        await ctx.send(embed=embed)

    @commands.command(name='Beer')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.mention}**: fieeeeestaaa!🎉🍺")
        if user.bot:
            return await ctx.send(f"You that lonely? Give an actual person not a bot.")
        beer_offer = f"**{user.mention}**, You have a 🍺 offered from **{ctx.author.mention}**"
        beer_offer = beer_offer + f"\n\n**Reason:** {reason}" if reason else beer_offer
        msg = await ctx.send(beer_offer)

        def reaction_check(m):
            if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "🍻":
                return True
            return False

        try:
            await msg.add_reaction("🍻")
            await self.bot.wait_for('raw_reaction_add', timeout=10.0, check=reaction_check)
            await msg.edit(content=f"**{user.mention}** and **{ctx.author.mention}** Are enjoying a lovely 🍻")
            await msg.clear_reactions()
        except asyncio.TimeoutError:
            await msg.delete()
            await ctx.send(f"well it seems **{user.name}** didn't want a beer with **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            beer_offer = f"{user.mention} and {ctx.author.mention} are enjoying a 🍻."
            beer_offer = beer_offer + f"\n\n**reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command(name='Reverse')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def reverse(self, ctx, *, message):
        await ctx.send(embed=discord.Embed(
            description=message[::-1],
            colour=discord.Colour.red()
        ))

    @commands.command(name='Simp')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def simp(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'{user.display_name} is {random.randint(0, 101)}% simp'
        )
        await ctx.send(embed=embed)

    @commands.command(name='Retard')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def retard(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            description=f'{user.display_name} is {random.randint(0, 101)}% retarded',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name='Human')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def human(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            description=f'{user.display_name} is {random.randint(0, 101)}% human',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name='Buff')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buff(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'{user.display_name} is {random.randint(0, 101)}/100 Buff :muscle:'
            )
        await ctx.send(embed=embed)

    @commands.command(name='Waifu')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def waifu(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'{user.display_name} is {random.choice(IMG.Number1)}'
        )
        await ctx.send(embed=embed)

    @commands.command(name='Dad')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dad(self, ctx, *, message: str):
        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'Hello {message}, Im Dad'
        )
        await ctx.send(embed=embed)

    @commands.command(name='Gay')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gay(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        embed = discord.Embed(
            color=random.randint(0x000000, 0xFFFFFF),
            description=f'{user.display_name} is {random.randint(1, 101)}% gay :rainbow_flag:'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['jokes'], name='Joke')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def joke(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    'https://sv443.net/jokeapi/v2/joke/Miscellaneous?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart') as r:
                r = await r.json()
        embed = discord.Embed(colour=random.randint(0x000000, 0xFFFFFF), timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Setup:', value=r['setup'])
        embed.add_field(name='Delivery:', value=r['delivery'], inline=False)
        embed.set_footer(text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['facts'], name='Fact')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def facts(self, ctx):
        embed = discord.Embed(
            title='**Fun Fact:**',
            color=discord.Color.teal(),
            description=f'{random.choice(Co.fact)}'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['gender'], name='GenderFinder')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def genderfinder(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        genders = random.choice(gender.gend)
        embed = discord.Embed(
            title=f"**{user.display_name}'s Gender!**",
            description=genders,
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['mk', 'MagicK', 'MKaren'], name='MagicKaren')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def magickaren(self, ctx, *, question=None):
        if question == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('Atleast give me a question. Try again!')
        responses = ["It is certain.",
                     "It is decidedly so.",
                     "Without a doubt.",
                     "Yes - definitely.",
                     "You may rely on it.",
                     "As I see it, yes.",
                     "Most likely.",
                     "Outlook good.",
                     "Yes.",
                     "Signs point to yes.",
                     "Reply hazy, try again.",
                     "Ask again later.",
                     "Better not tell you now.",
                     "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don't count on it.",
                     "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.",
                     "Very doubtful."]
        embed = discord.Embed(title='The Magic Karen',
                              colour=discord.Colour.red(),
                              description=random.choice(responses))
        await ctx.send(embed=embed)

    @commands.command(name='IQ')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def iq(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        iq = ['130 and above (Very Superior)',
              '120–129 (Superior)',
              '110–119 (High Average)',
              '90–109 (Average)',
              '80–89 (Low Average)',
              '70–79 (Borderline)',
              '69 and below	(Extremely Low)']
        e = discord.Embed(
            color=discord.Colour.red(),
            description=f'{user.display_name} IQ is {random.choice(iq)}'
            )
        await ctx.send(embed=e)

    @commands.command(aliases=['Penis'], name='PP')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pp(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        former = ['8', 'D']
        for i in range(random.randrange(10)):
            former.insert(1, '=')
        e = discord.Embed(color=0x50C878)
        e.add_field(name="**{}'s penis is:**".format(user),
                    value=''.join(map(str, former)))
        await ctx.send(embed=e)

    @commands.command(aliases=['insult'], name='Roast')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roast(self, ctx):
        A = ['You’re the reason God created the middle finger.',
             'You’re a grey sprinkle on a rainbow cupcake.',
             'If your brain was dynamite, there wouldn’t be enough to blow your hat off.',
             'You are more disappointing than an unsalted pretzel.',
             'Light travels faster than sound which is why you seemed bright until you spoke.',
             'We were happily married for one month, but unfortunately we’ve been married for 10 years.',
             'Your kid is so annoying, he makes his Happy Meal cry.',
             'You have so many gaps in your teeth it looks like your tongue is in jail.',
             'Your secrets are always safe with me. I never even listen when you tell me them.',
             'I’ll never forget the first time we met. But I’ll keep trying.',
             'I forgot the world revolves around you. My apologies, how silly of me.',
             'I only take you everywhere I go just so I don’t have to kiss you goodbye.',
             'Hold still. I’m trying to imagine you with personality.',
             'Our kid must have gotten his brain from you! I still have mine.',
             'Your face makes onions cry.',
             'The only way my husband would ever get hurt during an activity is if the TV exploded.',
             'You look so pretty. Not at all gross, today.',
             'Her teeth were so bad she could eat an apple through a fence.',
             'I’m not insulting you, I’m describing you.',
             'I’m not a nerd, I’m just smarter than you.',
             'Keep rolling your eyes, you might eventually find a brain.',
             'Your face is just fine but we’ll have to put a bag over that personality.',
             'You bring everyone so much joy, when you leave the room.',
             'I thought of you today. It reminded me to take out the trash.',
             'Don’t worry about me. Worry about your eyebrows.',
             'there is approximately 1,010,030 words in the language english, but i cannot string enough words together to express how much i want to hit you with a chair']
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.red(),
            description=random.choice(A)
        ).set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url))

    @commands.command(aliases=['murder', 'die'], name='Kill')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kill(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        died = ['rolling out of the bed and the demon under the bed ate them.',
                'getting impaled on the bill of a swordfish.',
                'falling off a ladder and landing head first in a water bucket.',
                'his own explosive while trying to steal from a condom dispenser.',
                'a coconut falling off a tree and smashing there skull in.',
                'taking a selfie with a loaded handgun shot himself in the throat.',
                'shooting himself to death with gun carried in his breast pocket.',
                'getting crushed while moving a fridge freezer.',
                'getting crushed by his own coffins.',
                'getting crushed by your partner.',
                'laughing so hard at The Goodies Ecky Thump episode that he died of heart failure.',
                'getting run over by his own vehicle.',
                'car engine bonnet shutting on there head.',
                'tried to brake check a train.',
                'dressing up as a cookie and cookie monster ate them.',
                'trying to re-act Indiana Jones, died from a snake bite.',
                'tried to short circuit me, not that easy retard',
                'tried to fight a bear with there hands',
                'getting Billy Heartied in the ball sacks'
                ]
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.red(),
            description='{} was killed by {}'.format(user.display_name, random.choice(died))
        ).set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url))

    @commands.command(aliases=['punch'], name='PunchMachine')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def punchmachine(self, ctx):
        answer = random.randint(0, 999)

        embed = discord.Embed(
            color=discord.Color.red(),
            description='You swing and hit a **{}**.'.format(answer)
        )
        await ctx.send(embed=embed)

    @commands.command(name='Say')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def say(self, ctx, *, quote: str = None):
        if not quote:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('What are u saying!')
        await ctx.send('{}\n\t- **{}**'.format(quote, ctx.author))

    @commands.command(name='F')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def f(self, ctx, *, message: str = None):
        if message == None:
            await ctx.send('<:F_:745287381816574125>')
            return await ctx.send('**{} Has Paid Their Respects.**'.format(ctx.author.display_name))
        await ctx.send('<:F_:745287381816574125>')
        await ctx.send('**{} Has Paid There Respects:** {}'.format(ctx.author.display_name, message.title()))

    @commands.command(name='Spoiler')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def spoiler(self, ctx, *, message: str):
        await ctx.send('||{}||'.format(message))

    @commands.command(name='Pings')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, read_messages=True)
    async def pings(self, ctx, limit: str = '10', user: discord.Member = None):
        user = ctx.author if not user else user
        try:
            limit = int(limit)
        except ValueError:
            return await ctx.send('The limit for the searching must be a number.')
        if limit > 100:
            return await ctx.send('Max limit is 100 messages. This is to keep the command consistent.')
        counter = 0
        async for message in ctx.channel.history(limit=limit):
            if user.mentioned_in(message):
                counter += 1
        await ctx.send('You have been pinged {} times in the last {} messages'.format(counter, limit))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def timer(self, ctx, time: str = None):
        try:
            is_there = self.times[ctx.author.id]
            now = time.time()
            gap = now - is_there['time']
            del self.times[ctx.author.id]
            return await ctx.send(embed=discord.Embed(
                description='⌚ | Timer was set for {}'.format(await self.convert(int(gap))),
                colour=discord.Colour.red()
            ))
        except KeyError:
            if not time:
                self.times[ctx.author.id] = {
                    'time': time.time()
                }
                await ctx.send(embed=discord.Embed(
                    description='⌚ | The timer has been set...',
                    colour=discord.Colour.red()
                ))
            else:
                try:
                    time = int(time)
                except ValueError:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> Time to set must a number (counted with minutes)',
                        colour=discord.Color.red()
                        ))
                await ctx.send(embed=discord.Embed(
                    description='⌚ | Will remind you in **{}** minutes.'.format(time),
                    colour=discord.Colour.green()
                ))
                await asyncio.sleep(time*60)
                return await ctx.send(embed=discord.Embed(
                    description='⏰ | Times Up!',
                    colour=discord.Color.red()
                    ), content=ctx.author.mention)
            
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ship(self, ctx, member1: discord.Member, member2: discord.Member):
        res = await ship(name1=member1.display_name, name2=member2.display_name)
        await ctx.send(embed=discord.Embed(
            description='❤️ | {} + {} = {}'.format(member1.display_name, member2.display_name, res),
            colour=discord.Colour.red()
        ))
    
    @commands.command(aliases=['cb'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def chatbot(self, ctx, *, message: str):
        res = await self.session.post(
            'https://api.mechakaren.xyz/v1/chatbot',
            headers = {'Authorization': 'idk lads'},
            json = {'message': message}
        )
        try:
            real = await res.json()
        except Exception:
            return await ctx.message.reply(content='I have no response for you, now go away.')
        return await ctx.message.reply(content=real['response']['answer'] or 'Hello There.')
                        
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def urban(self, ctx, *, word : str=None):
        message = await ctx.send('Fetching Your Word From `Urban Dictionary`!')
        data = UD.search(word)
        try:
            name = 'User Not Found' if data.author['name'] == "" else data.author['name']
            embed = discord.Embed(
                title='Search Results for **{}**'.format(data.the_word.title()),
                description='**Contributed by {}**'.format(name),
                colour=discord.Color.dark_blue(),
                timestamp=datetime.datetime.utcnow()
            ).set_footer(text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            embed.add_field(name='Meaning:', value=data.meaning)
            embed.add_field(name='Example:', value='N/A' if data.example == "" else data.example, inline=False)
            embed.add_field(name='Likes:', value='👍 {}'.format(data.rating['likes']))
            embed.add_field(name='Dislikes:', value='👎 {}'.format(data.rating['dislikes']))
            year, month, day = int(data.date['year']), int(data.date['date'].split('-')[1]), int(data.date['day'])
            embed.add_field(name='Posted At:', value=datetime.date(year, month, day).strftime('%A, %B %Y') + ' ({})'.format(data.date['date']), inline=False)
            await message.edit(content=None, embed=embed)
        except KeyError:
            await message.edit('{} The word **`{}`** wasnt found!'.format(ctx.author.mention, word.title()))

    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True, create_instant_invite=True)
    async def vanish(self, ctx):
        global xyz

        async def message():
            try:
                invites = await ctx.guild.invites()
                y = await ctx.author.send('You have vanished.\nRejoin: {}'.format(random.choice(invites)))
                return y
            except Exception:
                return
        try:
            check:discord.Message = await ctx.send('Are your sure that you want to vanish?')
            await check.add_reaction('✅')
            await check.add_reaction('❌')
            xyz = False

            def _check(m):
                global xyz
                if m.member.id == ctx.author.id and str(m.emoji) == '✅':
                    xyz = True
                    return True
                elif m.member.id == ctx.author.id and str(m.emoji) == '❌':
                    return True
                return False
            await self.bot.wait_for('raw_reaction_add', check=_check)
            if not xyz:
                await check.clear_reactions()
                return await check.edit(content='Looks like **{}** doesnt want to vanish!'.format(ctx.author))
            await ctx.guild.kick(ctx.author, reason='They have VANISHED.')
            try:
                await message()
            except discord.errors.Forbidden:
                return
            await check.edit(content='**{}** Has Vanished.'.format(ctx.author))
            await check.clear_reactions()
            await check.add_reaction(emoji.KAREN_ADDITIONS_ANIMATED['wave'])
        except discord.errors.Forbidden:
            await check.edit(content="Failed to secretly move {}'s Fat Ass.".format(ctx.author.mention))
            await check.clear_reactions()
            return await check.add_reaction('<:F_:745287381816574125>')

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def image(self, ctx, query:str = None):
        if not query:
            return await ctx.send('Need to give an image to search for!')
        url = 'https://api.pexels.com/v1/search?query={}&per_page={}'.format(query, random.randint(1, 100))
        auth = 'API KEY_HERE'
        ## Returns stock images so it wont find everything and wont find NSFW as well
        r = requests.get(url, headers={'Authorization' : auth}).json()
        try:
            await ctx.send(
                embed=discord.Embed(
                    title='Search results for {}'.format(
                        query.title()
                    ),
                    colour=discord.Color.red(),
                ).set_image(url=random.choice(r['photos'])['src']['large2x'])
            )
        except IndexError:
            return await ctx.send('No Image was Found Under the Context **{}**'.format(query.title()))
    
def setup(bot):
    bot.add_cog(fun(bot))
