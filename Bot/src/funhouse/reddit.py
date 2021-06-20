import random
import datetime
import time

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import os
import apraw
import asyncio
from utility import emojis as emoji
from utility import abbrev_denary as convert_size
import math
import aiohttp
from requests.utils import requote_uri

class Reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.all_subs = []
        self.reddit = apraw.Reddit(
            username='Seniatical',
            password='ilikemrbean',
            client_id='cwmSyyiijyG0Wg',
            client_secret='RbujK11eDKYIiLeAf3zzGyQGcFg',
            user_agent='Mecha Karen Memes Refresh'
        )
    @commands.Cog.listener()
    async def on_ready(self):
        async def speed():
            while True:
                sub = await self.reddit.subreddit('memes')
                async for _submission in sub.top(limit=500):
                    if not _submission:
                        continue

                    name = _submission.title
                    url = _submission.url
                    comments = _submission.num_comments
                    up = _submission.score
                    sub = await _submission.subreddit()
                    name_ = await _submission.author()

                    embed = discord.Embed(
                        title=name,
                        color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)),
                        url = await self.bot.loop.run_in_executor(None, requote_uri, f'https://www.reddit.com/r/dankmemes/comments/{_submission.id}/{_submission.title}/')
                    )
                    try:
                        embed.set_author(name='Posted by {} from r/{}'.format(name_, sub), icon_url=name_.icon_img, url=f'https://www.reddit.com/user/{name_}/')
                    except Exception:
                        embed.set_author(name='Posted by {} from r/{}'.format(name_, sub), url=f'https://www.reddit.com/user/{name_}/')
                    embed.set_image(url=url)
                    embed.set_footer(text='{} {}   |   {} {}'.format(emoji.UNICODE['up'], convert_size(up), emoji.UNICODE['text'], convert_size(comments)))
                    self.all_subs.append(embed)
                await asyncio.sleep(3600)
        self.bot.loop.create_task(speed())

    @commands.command(name='Meme', aliases=['memes'])
    @commands.cooldown(1, 5, BucketType.user)
    async def memes(self, ctx):
        embed = random.choice(self.all_subs)
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
