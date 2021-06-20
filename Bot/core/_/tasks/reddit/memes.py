from utility import emojis as emoji
from utility import abbrev_denary as convert_size
import random
import discord
global stack
from requests.utils import requote_uri
import asyncio

stack = []

def add_global(new_stack: list) -> None:
    global stack
    stack = new_stack

async def task(bot, reddit):
    while True:
        bot.cache.cache['memes'].clear()
        sub = await reddit.subreddit('memes')
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
                color=random.randint(0x000000, 0xFFFFFF),
                url=await bot.loop.run_in_executor(
                    None, requote_uri,
                    f'https://www.reddit.com/r/dankmemes/comments/{_submission.id}/{_submission.title}/'
                )
            )
            try:
                embed.set_author(name='Posted by {} from r/{}'.format(name_, sub), icon_url=name_.icon_img,
                                 url=f'https://www.reddit.com/user/{name_}/')
            except Exception:
                embed.set_author(name='Posted by {} from r/{}'.format(name_, sub),
                                 url=f'https://www.reddit.com/user/{name_}/')
            embed.set_image(url=url)
            embed.set_footer(
                text='{} {}   |   {} {}'.format(emoji.UNICODE['up'], convert_size(up), emoji.UNICODE['text'],
                                                convert_size(comments)))
            bot.cache.cache['memes'].append(embed)
        await asyncio.sleep(3600)