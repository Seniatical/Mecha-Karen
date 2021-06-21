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

import asyncio
import datetime

import TagScriptEngine
import discord
import pymongo.cursor
from discord.ext import commands
import TagScriptEngine as tagscript
from pydantic import BaseModel
from core.abc import KarenMixin, KarenMetaClass


class Tags(commands.Cog, KarenMixin, metaclass=KarenMetaClass):
    def __init__(self, bot):
        super().__init__()

        self.bot = bot
        self.client = bot.client
        
        column = self.client['Bot']
        self.table = column['Tags']

        bot.cache.cache['Tags'] = dict()

        self.max_tags = 10

        for tag in self.table.find():
            guild = bot.get_guild(tag['_id'])

            if not guild:
                continue

            if bot.cache.cache['Tags'].get(tag['_id']):
                bot.cache.cache['Tags'][tag['_id']].update({tag['name']: self.Tag(
                    content=tag['value'], name=tag['name'], guild=guild.id,
                    author=getattr(guild.get_member(tag['author']), 'id', 0),
                    created_at=datetime.datetime.fromisoformat(tag['created_at']),
                    updated_at=datetime.datetime.fromisoformat(tag['updated_at']),
                    uses=tag['uses']
                )})
            else:
                self.bot.cache.cache['Tags'][tag['_id']] = dict()
                self.bot.cache.cache['Tags'][tag['_id']][tag['name']] = self.Tag(
                    content=tag['value'], name=tag['name'], guild=guild.id,
                    author=getattr(guild.get_member(tag['author']), 'id', 0),
                    created_at=datetime.datetime.fromisoformat(tag['created_at']),
                    updated_at=datetime.datetime.fromisoformat(tag['updated_at']),
                    uses=tag['uses']
                )

        tagscript_blocks = [
            tagscript.MathBlock(),
            tagscript.RandomBlock(),
            tagscript.RangeBlock(),
            tagscript.AnyBlock(),
            tagscript.IfBlock(),
            tagscript.AllBlock(),
            tagscript.BreakBlock(),
            tagscript.StrfBlock(),
            tagscript.StopBlock(),
            tagscript.AssignmentBlock(),
            tagscript.FiftyFiftyBlock(),
            tagscript.ShortCutRedirectBlock("args"),
            tagscript.LooseVariableGetterBlock(),
            tagscript.SubstringBlock(),
            tagscript.EmbedBlock(),
            tagscript.ReplaceBlock(),
            tagscript.PythonBlock(),
            tagscript.URLEncodeBlock(),
            tagscript.RequireBlock(),
            tagscript.BlacklistBlock(),
            tagscript.CommandBlock(),
            tagscript.OverrideBlock(),
        ]

        self.engine = TagScriptEngine.Interpreter(tagscript_blocks)

    class Tag(BaseModel):
        r""" An object which represents a TAG """
        content: str
        name: str
        guild: int
        author: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        uses: int

    async def save_tag(self, ctx: commands.Context, name: str, value: str):
        tag_info_as_dict = await self.get_tag_info(ctx, name, value)
        tag = self.Tag(content=value, name=name, guild=ctx.guild.id, author=ctx.author.id,
                       created_at=ctx.message.created_at, updated_at=ctx.message.created_at,
                       uses=0
                       )
        try:
            self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag
        except KeyError:
            self.bot.cache.cache['Tags'][ctx.guild.id] = dict()
            self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag

        await self.bot.loop.run_in_executor(
            None, self.table.insert_one, tag_info_as_dict
        )

    @staticmethod
    async def get_tag_info(ctx: commands.Context, name: str, value: str) -> dict:
        tag = {'_id': ctx.guild.id, 'author': ctx.author.id,
               'created_at': ctx.message.created_at.isoformat(),
               'updated_at': ctx.message.created_at.isoformat(),
               'name': name, 'value': value, 'uses': 0,
               }
        return tag

    @staticmethod
    async def get_seeds(ctx: commands.Context, tag):
        author = {
            'avatar': ctx.author.avatar,
            'name': ctx.author.name,
            'id': ctx.author.id,
            'display_name': ctx.author.display_name,
            'mention': ctx.author.mention
        }

        seed = {
            "author": author,
            "user": author,
            "tag_owner": tag.author,
            "tag_name": tag.name,
            "tag_uses": tag.uses
        }
        if ctx.guild:
            guild = {
                'name': ctx.guild.name,
                'icon': ctx.guild.icon,
                'id': ctx.guild.id,
                'owner': ctx.guild.owner
            }
            seed.update(guild=guild, server=guild)
        return seed

    async def tag_exists(self, ctx: commands.Context, name: str):
        tag = await self.bot.loop.run_in_executor(
            None, self.table.find_one, {'_id': ctx.guild.id, 'name': name}
        )
        if tag is not None:
            return True
        return False

    async def surpassed_limit(self, ctx: commands.Context):
        tags: pymongo.cursor.Cursor = await self.bot.loop.run_in_executor(
            None, self.table.find, {'_id': ctx.guild.id, 'author': ctx.author.id}
        )
        return tags.count() > self.max_tags

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def tag(self, ctx: commands.Context, *, tag: str):
        try:
            tags = self.bot.cache.cache['Tags'][ctx.guild.id]
        except KeyError:
            tags = None

        if not tags or not tags.get(tag):
            return await ctx.message.reply(content='This tag doesn\'t exist', mention_author=False)
        tag = tags[tag]
        seeds = await self.get_seeds(ctx, tag)

        content = self.engine.process(tag.content, seed_variables=seeds)

        if ctx.message.reference and ctx.message.reference.resolved:
            return await ctx.message.reference.resolved.reply(content=content.body, mention_author=False)
        return await ctx.send(content.body)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def delete(self, ctx: commands.Context, *, tag: str):
        global confirmed

        tags: dict = self.bot.cache.cache['Tags'].get(ctx.guild.id)
        if not tags or not tags.get(tag):
            return await ctx.message.reply(content='This tag doesn\'t exist!')
        tag = tags[tag]

        if not tag.author == ctx.author.id and not ctx.author.guild_permissions.manage_guild:
            return await ctx.message.reply(content='This tag doesn\'t belong to you.')

        confirmed = False

        def check(m):
            global confirmed

            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['y', 'yes']:
                confirmed = True
                return True
            elif m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['n', 'no']:
                return True
        try:
            await ctx.send('Are you sure you would like to delete this tag, response with `(y / n)`')
            message: discord.Message = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.message.reply(content='You didn\'t confirm in time!')
        if not confirmed:
            return await message.reply(content='Ok, I will not delete this tag!')

        await self.bot.loop.run_in_executor(
            None, self.table.delete_one, {'_id': ctx.guild.id, 'name': tag.name}
        )
        self.bot.cache.cache['Tags'][ctx.guild.id].pop(tag.name)

        return await message.reply(content='Successfully deleted this tag for you!')

    @tag.command(aliases=['add'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def create(self, ctx: commands.Context):
        await ctx.send('What will be the name for this tag, keep it under **50** characters!')
        try:
            tag_name: discord.Message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and ctx.channel.id == m.channel.id, timeout=30.0)
        except asyncio.TimeoutError:
            return await ctx.message.reply(content='Failed to create tag, You didn\'t provide a name in time!')
        if len(tag_name.content) > 50:
            return await tag_name.reply(content='Failed to create tag, Your tags name must be under **50** characters')

        if await self.tag_exists(ctx, tag_name.content):
            return await tag_name.reply(content='This tag already exists in your server!')

        await tag_name.reply(content='Ok then, your tags name will be called **%s**, now what will be the tags content?' % tag_name.content)

        try:
            tag_content: discord.Message = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and ctx.channel.id == m.channel.id, timeout=30.0)
        except asyncio.TimeoutError:
            return await tag_name.reply(content='Failed to create tag, You didn\'t respond in time!')

        if await self.surpassed_limit(ctx):
            return await tag_content.reply(content='You have already reached the maximum amount of tags, which is **%s**' % self.max_tags)

        ## No point checking for content length because the bot just sends what they said

        await self.save_tag(ctx, tag_name.content, tag_content.content)

        return await ctx.send('Created a new tag for this server using the name **%s**' % tag_name.content)


def setup(bot):
    bot.add_cog(Tags(bot))

