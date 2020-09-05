import PIL
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import json
import random
import datetime
import time

import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, MissingRequiredArgument
import os

import Bio
import Co
import IMG
import Jokes
import Memes
import Numbers
import Quotes
import Status
import Token
import art
import gender

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Fun Cog is ready')

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def simp(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Simp**', value=f'You are {random.choice(IMG.Numbers)}% simp')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def retard(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Retard**', value=f'You are {random.choice(IMG.Numbers)}% retarded')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def Human(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Human**', value=f'You are {random.choice(IMG.Numbers)}% a real human')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def buff(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Buff Test**', value=f'You are {random.choice(IMG.Numbers)}/100 Buff :muscle:')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def Waifu(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Waifu**', value=f'Waifu rating {random.choice(IMG.Number1)}')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def Dad(self, ctx, message):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_orange()
        )
        embed.add_field(name='Daddo Machine 9000', value=f'Hello {message}. Im Dad')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def gay(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Gay**', value=f'You are {random.choice(IMG.Numbers)}% gay :rainbow_flag:')
        await ctx.send(embed=embed)

    @commands.command(aliases=['jokes'])
    @cooldown(1, 2, BucketType.user)
    async def joke(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.gold()
        )
        embed.add_field(name='**Joke**', value=f'{random.choice(Jokes.joke)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['ud'])
    @cooldown(1, 2, BucketType.user)
    async def Urban_dictionary(self, ctx):
        embed = discord.Embed(
            title='Urban Dictionary (UK Slang)',
            colour=discord.Color.purple()
        )
        embed.add_field(name='**Chosen Word:**', value=f'{random.choice(IMG.response)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['fact'])
    @cooldown(1, 2, BucketType.user)
    async def facts(self, ctx):
        embed = discord.Embed(
            title='**Fun Facts:**',
            color=discord.Color.teal()
        )
        embed.add_field(name='‏‏‎ ', value=f'{random.choice(Co.fact)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['gender'])
    @cooldown(1, 2, BucketType.user)
    async def genderfinder(self, ctx):
        genders = random.choice(gender.gend)
        embed = discord.Embed(
            title='**What gender are you!**',
            color=discord.Color.magenta()
        )
        embed.add_field(name='‏‏‎ ', value=f'{genders}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['mk', 'MagicK', 'MKaren'])
    @cooldown(1, 2, BucketType.user)
    async def MagicKaren(self, ctx, *, question):
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
        e = discord.Embed(title="", description="__**MagicKaren:**__", color=0x50C878)
        e.add_field(name='**Results**', value=(f'Question:\t{question}\n\nAnswer:\t{random.choice(responses)}'))
        await ctx.send(embed=e)

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def IQ(self, ctx):
        iq = ['130 and above (Very Superior)',
              '120–129 (Superior)',
              '110–119 (High Average)',
              '90–109 (Average)',
              '80–89 (Low Average)',
              '70–79 (Borderline)',
              '69 and below	(Extremely Low)']
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**IQ Machine 9000**', value=(f'Your IQ is {random.choice(iq)} '))
        await ctx.send(embed=e)


    @commands.command(aliases=['Penis'])
    @cooldown(1, 2, BucketType.user)
    async def PP(self, ctx):
        pen = ['8D',
               '8=D',
               '8==D',
               '8===D',
               '8====D',
               '8=====D',
               '8======D',
               '8=======D',
               '8========D',
               '8=========D',
               '8==========D',
               '8===========D',
               '8============D',
               '8=============D',
               '8==============D',
               '8===============D']
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**PP machine 4356**',
                    value=f'Your penis is:\n{random.choice(pen)}\n**Even my angel has a bigger one**', )
        await ctx.send(embed=e)


    @commands.command(aliases=['insult'])
    @cooldown(1, 2, BucketType.user)
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

        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Roast**', value=(f'{random.choice(A)}'))
        await ctx.send(embed=e)

    @commands.command(aliases=['Girlfriend'])
    @cooldown(1, 2, BucketType.user)
    async def GF(self, ctx):
        girl = ['No chance.',
                'Very hard.',
                'Barely.',
                'Would be lucky.',
                'pretty rare.',
                'Good chance.',
                '100 out a 100. Maybe you would like me?',
                'Ummm dont ask that again.',
                'Good joke. But were you being seriou tho?',
                'Dont want to answer that...',
                'CANT YOU SEE MY ANGEL IS CALLING ME. GO AWAY!!!']
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Karens Stalker**',
                    value=(f'The chances of you getting a GF:\n\n**The Wild Karen Says:**\n\n{random.choice(girl)}'))
        await ctx.send(embed=e)


    @commands.command(aliases=['comp'])
    @cooldown(1, 2, BucketType.user)
    async def Compliment(self, ctx, *, answer):
        comp = ['Gross. Now piss off!',
                'My angel is still better!',
                "I don't really care. Just keep my angel happy!",
                'Please shut up!!!',
                'Umm im a Queen. Your a peasent. Now clean my feet!',
                'I couldnt be bothered listening. Now shoo!!!']
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Complimento Machino**',
                    value=(f'**You ask Karen:**\n\n{answer}\n\n**Karen Says**\n\n{random.choice(comp)}'))
        await ctx.send(embed=e)

    @commands.command(aliases=['murder'])
    @cooldown(1, 2, BucketType.user)
    async def kill(self, ctx, *, question):
        died = ['rolling out of the bed and the demon under the bed ate them',
                'getting impaled on the bill of a swordfish',
                'falling off a ladder and landing head first in a water butt',
                'his own explosive while trying to steal from a condom dispenser',
                'a coconut falling off a tree and smashing there skull in',
                'taking a selfie with a loaded handgun shot himself in the throat',
                'shooting himself to death with gun carried in his breast pocket',
                'getting crushed while moving a fridge freezer',
                'getting crushed by his own coffins',
                'getting crushed by your partner',
                'laughing so hard at The Goodies Ecky Thump episode that he died of heart failure',
                'getting run over by his own vehicle',
                'car engine bonnet shutting on there head',
                'heading a medicine ball',
                'becoming a gacha fan for life. Angry redditors brutally murdered them.',
                'doing something wrong in front of their mother while she had a slipper.',
                'dressing up as a cookie and cookie monster ate them.',
                'getting a boner while standing on a train platform. The train zoomed by and cut it clean. They died from blood loss.',
                'being so obese that the broke the elevator in the Burj Khalifa and died from the impact of the falling elevator.',
                'paying a prostitute and ended up in the friendzone.',
                ]
        e = discord.Embed(title="", description="", color=0x50C878)
        e.add_field(name=f'**How did they die**', value=(f'{question} was killed by {random.choice(died)}'))
        await ctx.send(embed=e)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def kiss(self, ctx, *, U1, ):
        U2 = ['your moms',
              'a slugs',
              'a fit girls',
              'the 80 yr old janitors',
              'the floors',
              'the airs',
              "there ex's photo",
              'the screens',
              ]

        embed = discord.Embed(
            title='',
            color=discord.Color.teal()
        )
        embed.add_field(name='**Kiss**',
                        value=f'{U1} stares deeply into {random.choice(U2)} eyes and they arkwardly kiss eachother.')
        await ctx.send(embed=embed)


    @commands.command(aliases=['mates'])
    @cooldown(1, 2, BucketType.user)
    async def Friend(self, ctx):
        friend = ['None to be found.',
                  'Mark\nBob\nMom.',
                  'All the girls in the school.',
                  'Karen and her soccer kid.',
                  'Mom and dad.',
                  'Too many to be said',
                  'Girl\nA man\nIdk the other guy',
                  'Yourself',
                  'You\nYourself\nand **BLEEP**',
                  ]
        embed = discord.Embed(
            title='',
            color=discord.Color.light_grey()
        )
        embed.add_field(name='**Friends Finder 653**', value=f'{random.choice(friend)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['punch'])
    @cooldown(1, 2, BucketType.user)
    async def PunchMachine(self, ctx):
        answer = random.randint(0, 999)

        responce = ['**Nice shot bro**',
                    '**Did you miss the machine**',
                    '**DAHM HAVE SOME MERCY**',
                    '**Even a baby can hit harder**',
                    '**Weakling lmfao**',
                    '**You wasted money to get that score**',
                    ]
        embed = discord.Embed(
            title='',
            color=discord.Color.default()
        )
        embed.add_field(name='**Punch MACHINE**',
                        value=f'\n\n*You swing and hit*\n\n**{answer}**\n\n*The crowd around you:*\n\n{random.choice(responce)}')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def fight(self, ctx):
        power = ['You got smacked so hard your jar broke',
                 'You missed the guy and ended up getting mowed down by his boys. LOL',
                 'Sent the man through the wall. calm down!!!',
                 'Ended up fighting and causing a mass brawl. You are now in jail...',
                 'Smacked the guy so hard he is still in hospital till this day!!!',
                 'You knocked out the opponent in one shot.',
                 'The guy ended up pulling out a knife and you get stabbed.',
                 'Phoned the guy to fight and he was there with his boys...',
                 'You slide tackled him and he fell and broke his neck!!!',
                 'You attended the fight with a baseball bat and knocked some sense into him.',
                 'Catched a deadly disease and ended up dieing.',
                 'A close fight but you ended up victorious!!! GG!',
                 'A close fight but you ended up loosing!!! GG!'
                 ]
        embed = discord.Embed(
            title='**Get Boxxed up skid**',
            color=discord.Color.light_grey()
        )
        embed.add_field(name='**Streets**', value=f'{random.choice(power)}')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def fly(self, ctx):
        flying = ['You bacame a bird and flew around the world.',
                  'Jumped off your roof and ended up in a bush of thorns. What a retard',
                  'Flew straight into a building. Doesnt that remind us of something.',
                  'Went to a mental asylum because the theropist thought you was mentally disabled',
                  'Failed landing and you skidded right into a tree and snapped your beak in half',
                  ]
        embed = discord.Embed(
            title='Fly machine 10000',
            color=discord.Color.blue()
        )
        embed.add_field(name='**The sky**', value=f'{random.choice(flying)}')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def parent(self, ctx):
        parents = ['Left you when they were young',
                   'There still with you.',
                   'Dad went to  get the milk. idk were hes gone',
                   'Mommys boy. HAHAHA',
                   'Idk mate. You were adopted',
                   ]
        await ctx.send(f'{random.choice(parents)}')


    @commands.command(aliases=['WTW', 'weather', 'W'])
    @cooldown(1, 2, BucketType.user)
    async def WhatsTheWeather(self, ctx):
        weather = [
            'Get your fat ass up and look outside your window.',
            'Its cloudly',
            'Bloody boiling. get me a ice cream. Pleb..',
            'Raining cats and dogs',
            'Spitting outside!',
            'Its raining. did you take my clothes off the line',
            'Do i look like BBC Weather',
            'Umm ask later. Piece of shit.',
            'Sunny.',
            'Theres a tornado outside. Are you deaf!',
        ]
        await ctx.send(f'{random.choice(weather)}')


    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def pussy(self, ctx):
        number = random.randint(1, 101)
        embed = discord.Embed(
            title='**How much of a pussy are you!!!**',
            color=discord.Color.purple()
        )
        embed.add_field(name='‏‏‎ ‎', value=f'{number}% pussy.')
        if number < 50:
            embed.add_field(name='‏‏‎ ‎', value='\n\nYour a man. Back your bedrins on the road!!!')
        else:
            embed.add_field(name='‏‏‎ ‎', value='\n\nYour some weak ass bruv. get outta here!!')
        await ctx.send(embed=embed)


    @commands.command(aliases=['diprate', 'dip', 'stab'])
    @cooldown(1, 2, BucketType.user)
    async def stabrate(self, ctx):
        chance = random.randint(1, 101)
        embed = discord.Embed(
            title='**Chances of you getting stabbed:**',
            color=discord.Color.blue()
        )
        embed.add_field(name='‏‏‎ ', value=f'The chance of you getting stabbed is {chance}%.')
        if chance < 50:
            embed.add_field(name='‏‏‎ ', value='\nLooks like you gonna live another day..')
        else:
            embed.add_field(name='‏‏‎ ', value='\nBetter be carrying that mechete!')
        await ctx.send(embed=embed)


    @commands.command(aliases=['begr', 'Brate'])
    @cooldown(1, 2, BucketType.user)
    async def begrate(self, ctx):
        begrate = random.randint(1, 101)
        embed = discord.Embed(
            title='**How much of a beg are you!!!!**',
            color=discord.Color.blue()
        )
        embed.add_field(name='‏‏‎ ', value=f'You are **{begrate}%** a beg')
        if begrate < 50:
            embed.add_field(name='‏‏‎ ', value='You calm fam. have a slice!')
        else:
            embed.add_field(name='‏‏‎ ', value='Your some dirty beg fam. Piss off!')
        await ctx.send(embed=embed)

    @commands.command(aliases=['slots', 'bet'])
    async def slot(self, ctx):
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a = random.choice(emojis)
        b = random.choice(emojis)
        c = random.choice(emojis)

        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} Has gotten 3 out of 3, ¡HE WINS!!! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 out of 3, ¡HE WINS!!! 🎉")
        else:
            await ctx.send(f"{slotmachine} 0 out of 3, He looses 😢")

    @commands.command(aliases=['Latency'])
    async def ping(self, ctx):
        msg = await ctx.send("`Bot Latency...`")
        times = []
        counter = 0
        embed = discord.Embed(title="More Information:", description="4 pings have been made and here are the results:", colour=discord.Color.red())
        for _ in range(3):
            counter += 1
            start = time.perf_counter()
            await msg.edit(content=f"Trying Ping... {counter}/3")
            end = time.perf_counter()
            speed = round((end - start) * 1000)
            times.append(speed)
            if speed < 160:
                embed.add_field(name=f"Ping {counter}:", value=f"🟢 | {speed}ms", inline=True)
            elif speed > 170:
                embed.add_field(name=f"Ping {counter}:", value=f"🟡 | {speed}ms", inline=True)
            else:
                embed.add_field(name=f"Ping {counter}:", value=f"🔴 | {speed}ms", inline=True)
        embed.set_author(name="🏓    **PONG**    🏓", icon_url="https://img.icons8.com/ultraviolet/40/000000/table-tennis.png")
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Normal Speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_footer(text=f"Total estimated elapsed time: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

def setup(bot):
    bot.add_cog(Fun(bot))
