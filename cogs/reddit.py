import random
import datetime
import time

import discord
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown
import os
import praw
import asyncio


class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.all_subs = []
        self.reddit = praw.Reddit(
            username='YOUR REDDIT ACCOUNT USERNAME',
            password='YOUR REDDIT ACCOUNT PASSWORD',
            client_id='YOUR REDDIT APP CLIENT_ID (THE SHORT ONE)',
            client_secret='YOUR REDDIT APP SECRET (THE LONG ONE)',
            user_agent='Anything goes here bois'
        )
        '''
        TO GET A REDDIT APPLICATION, VISIT:
            https://www.reddit.com/prefs/apps
        '''

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.loop.create_task(speed())

    @commands.command(aliases=['meme'])
    @commands.cooldown(1, 10, BucketType.user)
    async def memes(self, ctx):

        random_sub = random.choice(self.all_subs)

        name = random_sub.title
        url = random_sub.url
        comments = random_sub.comments
        upvote = random_sub.upvote_ratio
        up = random_sub.score
        author = random_sub.author
        sub = random_sub.subreddit

        embed = discord.Embed(
            title= name,
            color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        )
        embed.description='Submission [URL]({}).'.format(random_sub.url)
        embed.set_author(name=f'Posted by {author} from r/{sub}')
        embed.set_image(url=url)
        embed.set_footer(text=f'\t💬 {len(comments)}    ⇅ {upvote}    ↑ {up}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['BreakingBad'])
    @commands.cooldown(1, 5, BucketType.user)
    async def BB(self, ctx):
        subreddit = reddit.subreddit('okbuddychicanery')
        top = subreddit.hot(limit=100)
        allsubs = []
        for sub in top:
            allsubs.append(sub)
        random_sub = random.choice(allsubs)
        
        if random_sub.subreddit.over18 == True:
            await ctx.send('Please navigate to a NSFW channel to use this. Most likey due to a meme containing 18+ content.')
            return
        
        name = random_sub.title
        url = random_sub.url
        comments = random_sub.comments
        upvote = random_sub.upvote_ratio
        up = random_sub.score
        author = random_sub.author
        sub = random_sub.subreddit

        embed = discord.Embed(
            title= name,
            color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
        )
        embed.set_author(name=f'Posted by {author} from r/{sub}')
        embed.set_image(url=url)
        embed.set_footer(text=f'\t💬 {len(comments)}    ⇅ {upvote}    ↑ {up}')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.cooldown(1, 60, BucketType.user)
    async def reddit(self, ctx, subname=None):
        if subname == None:
            await ctx.send('Give a subreddit name!')
            return
        global msg
        subreddit = reddit.subreddit('{}'.format(subname))
        if subreddit.over18 == True:
            msg = await ctx.send('Over 18 Content Detected!')
            if ctx.channel.is_nsfw() == True:
                all_subs = []
                top = subreddit.hot(limit=100)

                for submission in top:
                    all_subs.append(submission)

                random_sub = random.choice(all_subs)

                name = random_sub.title
                url = random_sub.url
                comments = random_sub.comments
                upvote = random_sub.upvote_ratio
                up = random_sub.score
                author = random_sub.author
                sub = random_sub.subreddit

                embed = discord.Embed(
                    title= name,
                    color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
                )
                embed.set_author(name=f'Posted by {author} from r/{sub}')
                embed.set_image(url=url)
                embed.set_footer(text=f'\t💬 {len(comments)}    ⇅ {upvote}    ↑ {up}')
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.set_thumbnail(url='https://rlv.zcache.com/return_to_sender_wrong_address_rubber_stamp-rabe45bc54d524b0ca9b150ee9d222490_6o1xx_540.jpg?rlvnet=1')
                embed.add_field(name='NOPE', value='This command must be used in a `NSFW` channel since this command is explicit!')
                await ctx.send(embed=embed)
        else:
            all_subs = []
            top = subreddit.hot(limit=100)

            for submission in top:
                all_subs.append(submission)

            random_sub = random.choice(all_subs)

            name = random_sub.title
            url = random_sub.url
            comments = random_sub.comments
            upvote = random_sub.upvote_ratio
            up = random_sub.score
            author = random_sub.author
            sub = random_sub.subreddit

            embed = discord.Embed(
                title= name,
                color=discord.colour.Color.from_rgb(random.randint(1, 255), random.randint(1, 255), random.randint(1, 255))
            )
            embed.set_author(name=f'Posted by {author} from r/{sub}')
            embed.set_image(url=url)
            embed.set_footer(text=f'\t💬 {len(comments)}    ⇅ {upvote}    ↑ {up}')
            await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(reddit(bot))
