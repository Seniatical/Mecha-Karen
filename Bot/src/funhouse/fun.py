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
import math

import utility.genders
from utility import *
from utility import emojis as emoji

async def ship(name1, name2):
    vowels = ['a', 'e', 'i', 'o', 'u', 'y']
    count1 = -1
    count2 = -1
    mid1 = math.ceil(len(name1) / 2) - 1
    mid2 = math.ceil(len(name2) / 2) - 1
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

    if noVowel1 and noVowel2:
        name = name1[:mid1 + 1]
        name += name2[mid2:]
    elif count1 <= count2:
        name = name1[:mid1 - count1 + 1]
        name += name2[mid2:]
    else:
        name = name1[:mid1 + 1]
        name += name2[mid2 + count2:]
    return name


class fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.m_converter = commands.MemberConverter()
        self.times = dict()
        self.session = aiohttp.ClientSession()
        ## self.client = bot.api_c
        self.sched = {}

        self.weights = ['Pinweight\t(44 - 46 Kg)', 'Light Flyweight\t(Below 48Kg)', 'Flyweight\t(49 - 52 Kg)',
                        'Bantamweight\t(52 - 53.5 Kg)', 'Featherweight\t(54 - 57 Kg)', 'Lightweight\t(59 - 61 Kg)',
                        'Lighter welterweight\t(54 - 67 Kg)', 'Welterweight\t(64 - 69 Kg)',
                        'Middleweight\t(70 - 73 Kg)',
                        'Light heavyweight\t(76 - 80 Kg)', 'Heavyweight\t(Above 81 Kg)',
                        'Super Heavyweight\t(Above 91 Kg)']
        self.responses = ["It is certain.",
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
        self.iqs = ['130 and above (Very Superior)',
                    '120–129 (Superior)',
                    '110–119 (High Average)',
                    '90–109 (Average)',
                    '80–89 (Low Average)',
                    '70–79 (Borderline)',
                    '69 and below	(Extremely Low)']

    @staticmethod
    async def convert(num) -> str:
        if num >= (60 * 60):
            hours = num // (60 * 60)
            num %= (60 * 60)
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
        if not message.guild:
            return

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

        if (message.content.startswith('!') and message.guild.id == 819142185438019634) or (
                message.content.startswith('-') and message.guild.id == 772048764587606017):
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
                headers={'Authorization': self.bot.env('API_TOKEN')},
                json={'message': message.content}
            )
            try:
                real = await res.json()
            except Exception:
                return
            return await message.reply(content=real['response']['answer'] or 'Hello There.')

    @commands.command(aliases=['slots', 'bet'], name='Slot')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def slot(self, ctx):
        options = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(options)
        b = random.choice(options)
        c = random.choice(options)

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
            await msg.edit(content=f"Trying Ping{('.' * counter)} {counter}/3")
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
        embed.add_field(name="Normal Speed",
                        value=f"{round((round(sum(times)) + round(self.bot.latency * 1000)) / 4)}ms")
        embed.add_field(name='Buffer', value=f'{self.bot.buffer._round_time(__import__('time').perfcounter, 'ms')}ms')

        ##		  website = await self.bot.loop.run_in_executor(None, lambda: os.popen('ping mechakaren.xyz ; echo $?').read())
        ##        ping = website.result()
        ##        embed.add_field(name='Dashboard', value=ping)

        embed.set_footer(text=f"Total estimated elapsed time: {round(sum(times))}ms")
        embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar)

        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000)) / 4)}ms**",
                       embed=embed)

    @commands.command(name='Useless')
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def useless(self, ctx):
        user = ctx.author
        await ctx.send('Hello ' + user.display_name + '\nType `press` to press the useless button.')

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
            ).set_image(
                url='https://66.media.tumblr.com/d1483298e112b3bf08d35a2bd345a097/tumblr_n5ig6cjyk81t2csv8o2_500.gif'))
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
            description=f'{user.display_name} is going to live to **{counter}** years old!'
        )
        await ctx.send(embed=embed)

    @commands.command(name='BWeight')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bweight(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        weight = random.choice(self.weights)

        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'{user.display_name}\'s Boxing weight would be **{weight}**'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['Weight', 'WI'], name='WeighIn')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def weighin(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        weight = random.randint(1, 200)

        embed = discord.Embed(
            color=discord.Color.red(),
            description=f'{user.display_name} Weighs **{weight}** KG!'
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
            await msg.edit(content=f"well it seems **{user.name}** didn't want a beer with **{ctx.author.name}** ;-;")
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
            description=f'If I had to rate how much a simp **{user.display_name} is. I would give them **{random.randint(0, 101)}/100'
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
            description=f'{user.display_name} is {random.randint(0, 101)}% Human',
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
        rating = random.randint(0, 100)
        if rating < 10:
            emoji = '🤮'
        elif 10 < rating < 20:
            emoji = '🤢'
        elif 20 > rating and rating < 30:
            emoji = '😬'
        elif 30 > rating and rating < 50:
            emoji = '☺️'
        elif 50 > rating and rating < 70:
            emoji = '😚'
        elif 70 > rating and rating < 90:
            emoji = '🥰'
        else:
            emoji = '😍'
        embed = discord.Embed(colour=discord.Colour.red(),
                              description=f'If I had to rate how much of a waifu **{user.display_name}** is. I would give them {rating}/100 {emoji}')
        await ctx.send(embed=embed)

    @commands.command(name='Dad')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def dad(self, ctx, *, message: str):
        await ctx.send(f'Hello **{message}**, Im Dad')

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
        response = await self.session.get(
            'https://sv443.net/jokeapi/v2/joke/Miscellaneous?blacklistFlags=nsfw,religious,political,racist,sexist&type=twopart')
        r = await response.json()
        embed = discord.Embed(colour=random.randint(0x000000, 0xFFFFFF), timestamp=datetime.datetime.utcnow())
        embed.add_field(name='Setup:', value=r['setup'])
        embed.add_field(name='Delivery:', value=r['delivery'], inline=False)
        embed.set_footer(text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar)
        await ctx.send(embed=embed)

    @commands.command(aliases=['facts'], name='Fact')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def facts(self, ctx):
        embed = discord.Embed(
            title='**Fun Fact:**',
            color=discord.Color.teal(),
            description=f'{random.choice(facts)}'
        )
        await ctx.send(embed=embed)

    @commands.command(name='Gender')
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def gender(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        gender = random.choice(utility.genders.genders)
        embed = discord.Embed(
            description=f'**{user.diplay_name}**\'s Gender is **{gender}**',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['mk', 'MagicK', 'MKaren'], name='MagicKaren')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def magic(self, ctx, *, question: str):
        embed = discord.Embed(title='Magic Karen',
                              colour=discord.Colour.red())
        embed.add_field(name='Question', value=question.title())
        embed.add_field(name='Response', value=random.choice(self.responses))

        await ctx.send(embed=embed)

    @commands.command(name='IQ')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def iq(self, ctx, user: discord.Member = None):
        user = user or ctx.author
        e = discord.Embed(
            color=discord.Colour.red(),
            description=f'{user.display_name} IQ is {random.choice(self.iqs)}'
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
        return await ctx.message.reply(content=random.choice(roasts))

    @commands.command(aliases=['murder', 'die'], name='Kill')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kill(self, ctx, *, user: discord.Member = None):
        user = user or ctx.author
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.red(),
            description='{} was killed by {}'.format(user.display_name, random.choice(deaths))
        ).set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar))

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
    async def say(self, ctx, *, quote: str):
        await ctx.send('{}\n- **{}**'.format(quote, ctx.author))

    @commands.command(name='F')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def f(self, ctx, *, message: str = None):
        if message == None:
            return await ctx.send('<:F_:745287381816574125> **{} Has Paid Their Respects.**'.format(ctx.author.display_name))

        await ctx.send('<:F_:745287381816574125> **{} Has Paid There Respects:** {}'.format(ctx.author.display_name, message.title()))

    @commands.command(name='Spoiler')
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def spoiler(self, ctx, *, message: str, split: str = None):
        def get_body(letter: str) -> str:
            if split == '*':
                return '||' + letter + '||'
            if letter == split:
                return '||' + letter + '||'
            return letter

        message = discord.utils.remove_markdown(text=message, ignore_links=False)

        if not split:
            return await ctx.send('||{}||'.format(message))
        map_ = await self.bot.loop.run_in_executor(None, map, get_body, message)
        return await ctx.send('\n'.join(map_))

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
        await ctx.send('**{}** been pinged **{}** times in the last **{}** messages'.format(user.display_name, counter, limit))

    @commands.command(name='Mutate')
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(manage_webhooks=True)
    async def mutate(self, ctx, *args):
        if not args:
            ctx.command.reset_cooldown(ctx)
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Need to give me something to transform you into!',
                colour=discord.Colour.red()
            ))
        try:
            user = await self.m_converter.convert(ctx, args[0])
            args = args[1:]
        except commands.errors.MemberNotFound:
            user = ctx.author
        holder_ = []
        for i in args:
            try:
                x = [j for j in self.bot.emojis if
                     j.name.lower() == i.split(':')[1].lower() and ':' in i[0] and ':' in i[-1]]
            except IndexError:
                holder_.append(i)
                continue
            if x:
                holder_.append(x[0])
            else:
                holder_.append(i)
        await ctx.message.delete()
        channel_webhooks = await ctx.channel.webhooks()
        try:
            for webhook in channel_webhooks:
                if webhook.user == self.bot.user:
                    return await webhook.send(' '.join(map(str, holder_)), username=user.display_name,
                                              avatar_url=user.avatar)
            new_hook = await ctx.channel.create_webhook(name='Mecha Karen',
                                                        reason='Webhook Adaptation for Command: Emoji')
            return await new_hook.send(' '.join(map(str, holder_)), username=user.display_name,
                                       avatar_url=user.avatar)
        except discord.errors.HTTPException:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot send an empty message!',
                colour=discord.Colour.red()
            ))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def timer(self, ctx, time_to_wait: str = None):
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
            if not time_to_wait:
                self.times[ctx.author.id] = {
                    'time': time.time()
                }
                await ctx.send(embed=discord.Embed(
                    description='⌚ | The timer has been set...',
                    colour=discord.Colour.red()
                ))
            else:
                try:
                    time_to_wait = int(time_to_wait)
                except ValueError:
                    ctx.command.reset_cooldown(ctx)
                    return await ctx.send(embed=discord.Embed(
                        description='<a:nope:787764352387776523> Time to set must a number (counted with minutes)',
                        colour=discord.Color.red()
                    ))
                await ctx.send(embed=discord.Embed(
                    description='⌚ | Will remind you in **{}** minutes.'.format(time_to_wait),
                    colour=discord.Colour.green()
                ))
                await asyncio.sleep(time_to_wait * 60)
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
        response = await self.session.post(
            'https://api.mechakaren.xyz/v1/chatbot',
            headers={'Authorization': self.bot.env('API_TOKEN')},
            json={'message': message}
        )
        try:
            json = await response.json()
        except Exception:
            return await ctx.message.reply(content='API is currently down - Comeback soon!')
        return await ctx.message.reply(content=json['response']['answer'] or 'Hello There.')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def urban(self, ctx, *, term: str) -> discord.Embed:
        base_url = 'https://api.urbandictionary.com/v0/define?page=1&term={}'.format(term)
        url = await self.bot.loop.run_in_executor(None, requote_uri, base_url)

        req = await self.session.get(url)
        try:
            stack = await req.json()
        except Exception:
            return await ctx.send('Urban API is currently down.')

        if not stack['list']:
            return await ctx.send('It appears that I cannot find this word.')

        current_definition = stack['list'][0]
        embed = discord.Embed(title=current_definition['word'].title(), colour=discord.Colour.purple(),
                              url=current_definition['permalink'],
                              description='Contributor: **{}**'.format(current_definition['author']))
        embed.add_field(name='Meaning:', value=current_definition['definition'])
        embed.add_field(name='Example:', value=current_definition['example'], inline=False)
        embed.add_field(name='Likes:', value=':thumbsup: {}'.format(current_definition['thumbs_up']))
        embed.add_field(name='Dislikes:', value=':thumbsdown: {}'.format(current_definition['thumbs_down']))
        embed.add_field(name='Posted At:', value='{} ({})'.format(
            datetime.datetime.fromisoformat(current_definition['written_on'][:-1]).strftime('%A, %B %Y'),
            current_definition['written_on'].split('T')[0]), inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(create_instant_invite=True)
    async def vanish(self, ctx):
        global vanish_

        async def message():
            try:
                invites = await ctx.guild.invites()
                message_ = await ctx.author._user.send('You have vanished.\nRejoin: {}'.format(random.choice(invites)))
                return message_
            except Exception:
                return

        check = await ctx.send('Are your sure that you want to vanish?')

        try:
            await check.add_reaction('✅')
            await check.add_reaction('❌')
            vanish_ = False

            def _check(m):
                global vanish_

                if m.member.id == ctx.author.id and str(m.emoji) == '✅':
                    vanish_ = True
                    return True

                elif m.member.id == ctx.author.id and str(m.emoji) == '❌':
                    return True
                return False

            await self.bot.wait_for('raw_reaction_add', check=_check)
            if not vanish_:
                await check.clear_reactions()
                return await check.edit(content='Looks like **{}** doesnt want to vanish!'.format(ctx.author))

            await ctx.guild.kick(ctx.author, reason='They have VANISHED.')

            try:
                await check.edit(content='**{}** Has Vanished.'.format(ctx.author))
                await check.clear_reactions()
                await check.add_reaction(emoji.KAREN_ADDITIONS_ANIMATED['wave'])
            except Exception:
                return await ctx.send(content='**{}** Has Vanished.'.format(ctx.author))

            try:
                await message()
            except discord.errors.Forbidden:
                pass

        except discord.errors.Forbidden:
            try:
                await check.edit(content="Uh oh, Looks like I cannot make you disappear".format(ctx.author.mention))
                await check.clear_reactions()
                return await check.add_reaction('<:F_:745287381816574125>')
            except Exception:
                return await ctx.send(content="Uh oh, Looks like I cannot make you disappear".format(ctx.author.mention))

def setup(bot):
    bot.add_cog(fun(bot))
