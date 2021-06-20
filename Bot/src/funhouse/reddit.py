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

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import apraw
import asyncio
from utility import emojis as emoji
from utility import abbrev_denary as convert_size
import aiohttp
from requests.utils import requote_uri
from core._.tasks.reddit import memes

class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit = apraw.Reddit(
            username=bot.env('REDDIT_USERNAME'),
            password=bot.env('REDDIT_PASSWORD'),
            client_id=bot.env('REDDIT_CLIENT_ID'),
            client_secret=bot.env('REDDIT_CLIENT_SECRET'),
            user_agent='<Mecha Karen - Discord Bot [https://github.com/Seniatical/Mecha-Karen/main/Bot/src/funhouse/reddit.py]>'
        )

        bot.cache.cache['memes'] = []

        print('Storing memes from `r/memes` in cache container - `self.cache.cache["memes"]`')
        
        memes.add_global(bot.cache.cache['memes'])
        self.bot.loop.create_task(memes.task(bot, self.reddit))
        
    @commands.command(name='Meme', aliases=['memes'])
    @commands.cooldown(1, 5, BucketType.user)
    async def memes(self, ctx):
        embed = random.choice(self.bot.cache.cache['memes'])
        await ctx.send(embed=embed)

    @commands.command(name='BB', aliases=['BreakingBad'])
    @commands.cooldown(1, 5, BucketType.user)
    async def bb(self, ctx):
        subreddit = await self.reddit.subreddit('okbuddychicanery')
        allsubs = []
        async for i in subreddit.top(limit=50):
            if i.is_video:
                continue
            allsubs.append(i)
        random_sub = random.choice(allsubs)
        
        name = random_sub.title
        url = random_sub.url
        comments = random_sub.num_comments
        up = random_sub.score
        author = await random_sub.author()
        sub = await random_sub.subreddit()

        embed = discord.Embed(
            title=name,
            color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        )
        embed.set_author(name=f'Posted by {author} from r/{sub}')
        embed.set_image(url=url)
        embed.set_footer(text='{} {}   |   {} {}'.format(emoji.UNICODE['up'], convert_size(up), emoji.UNICODE['text'], convert_size(comments)))
        await ctx.send(embed=embed)
        
    @commands.command(name='Reddit')
    @commands.cooldown(1, 30, BucketType.user)
    async def reddit(self, ctx, subreddit: str):
        global msg
        
        try:
            try:
                subreddit = await self.reddit.subreddit(subreddit)
            except Exception:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send('Subreddit doesnt exist!')
            
            all_subs_ = []
            async for submission in subreddit.hot(limit=10):
                all_subs_.append(submission)
            random_sub = random.choice(all_subs_)
            
            if random_sub.over18:
                msg = await ctx.send('Over 18 content detected.')
                if ctx.channel.is_nsfw():
                    name = random_sub.title
                    url = random_sub.url
                    comments = random_sub.num_comments
                    up = random_sub.score
                    author = await random_sub.author()
                    sub = await random_sub.subreddit()
                    embed = discord.Embed(
                        title=name,
                        color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                    )
                    embed.set_author(name=f'Posted by {author} from r/{sub}')
                    embed.set_image(url=url)
                    embed.set_footer(text='{} {}   |   {} {}'.format(emoji.UNICODE['up'], convert_size(up), emoji.UNICODE['text'], convert_size(comments)))
                    await msg.edit(content=None, embed=embed)
                else:
                    embed = discord.Embed(title='Error 404!', colour=discord.Color.red(),
                                          description="You must use this command in a channel marked as **NSFW**.",
                                          timestamp=ctx.message.created_at
                                          ).set_footer(text='Invoked by {}'.format(ctx.author), icon_url=ctx.author.avatar)
                    embed.set_image(url='https://i.imgur.com/cy9t3XN.gif')
                    await msg.edit(content=None, embed=embed)
                    ctx.command.reset_cooldown(ctx)
            else:

                name = random_sub.title
                url = random_sub.url
                comments = random_sub.num_comments
                up = random_sub.score
                author = await random_sub.author()
                sub = await random_sub.subreddit()

                embed = discord.Embed(
                    title=name,
                    color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                )
                embed.set_author(name=f'Posted by {author} from r/{sub}')
                embed.set_image(url=url)
                embed.set_footer(text='{} {}   |   {} {}'.format(emoji.UNICODE['up'], convert_size(up), emoji.UNICODE['text'], convert_size(comments)))
                await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('Message Content was too large!')

def setup(bot):
    bot.add_cog(Reddit(bot))
