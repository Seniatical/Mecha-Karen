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

## NOTE: Currently working this section

import asyncio

import discord
from discord.ext import commands
import random

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client
        
        column = self.client['Bot']
        self.table = column['Tags']

        bot.cache.cache['Tags'] = dict()
        bot.cache.cache['Tags']['Popularity'] = dict()

        for tag in self.table.find():
            if bot.cache.cache['Tags'].get(tag['_id']):
                bot.cache.cache['Tags'][tag['_id']].update({tag['name']: tag})
            else:
                bot.cache.cache['Tags'].update({tag['_id']: {tag['name']: tag}})

    def normalize(self, tag_content: str) -> str:
        pass

    def get_tag_info(self, ctx: commands.Context, name: str, value: str) -> dict:
        tag = {'_id': ctx.guild.id, 'author': ctx.author.id,
               'created_at': ctx.message.created_at.isoformat(),
               'updated_at': ctx.message.created_at.isoformat(),
               'name': name, 'value': value, 'uses': 0,
               }
        return tag

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tag(self, *, tag: str = None):
        if not tag:
            return

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def delete(self, ctx: commands.Context, *, tag: str):

        tags: dict = self.bot.cache.cache['Tags'].get(ctx.guild.id)
        if not tags or not tags.get(tag):
            return await ctx.message.reply(content='This tag doesn\'t exist!')
        tag: dict = tags[tag]

        if not tag['author'] == ctx.author.id and not ctx.author.guild_permissions.manage_guild:
            return await ctx.message.reply(content='This tag doesn\'t belong to you.')

        confirmed: bool = False

        def check(m):
            global confirmed

            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['y', 'yes']:
                confirmed = True
                return True
            elif m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['n', 'no']:
                return True
        try:
            await ctx.send('Are you sure you would like to delete this tag, response with `(y / n)`')
            message: discord.Message = await self.bot.wait_for('message', check, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.message.reply(content='You didn\'t confirm in time!')
        if not confirmed:
            return await message.reply(content='Ok, I will not delete this tag!')

        await self.bot.loop.run_in_executor(
            None, self.table.delete_one, {'_id': ctx.guild.id, 'name': tag['name']}
        )

        return await message.reply(content='Successfully deleted this tag for you!')

    @tag.command(aliases=['add'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx: commands.Context):
        await ctx.send('What will be the name for this tag, keep it under **50** characters!')
        try:
            message: discord.Message = await self.bot.wait_for('message', lambda m: m.author.id == ctx.author.id and ctx.channel.id == m.channel.id)
        except asyncio.TimeoutError:
            return await ctx.message.reply(content='Failed to create tag, You didn\'t provide a name in time!')
        if len(message.content) > 50:
            return await message.reply(content='Failed to create tag, Your tags name must be under **50** characters')

        await message.reply(content='Ok then, your tags name will be called **%s**, now what will be the tags content?' % message.content)


def setup(bot):
    bot.add_cog(Tags(bot))
