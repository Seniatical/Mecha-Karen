import random
import datetime
import time

import discord
from discord import File
from discord.ext import commands
from discord.ext.commands import BucketType, cooldown, MissingRequiredArgument
import os
import praw

class Images(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Memes Cog is ready')

    @commands.command(aliases=['meme'])
    @commands.cooldown(1, 5, BucketType.user)
    async def memes(self, ctx):
        reddit = praw.Reddit(client_id='z0tV5Vb8-xHnYA',
                        client_secret='EgmNP1VmT-IpIMj-7auUMM8E0W0',
                        username='python_praw123',
                        password='python123',
                        user_agent='python123')
        subreddit = reddit.subreddit('Memes')
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
    bot.add_cog(Images(bot))
