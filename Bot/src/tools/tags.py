import asyncio
import datetime
import io
import textwrap

import discord
from discord.ext import commands
import TagScriptEngine as tagscript
from pydantic import BaseModel
from difflib import get_close_matches

import utility.metrics
from utility.min import get_permissions
from core.abc import KarenMixin, KarenMetaClass

from adapters.tag import TagAdapter
from adapters.args import ArgumentAdapter


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
            tag_id = tag['_id']
            guild, name, *args = tag_id.split('/')
            ## If `/` in the tag_name it will be filtered into args
            name += '/'.join(args)
            ## We get the original tag name by rejoining the args with a `/`

            tag['_id'] = int(guild)
            tag['name'] = name

            guild = bot.get_guild(tag['_id'])

            if not guild:
                continue

            if bot.cache.cache['Tags'].get(tag['_id']):
                bot.cache.cache['Tags'][tag['_id']].update({tag['name']: self.Tag(
                    content=tag['value'], name=tag['name'], guild=guild.id,
                    author=getattr(guild.get_member(tag['author']), 'id', 0),
                    created_at=datetime.datetime.fromtimestamp(tag['created_at']),
                    updated_at=datetime.datetime.fromtimestamp(tag['updated_at']),
                    uses=tag['uses'], nsfw=tag['nsfw'], mod=tag['mod']
                )})
            else:
                self.bot.cache.cache['Tags'][tag['_id']] = dict()
                self.bot.cache.cache['Tags'][tag['_id']][tag['name']] = self.Tag(
                    content=tag['value'], name=tag['name'], guild=guild.id,
                    author=getattr(guild.get_member(tag['author']), 'id', 0),
                    created_at=datetime.datetime.fromtimestamp(tag['created_at']),
                    updated_at=datetime.datetime.fromtimestamp(tag['updated_at']),
                    uses=tag['uses'], nsfw=tag['nsfw'], mod=tag['mod']
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

        self.engine = tagscript.Interpreter(tagscript_blocks)

    class Tag(BaseModel):
        r""" An object which represents a TAG """
        content: str
        name: str
        guild: int
        author: int
        created_at: datetime.datetime
        updated_at: datetime.datetime
        uses: int
        nsfw: bool = False
        mod: bool = False

    def format_tag(self, tag_id):
        guild, name, *args = tag_id.split('/')
        ## If `/` in the tag_name it will be filtered into args
        name += '/'.join(args)
        ## We get the original tag name by rejoining the args with a `/`

        return {'guild': guild, 'name': name}

    async def save_tag(self, ctx: commands.Context, name: str, value: str):
        tag_info_as_dict = await self.get_tag_info(ctx, name, value)
        tag = self.Tag(content=value, name=name, guild=ctx.guild.id, author=ctx.author.id,
                       created_at=ctx.message.created_at, updated_at=ctx.message.created_at,
                       uses=0, nsfw=False, mod=False
                       )
        try:
            self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag
        except KeyError:
            self.bot.cache.cache['Tags'][ctx.guild.id] = dict()
            self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag

        await self.bot.loop.run_in_executor(
            None, self.table.insert_one, tag_info_as_dict
        )

    async def update_tag(self, ctx: commands.Context, old_tag: dict, new_tag: str, value: str):
        guild = ctx.guild
        tag_id = old_tag['_id']
        data = self.format_tag(tag_id)

        ## Simply just update the dict
        new_tag = f'{guild.id}/{new_tag}'
        old_tag['_id'] = new_tag
        old_tag['value'] = value
        old_tag['updated_at'] = datetime.datetime.utcnow().timestamp()

        guild, name = self.format_tag(new_tag).values()

        await self.bot.loop.run_in_executor(
            None, self.table.delete_one, {'_id': tag_id}
        )
        await self.bot.loop.run_in_executor(
            None, self.table.insert_one, old_tag
        )

        tag = self.Tag(content=value, name=name, guild=ctx.guild.id, author=ctx.author.id,
                       created_at=old_tag['created_at'], updated_at=old_tag['updated_at'],
                       uses=old_tag['uses'], nsfw=old_tag['nsfw'], mod=old_tag['mod']
                       )

        self.bot.cache.cache['Tags'][ctx.guild.id].pop(data['name'])
        self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag

    @staticmethod
    async def get_tag_info(ctx: commands.Context, name: str, value: str) -> dict:
        tag = {'_id': f'{ctx.guild.id}/{name}', 'author': ctx.author.id,
               'created_at': ctx.message.created_at.timestamp(),
               'updated_at': ctx.message.created_at.timestamp(),
               'value': value, 'uses': 0, 'nsfw': False, 'mod': False
               }
        return tag

    @staticmethod
    async def get_seed_from_context(ctx: commands.Context, tag, *args):
        author = tagscript.MemberAdapter(ctx.author)
        target = tagscript.MemberAdapter(ctx.message.mentions[0]) if ctx.message.mentions else author
        channel = tagscript.ChannelAdapter(ctx.channel)

        tag = TagAdapter(tag)
        args = ArgumentAdapter(*args)

        seed = {
            "author": author,
            "user": author,
            "target": target,
            "member": target,
            "channel": channel,
            "tag": tag,
            "args": args
        }
        if ctx.guild:
            guild = tagscript.GuildAdapter(ctx.guild)
            seed.update(guild=guild, server=guild)
        return seed

    async def tag_exists(self, ctx: commands.Context, name: str):
        tag = await self.bot.loop.run_in_executor(
            None, self.table.find_one, {'_id': f'{ctx.guild.id}/{name}'}
        )
        if tag is not None:
            return tag
        return False

    async def is_command(self, name: str):
        return bool(self.bot.get_command(name))

    async def surpassed_limit(self, ctx: commands.Context):
        tags: int = await self.bot.loop.run_in_executor(
            None, self.table.count_documents, {'_id': {'$regex': f'^{ctx.guild.id}'}, 'author': ctx.author.id}
        )
        return (tags + 1) > self.max_tags

    @commands.Cog.listener()
    async def on_message(self, message):
        r""" Allows usage of `-karen` so it becomes like a cmd """

        tags = self.bot.cache.cache['Tags'].get(getattr(getattr(message, 'guild', None), 'id', None))
        if not tags:
            return

        prefixes = self.bot.prefix.cache.get(message.guild.id)
        tag = None

        if not prefixes:
            if not message.content.startswith('-'):
                return
            tag = message.content[1:]

        for prefix in prefixes:
            # Shouldn't be too slow as the maximum they can have is 7
            if message.content.startswith(prefix):
                tag = message.content[len(prefix):]
                break

        if not tag:
            return
        # Args may be passed through so we need to refilter to sort the args out

        tag, *args = tag.split(' ')

        try:
            tag = tags[tag.lower()]
        except KeyError:
            return

        # Now we have the tag object

        seeds = await self.get_seed_from_context(await self.bot.get_context(message), tag, *args)

        content = await self.bot.loop.run_in_executor(
            None, self.engine.process, tag.content, seeds
        )

        if not message.channel.nsfw and tag.nsfw:
            raise commands.NSFWChannelRequired() from None

        if tag.mod and not message.author.guild_permissions.manage_messages:
            raise commands.MissingPermissions(missing_perms=['manage_messages'])
        try:
            return await message.channel.send(content.body)
        except discord.errors.Forbidden:
            return

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True, embed_links=True)
    async def tags(self, ctx: commands.Context):
        try:
            tags = self.bot.cache.cache['Tags'][ctx.guild.id]
        except KeyError:
            tags = None
        if not tags:
            try:
                return await ctx.message.reply(content='You do not have any tags!')
            except Exception:
                return await ctx.send(content='You do not have any tags!')

        def tag_filter(tag):
            return tag.author == ctx.author.id

        tags = list(await self.bot.loop.run_in_executor(None, filter, tag_filter, tags.values()))
        if not tags:
            try:
                return await ctx.message.reply(content='You do not have any tags!')
            except Exception:
                return await ctx.send(content='You do not have any tags!')
        embed = discord.Embed(title='%s\'s Tags' % ctx.author.display_name, colour=discord.Colour.blue())
        description = ''
        for tag in tags:
            description += f'{tags.index(tag, 0) + 1}. {tag.name}\n'
        embed.description = description

        return await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def tag(self, ctx: commands.Context, tag: str, *args):
        try:
            tags = self.bot.cache.cache['Tags'][ctx.guild.id]
        except KeyError:
            tags = None

        tag = tag.lower()

        if not tags or not tags.get(tag):
            similar = await self.bot.loop.run_in_executor(
                None, get_close_matches, tag, tags.keys()
            )
            if not similar:
                return await ctx.message.reply(content='This tag doesn\'t exist', mention_author=False)
            else:
                return await ctx.message.reply(content="This tag doesn't exist, perhaps you ment\n{}".format(
                    ', '.join(map(lambda _: '`' + _ + '`', similar[:10]))
                ))
        tag = tags[tag]

        if tag.nsfw and not ctx.channel.nsfw:
            raise commands.NSFWChannelRequired(channel=ctx.channel) from None
        if tag.mod and not ctx.author.guild_permissions.manage_messages:
            raise commands.MissingPermissions(missing_perms=['manage_messages'])

        seeds = await self.get_seed_from_context(ctx, tag, *args)

        try:
            content = self.engine.process(tag.content, seed_variables=seeds)
        except Exception as e:
            return await ctx.send(f'Woops something went wrong when it shouldn\'t have!')

        await self.bot.loop.run_in_executor(
            None, self.table.update_one, {'_id': f'{tag.guild}/{tag.name}'}, {'$inc': {'uses': 1}}
        )
        tag.uses += 1
        self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag

        if ctx.message.reference and ctx.message.reference.resolved:
            try:
                return await ctx.message.reference.resolved.reply(content=content.body, mention_author=False)
            except Exception:
                pass
        return await ctx.send(content.body)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True, embed_links=True)
    async def info(self, ctx: commands.Context, *, tag: str):
        try:
            tags = self.bot.cache.cache['Tags'][ctx.guild.id]
        except KeyError:
            tags = None

        tag = tag.lower()

        if not tags or not tags.get(tag):
            return await ctx.message.reply(content='This tag doesn\'t exist', mention_author=False)
        tag = tags[tag]

        embed = discord.Embed(title=tag.name.capitalize(), colour=discord.Colour.blue())
        author = ctx.guild.get_member(tag.author)

        if not author:
            embed.set_author(name='N/A - User has left this server')
        else:
            embed.set_author(name=author.display_name, icon_url=author.avatar)

        embed.add_field(name='Created At', value=tag.created_at.strftime('%a, %#d %b %Y, %I:%M %p'))
        embed.add_field(name='Last Updated', value=tag.updated_at.strftime('%a, %#d %b %Y, %I:%M %p'))
        embed.add_field(name='Meta', value=f'This tag **{"has not" if not tag.nsfw else "has"}** been marked\
         as **NSFW** and is currently **{"avaliable for everyone" if not tag.mod else "users with `manage_messages`"}**.')

        embed.add_field(name='Short Content', value=textwrap.shorten(tag.content, 100), inline=False)
        embed.set_footer(text=f'This tag has been used %s times!' % utility.metrics.abbrev_denary(tag.uses))

        return await ctx.send(embed=embed)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def claim(self, ctx: commands.Context, *, tag: str):
        try:
            tags = self.bot.cache.cache['Tags'][ctx.guild.id]
        except KeyError:
            tags = None

        tag = tag.lower()

        if not tags or not tags.get(tag):
            return await ctx.message.reply(content='This tag doesn\'t exist', mention_author=False)
        tag = tags[tag]

        author = ctx.guild.get_member(tag.author)
        if author:
            try:
                return await ctx.message.reply(content='This tag already belongs to somebody!')
            except Exception:
                return await ctx.send(content='This tag already belongs to somebody!')

        if await self.surpassed_limit(ctx):
            try:
                return await ctx.message.reply(content='You have already reached the max number of tags!')
            except Exception:
                return await ctx.send(content='You have already reached the max number of tags!')

        tag.author = ctx.author.id
        tag.updated_at = datetime.datetime.utcnow().timestamp()

        await self.bot.loop.run_in_executor(
            None, self.table.update_one, {'_id': f'{tag.guild}/{tag.name}'},
            {'$set': {'author': ctx.author.id, 'updated_at': tag.updated_at}}
        )

        try:
            return await ctx.message.reply(content=f"The tag **{tag.name}** now belongs to {ctx.author.mention}!")
        except Exception:
            return await ctx.send(content=f"The tag **{tag.name}** now belongs to {ctx.author.mention}!")

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def delete(self, ctx: commands.Context, *, tag: str):
        global confirmed

        tag = tag.lower()

        tags: dict = self.bot.cache.cache['Tags'].get(ctx.guild.id)
        if not tags or not tags.get(tag):
            try:
                return await ctx.message.reply(content='This tag doesn\'t exist!')
            except Exception:
                return await ctx.send(content='This tag doesn\'t exist!')
        tag = tags[tag]

        if not tag.author == ctx.author.id and not ctx.author.guild_permissions.manage_guild:
            try:
                return await ctx.message.reply(content='This tag doesn\'t belong to you.')
            except Exception:
                return await ctx.send(content='This tag doesn\'t belong to you.')

        confirmed = False

        def check(m):
            global confirmed

            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['y', 'yes']:
                confirmed = True
                return True
            elif m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['n', 'no']:
                return True

        try:
            await ctx.send('Are you sure you would like to delete this tag, respond with `(y / n)`')
            message: discord.Message = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            try:
                return await ctx.message.reply(content='You didn\'t confirm in time!')
            except Exception:
                return await ctx.send(content='You didn\'t confirm in time!')
        if not confirmed:
            try:
                return await message.reply(content='Ok, I will not delete this tag')
            except Exception:
                return await ctx.send(content='Ok, I will not delete this tag')

        await self.bot.loop.run_in_executor(
            None, self.table.delete_one, {'_id': f'{ctx.guild.id}/{tag.name}'}
        )
        self.bot.cache.cache['Tags'][ctx.guild.id].pop(tag.name)

        try:
            return await message.reply(content='Successfully deleted this tag for you!')
        except Exception:
            return await ctx.send(content='Successfully deleted this tag for you!')

    @tag.command(aliases=['add'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def create(self, ctx: commands.Context):
        warnings = []

        await ctx.send('What will be the name for this tag, keep it under **50** characters!')
        try:
            tag_name: discord.Message = await self.bot.wait_for('message', check=lambda
                m: m.author.id == ctx.author.id and ctx.channel.id == m.channel.id, timeout=30.0)
        except asyncio.TimeoutError:
            try:
                return await ctx.message.reply(content='Failed to create tag, You didn\'t provide a name in time!')
            except Exception:
                return await ctx.send(content='Failed to create tag, You didn\'t provide a name in time!')

        if len(tag_name.content) > 50:
            warnings.append('[Warning] Tag name was greater then 50 letters, scaled it down')
            tag_name.content = tag_name.content[:50]

        if ' ' in tag_name.content:
            warnings.append('[Warning] Tag contained a space in its name, replaced with `-`')
            tag_name.content = tag_name.content.replace(' ', '-')

        if await self.tag_exists(ctx, tag_name.content):
            try:
                return await tag_name.reply(content='This tag already exists in your server!')
            except Exception:
                return await ctx.send(content='This tag already exists in your server!')

        if await self.is_command(tag_name.content):
            try:
                return await tag_name.reply(content='This tag mirrors a command name, Name it something unique!')
            except Exception:
                return await ctx.send(content='This tag mirrors a command name, Name it something unique!')

        try:
            await tag_name.reply(
                content='Ok then, your tags name will be called **%s**, now what will be the tags content?' % tag_name.content)
        except Exception:
            await ctx.send(
                content='Ok then, your tags name will be called **%s**, now what will be the tags content?' % tag_name.content)

        try:
            tag_content: discord.Message = await self.bot.wait_for('message', check=lambda
                m: m.author.id == ctx.author.id and ctx.channel.id == m.channel.id, timeout=(60 * 30))
        except asyncio.TimeoutError:
            try:
                return await tag_name.reply(content='Failed to create tag, You didn\'t respond in time!')
            except Exception:
                return await ctx.send(content='Failed to create tag, You didn\'t respond in time!')

        if await self.surpassed_limit(ctx):
            try:
                return await tag_content.reply(
                    content='You have already reached the maximum amount of tags, which is **%s**' % self.max_tags)
            except Exception:
                return await ctx.send(
                    content='You have already reached the maximum amount of tags, which is **%s**' % self.max_tags)

        ## No point checking for content length because the bot just sends what they said

        await self.save_tag(ctx, tag_name.content.lower(), tag_content.content)

        embed = discord.Embed(title='Tag Created!', colour=discord.Colour.red())
        embed.description = 'Created a new tag for this server, using the name **%s**' % tag_name.content.lower()
        if warnings:
            embed.add_field(name='Warnings', value='\n'.join(warnings))
        return await ctx.send(embed=embed)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def edit(self, ctx: commands.Context, *, tag: str):
        warnings = []

        global confirmed
        stored_tag = await self.tag_exists(ctx, tag.lower())

        if not stored_tag:
            try:
                return await ctx.message.reply(content='This tag doesn\'t exist!')
            except Exception:
                return await ctx.send(content='This tag doesn\'t exist!')

        if not stored_tag['author'] == ctx.author.id and not ctx.author.guild_permissions.manage_guild:
            try:
                return await ctx.message.reply(content='This tag doesn\'t belong to you.')
            except Exception:
                return await ctx.send(content='This tag doesn\'t belong to you.')

        confirmed = False

        def check(m):
            global confirmed

            if m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['y', 'yes']:
                confirmed = True
                return True
            elif m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['n', 'no']:
                return True

        await ctx.send(
            'Would you like to change the name of your tag, If so keep it under **50 characters**? `(y / n)`')
        try:
             _ = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            try:
                await ctx.message.reply(content='Ok then we wont change the name of your tag.')
            except Exception:
                await ctx.send(content='Ok then we wont change the name of your tag.')
        else:
            if confirmed:
                await ctx.send('What is your tags new name?')
                try:
                    tag_name = await self.bot.wait_for(
                        'message',
                        check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id,
                        timeout=(60 * 30)
                    )
                except asyncio.TimeoutError:
                    try:
                        await ctx.message.reply(content='Ok then we wont change the name of your tag.')
                    except Exception:
                        await ctx.send(content='Ok then we wont change the name of your tag.')
                else:
                    if await self.is_command(tag_name.content):
                        try:
                            return await tag_name.reply(
                                content='This tag mirrors a command name, Name it something unique!')
                        except Exception:
                            return await ctx.send(content='This tag mirrors a command name, Name it something unique!')

                    if len(tag_name.content) > 50:
                        warnings.append('[Warning] Tag name was greater then 50 letters, scaled it down')
                        tag_name.content = tag_name.content[:50]

                    if ' ' in tag_name.content:
                        warnings.append('[Warning] Tag contained a space in its name, replaced with `-`')
                        tag_name.content = tag_name.content.replace(' ', '-')

                    try:
                        await tag_name.reply(content='The content of your tag has been updated.')
                    except Exception:
                        await ctx.send(content='The content of your tag has been updated.')

        confirmed = False

        await ctx.send(content='Would you like to change the content of this tag? `(y / n)`')

        try:
            _ = await self.bot.wait_for('message', check=check, timeout=30.0)
        except asyncio.TimeoutError:
            try:
                await ctx.message.reply(content='Ok then we wont change the content of your tag.')
            except Exception:
                await ctx.send(content='Ok then we wont change the content of your tag.')
        else:
            if confirmed:
                await ctx.send('What is the contents of your new tag?')
                try:
                    tag_body = await self.bot.wait_for(
                        'message',
                        check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id,
                        timeout=(60 * 30)
                    )
                except asyncio.TimeoutError:
                    try:
                        await ctx.message.reply(content='Ok then we wont change the content of your tag.')
                    except Exception:
                        await ctx.send(content='Ok then we wont change the content of your tag.')
                else:
                    body = tag_body.content
                    try:
                        await tag_body.reply(content='The content of your tag has been updated.')
                    except Exception:
                        await ctx.send(content='The content of your tag has been updated.')
            else:
                body = stored_tag['value']
                try:
                    await ctx.message.reply(content='The content of your tag **has not** been updated.')
                except Exception:
                    await ctx.send(content='The content of your tag **has not** been updated.')
        old_tag = self.format_tag(stored_tag['_id'])

        if tag == old_tag['name'] and body == stored_tag['value']:
            try:
                return await ctx.message.reply(content='Your tag **has not** been updated')
            except Exception:
                return await ctx.send(content='Your tag has **not been** updated')

        await self.update_tag(ctx, stored_tag, tag, body)

        embed = discord.Embed(title='Tag Updated!', colour=discord.Colour.red())
        embed.description = 'Update tag **%s** for this server!' % old_tag['name']
        if warnings:
            embed.add_field(name='Warnings', value='\n'.join(warnings))
        return await ctx.send(embed=embed)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def nsfw(self, ctx: commands.Context, *, tag: str):
        tag = tag.lower()

        tags: dict = self.bot.cache.cache['Tags'].get(ctx.guild.id)
        if not tags or not tags.get(tag):
            try:
                return await ctx.message.reply(content='This tag doesn\'t exist!')
            except Exception:
                return await ctx.send(content='This tag doesn\'t exist!')
        tag = tags[tag]

        if not tag.author == ctx.author.id and not ctx.author.guild_permissions.manage_guild:
            try:
                return await ctx.message.reply(content='This tag doesn\'t belong to you.')
            except Exception:
                return await ctx.send(content='This tag doesn\'t belong to you.')

        if not tag.nsfw:
            tag.nsfw = True
            content = "Marked the tag **%s** as NSFW!"
        else:
            tag.nsfw = False
            content = "The tag **%s** is no longer marked as NSFW."
        self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag

        await self.bot.loop.run_in_executor(
            None, self.table.update_one, {'_id': f'{ctx.guild.id}/{tag.name}'},
            {'$set': {'nsfw': tag.nsfw}}
        )

        return await ctx.send(content=content % tag.name)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mod(self, ctx: commands.Context, *, tag: str):
        tag = tag.lower()

        tags: dict = self.bot.cache.cache['Tags'].get(ctx.guild.id)
        if not tags or not tags.get(tag):
            try:
                return await ctx.message.reply(content='This tag doesn\'t exist!')
            except Exception:
                return await ctx.send(content='This tag doesn\'t exist!')
        tag = tags[tag]

        if not tag.author == ctx.author.id and not ctx.author.guild_permissions.manage_guild:
            try:
                return await ctx.message.reply(content='This tag doesn\'t belong to you.')
            except Exception:
                return await ctx.send(content='This tag doesn\'t belong to you.')

        if not tag.nsfw:
            tag.mod = True
            content = "Marked the tag **%s** as moderator only!"
        else:
            tag.mod = False
            content = "The tag **%s** is no longer marked as moderator only."
        self.bot.cache.cache['Tags'][ctx.guild.id][tag.name] = tag

        await self.bot.loop.run_in_executor(
            None, self.table.update_one, {'_id': f'{ctx.guild.id}/{tag.name}'},
            {'$set': {'mod': tag.mod}}
        )

        return await ctx.send(content=content % tag.name)

    @tag.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(read_message_history=True, send_messages=True)
    async def raw(self, ctx: commands.Context, *, tag: str):
        try:
            tags = self.bot.cache.cache['Tags'][ctx.guild.id]
        except KeyError:
            tags = None

        tag = tag.lower()

        if not tags or not tags.get(tag):
            return await ctx.message.reply(content='This tag doesn\'t exist', mention_author=False)
        tag = tags[tag]

        if len(tag.content) > 500:
            with io.BytesIO() as buffer:
                buffer.write(tag.content.encode('utf-8', errors='ignore'))
                buffer.seek(0)
                file = discord.File(fp=buffer, filename='%s.log' % tag.name)
            return await ctx.send('Here is the raw contents of your tag.', file=file)
        else:
            return await ctx.send(content=tag.content)

def setup(bot):
    bot.add_cog(Tags(bot))
