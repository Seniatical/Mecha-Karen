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
import requests
from pprint import pprint

from Others import IMG, Bio, Channel, Co, gender, Jokes, Numbers, Numbers2, Quotes, Stuff, words

class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def simp(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title=f'How much of a simp are they?',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Simp**', value=f'{user.display_name} is {random.choice(IMG.Numbers)}% a simp')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def retard(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Retard**', value=f'{user.display_name} is {random.choice(IMG.Numbers)}% retarded')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def Human(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Human**', value=f'{user.display_name} is {random.choice(IMG.Numbers)}% human')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def buff(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Buff Test**', value=f'{user.display_name} is {random.choice(IMG.Numbers)}/100 Buff :muscle:')
        await ctx.send(embed=embed)


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def Waifu(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Waifu**', value=f'{user.display_name} is {random.choice(IMG.Number1)}')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def Dad(self, ctx, message):
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_orange()
        )
        embed.add_field(name='Daddo Machine 9000', value=f'Hello {message}. Im Dad')
        await ctx.send(embed=embed)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def gay(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        embed = discord.Embed(
            title='',
            color=discord.Color.dark_green()
        )
        embed.add_field(name='**Gay**', value=f'{user.display_name} is {random.randint(1, 101)}% gay :rainbow_flag:')
        await ctx.send(embed=embed)

    @commands.command(aliases=['jokes'])
    @cooldown(1, 10, BucketType.user)
    async def joke(self, ctx):
        embed = discord.Embed(
            title='',
            color=discord.Color.gold()
        )
        embed.add_field(name='**Joke**', value=f'{random.choice(Jokes.joke)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['fact'])
    @cooldown(1, 10, BucketType.user)
    async def facts(self, ctx):
        embed = discord.Embed(
            title='**Fun Facts:**',
            color=discord.Color.teal()
        )
        embed.add_field(name='‏‏‎ ', value=f'{random.choice(Co.fact)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['gender'])
    @cooldown(1, 10, BucketType.user)
    async def genderfinder(self, ctx, user : discord.Member):
        if user == None:
            user = ctx.author
        else:
            pass
        genders = random.choice(gender.gend)
        embed = discord.Embed(
            title=f"**{user.display_name}'s Gender!**",
            color=discord.Color.magenta()
        )
        embed.add_field(name='‏‏‎ ', value=f'{genders}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['mk', 'MagicK', 'MKaren'])
    @cooldown(1, 10, BucketType.user)
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
    @cooldown(1, 10, BucketType.user)
    async def IQ(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        iq = ['130 and above (Very Superior)',
              '120–129 (Superior)',
              '110–119 (High Average)',
              '90–109 (Average)',
              '80–89 (Low Average)',
              '70–79 (Borderline)',
              '69 and below	(Extremely Low)']
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**IQ Machine 9000**', value=(f'{user.display_name} IQ is {random.choice(iq)} '))
        await ctx.send(embed=e)


    @commands.command(aliases=['Penis'])
    @cooldown(1, 10, BucketType.user)
    async def PP(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
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
                    value=f'{user.display_name} penis is:\n{random.choice(pen)}\n**Even my angel has a bigger one**', )
        await ctx.send(embed=e)


    @commands.command(aliases=['insult'])
    @cooldown(1, 10, BucketType.user)
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
    @cooldown(1, 10, BucketType.user)
    async def GF(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
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
                    value=(f'The chances of {user.display_name} getting a GF:\n\n**The Wild Karen Says:**\n\n{random.choice(girl)}'))
        await ctx.send(embed=e)


    @commands.command(aliases=['comp'])
    @cooldown(1, 10, BucketType.user)
    async def Compliment(self, ctx, *, answer=None):
        if answer == None:
            await ctx.send('What are you asking me?')
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
    @cooldown(1, 10, BucketType.user)
    async def kill(self, ctx, *, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
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
                'there balls got crushed. They died from the pain.',
                ]
        e = discord.Embed(title="", description="", color=0x50C878)
        e.add_field(name=f'**How did they die**', value=(f'{user.display_name} was killed by {random.choice(died)}'))
        await ctx.send(embed=e)


    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def kiss(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
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
                        value=f'{user} stares deeply into {random.choice(U2)} eyes and they arkwardly kiss eachother.')
        await ctx.send(embed=embed)


    @commands.command(aliases=['mates'])
    @cooldown(1, 10, BucketType.user)
    async def Friend(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
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
        embed.add_field(name='**Friends Finder 653**', value=f'{user.display_name} friends\n{random.choice(friend)}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['punch'])
    @cooldown(1, 10, BucketType.user)
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
    @cooldown(1, 10, BucketType.user)
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
    @cooldown(1, 10, BucketType.user)
    async def fly(self, ctx):
        flying = ['You became a bird and flew around the world.',
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
    @cooldown(1, 10, BucketType.user)
    async def parent(self, ctx):
        parents = ['Left you when they were young',
                   'There still with you.',
                   'Dad went to  get the milk. idk were hes gone',
                   'Mommys boy. HAHAHA',
                   'Idk mate. You were adopted',
                   ]
        await ctx.send(f'{random.choice(parents)}')

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def Wobbler(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        number = random.randint(1, 101)
        embed = discord.Embed(
            title='**Do {} walk straight??**'.format(user),
            color=discord.Color.purple()
        )
        embed.add_field(name='‏‏‎ ‎', value=f'{number}% a Wobbler.')
        if number > 50:
            embed.add_field(name='‏‏‎ ‎', value='\n\nLearn to walk. LMFAO')
        else:
            embed.add_field(name='‏‏‎ ‎', value='\n\n{} parents did a good job. I think. ;-;'.format(user))
        await ctx.send(embed=embed)


    @commands.command(aliases=['diprate', 'dip', 'stab'])
    @cooldown(1, 10, BucketType.user)
    async def stabrate(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        chance = random.randint(1, 101)
        embed = discord.Embed(
            title='**Chances of {} getting stabbed:**'.format(user),
            color=discord.Color.blue()
        )
        embed.add_field(name='‏‏‎ ', value='The chance of {} getting stabbed is {}%.'.format(user, chance))
        if chance < 50:
            embed.add_field(name='‏‏‎ ', value='\nLooks like {} gonna live another day..'.format(user))
        else:
            embed.add_field(name='‏‏‎ ', value='\nBetter be carrying that mechete!')
        await ctx.send(embed=embed)


    @commands.command(aliases=['begr', 'Brate'])
    @cooldown(1, 10, BucketType.user)
    async def begrate(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        begrate = random.randint(1, 101)
        embed = discord.Embed(
            title='**How much of a beg are {}!!!!**'.format(user),
            color=discord.Color.blue()
        )
        embed.add_field(name='‏‏‎ ', value=f'{user} are **{begrate}%** a beg')
        if begrate < 50:
            embed.add_field(name='‏‏‎ ', value='{} is not a beg'.format(user))
        else:
            embed.add_field(name='‏‏‎ ', value='{} is some dirty beg fam. Piss off!'.format(user))
        await ctx.send(embed=embed)

    @commands.command(aliases=['slots', 'bet'])
    @cooldown(1, 10, BucketType.user)
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
    @cooldown(1, 10, BucketType.user)
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
        embed.set_author(name="🏓    PONG    🏓", icon_url="https://img.icons8.com/ultraviolet/40/000000/table-tennis.png")
        embed.add_field(name="Bot Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="Normal Speed", value=f"{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms")
        embed.set_footer(text=f"Total estimated elapsed time: {round(sum(times))}ms")
        await msg.edit(content=f":ping_pong: **{round((round(sum(times)) + round(self.bot.latency * 1000))/4)}ms**", embed=embed)

    @commands.command()
    @commands.cooldown(1, 60, BucketType.guild)
    async def useless(self, ctx):
        user = ctx.author
        await ctx.send('Hello ' + user.name)
        msg = await ctx.send('Type `press` to press the useless button.')
        def check(m):
            if m.author.id == user.id and m.content.lower() == 'press':
                return True
            return False
        await self.bot.wait_for('message', timeout=10.00, check=check)
        await ctx.send('http://66.media.tumblr.com/d1483298e112b3bf08d35a2bd345a097/tumblr_n5ig6cjyk81t2csv8o2_500.gif')
        await ctx.send('Button has been pressed by {}'.format(user.name))

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def odds(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        odd = ['homeless', 'a chippie', 'lost', 'rich', 'disabled', 'unwanted', 'loved', 'wanted']
        counter = random.randint(1, 101)
        emoji = ['😭','😰','<:trashcan:744626891948032124>','😥','😬','🤐','<:you_wot:748867944649588776>','<:birdonem:744615651645063219>','👍']
        embed = discord.Embed(
            title=f'The odds of {user} becoming {random.choice(odd)}',
            color=discord.Color.purple(),
            description=f'**{counter}%** {random.choice(emoji)}'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['le'])
    @commands.cooldown(1, 10, BucketType.user)
    async def lifeexpectancy(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        counter = random.randint(1, 150)
        embed = discord.Embed(
            title="{}'s life expectancy is:".format(user),
            color=discord.Color.red(),
            description=f'**{counter} yrs old!**'
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def BWeight(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        weight = ['Pinweight\t(44 - 46 Kg)', 'Light Flyweight\t(Below 48Kg)', 'Flyweight\t(49 - 52 Kg)', 'Bantamweight\t(52 - 53.5 Kg)', 'Featherweight\t(54 - 57 Kg)', 'Lightweight\t(59 - 61 Kg)', 'Lighter welterweight\t(54 - 67 Kg)', 'Welterweight\t(64 - 69 Kg)', 'Middleweight\t(70 - 73 Kg)', 'Light heavyweight\t(76 - 80 Kg)', 'Heavyweight\t(Above 81 Kg)', 'Super Heavyweight\t(Above 91 Kg)']
        choice = random.choice(weight)
        embed = discord.Embed(
            title='What is {} boxing weight?'.format(user),
            color=discord.Color.red(),
            description=f'{choice}'
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['Weight', 'WI'])
    @commands.cooldown(1, 10, BucketType.user)
    async def WeighIn(self, ctx, user : discord.Member=None):
        if user == None:
            user = ctx.author
        else:
            pass
        weight = random.randint(1, 200)
        if weight > 150:
            msg = 'Loose some weight bruv!'
        embed = discord.Embed(
            title='How much do you weigh?',
            color=discord.Color.red(),
            description=f'**`{weight}` Kg**'
        )
        await ctx.send(embed=embed)
        await ctx.send(msg)

    @commands.command()
    async def beer(self, ctx, user: discord.Member = None, *, reason: commands.clean_content = ""):
        if not user or user.id == ctx.author.id:
            return await ctx.send(f"**{ctx.author.mention}**: fieeeeestaaa!🎉🍺")
        if user.bot == True:
            return await ctx.send(f"I would love to give a beer to {user.mention}. But i am unsure they will respond to you!")

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
            await ctx.send(f"well it seems **{user.name}** didnt want a beer with **{ctx.author.name}** ;-;")
        except discord.Forbidden:
            beer_offer = f"**{user.name}**, you have a 🍺 from **{ctx.author.name}**"
            beer_offer = beer_offer + f"\n\n**reason:** {reason}" if reason else beer_offer
            await msg.edit(content=beer_offer)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.user)
    async def reverse(self, ctx, *args):
        args = ' '.join(map(str, args))
        x = list(args)
        if '@' in x:
            await ctx.send('Cant reverse the sentence as `@` is present!')
        else:
            x = reversed(x)
            x = ''.join(map(str, x))
            await ctx.channel.purge(limit=1)
            await ctx.send(x)

    @commands.command(aliases=['W'])
    @cooldown(1, 300, BucketType.user)
    async def weather(self, ctx, location : str=None):
        if location == None:
            await ctx.send('You havent provided a location!')
        else:
            try:
                x = location
                x = x.lower()
                r = requests.get('User your API'.format(x))
                x = r.json()
                country = x['sys']['country']
                city = x['name']
                cord1 = x['coord']['lon']
                cord2 = x['coord']['lat']
                main = x['weather'][0]['main']
                desc = x['weather'][0]['description']
                speed = x['wind']['speed']
                humid = x['main']['humidity']
                icon = x['weather'][0]['icon']
                pressure = x['main']['pressure']
                clouds = x['clouds']['all']
                temp = x['main']['temp']
                temp_f = x['main']['feels_like']
                zone = x['timezone']
                embed=discord.Embed(
                    title=f'{city} ({country})',
                    colour=discord.Color.blue(),
                    description=f'Longitude : {cord1} | Latitude : {cord2}'
                )
                if icon == '01d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '02d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '03d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '04d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '09d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '10d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '11d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '13d':
                    embed.set_thumbnail(url='LALA')
                elif icon == '50d':
                    embed.set_thumbnail(url='LALA')
                if icon == '01n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '02n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '03n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '04n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '09n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '10n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '11n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '13n':
                    embed.set_thumbnail(url='LALA')
                elif icon == '50d':
                    embed.set_thumbnail(url='LALA')
                embed.add_field(name='Wind', value=f'{speed} MPH')
                embed.add_field(name='Humidity', value=f'{humid}%')
                embed.add_field(name='Weather', value=f'{main} ({desc})')
                embed.add_field(name='Pressure', value=f'{pressure}')
                embed.add_field(name='Clouds', value=f'{clouds}')
                embed.add_field(name='Temperature', value=f'{round(temp - 273.15)} °C')
                embed.add_field(name='Feels Like', value=f'{round(temp_f - 273.15)} °C')
                embed.add_field(name=f'Time Zone', value=f'{zone}')
                embed.add_field(name=f'Min Temp', value=str(round(x['main']['temp_min'] - 273.15)) + ' °C')
                embed.add_field(name=f'Max Temp', value=str(round(x['main']['temp_max'] - 273.15)) + ' °C')
                await ctx.send(embed=embed)
            except KeyError:
                await ctx.send('Location was invalid.')

def setup(bot):
    bot.add_cog(Fun(bot))
