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

import discord, random
from discord.ext import commands
from Scrapers import UD, YT
import datetime, requests
from youtube_search import YoutubeSearch
from Helpers import emoji
import asyncio

class scrapers(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            await message.edit('{} The word **`{}`** wasnt found!'.format(word.title()))

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def yt(self, ctx, *, search : str=None):
        if search == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('What video are you searching for?')
        results = YoutubeSearch(YT.yt_search(search), max_results=1).to_dict()
        if results == []:
            return await ctx.send('**No Videos were Found!**')
        embed = discord.Embed(
            title=results[0]['title'],
            colour=discord.Color.red(),
            description='**Description:**\n```' + results[0]['long_desc'] + '```',
            timestamp=datetime.datetime.utcnow()
        ).set_footer(text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.set_thumbnail(url=results[0]['thumbnails'][0])
        embed.add_field(name='Channel:', value=results[0]['channel'])
        embed.add_field(name='Duration:', value=results[0]['duration'])
        embed.add_field(name='Views:', value=results[0]['views'].split()[0])
        embed.add_field(name='Link:', value='https://youtube.com{}'.format(results[0]['url_suffix']))
        await ctx.send(embed=embed)

    @commands.command()
    async def github(self, *, repository : str=None):
        if repository == None:
            return
        return

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
    bot.add_cog(scrapers(bot))
