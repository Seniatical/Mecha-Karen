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

import typing

import discord
from discord.ext import commands
import datetime
import io
from discord.ext.commands import BucketType, cooldown
import asyncio
from utility import emojis as emoji
from utility import colours
from utility import checks
import random
import re
import aiofiles
import unicodedata


def convert(time: int, unit):
    unit = unit.lower()
    if unit == 's':
        return time
    elif unit == 'm':
        return time * 60
    elif unit == 'h':
        return (time * 60) * 60
    elif unit == 'd':
        return ((time * 60) * 60) * 24


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.m_conv = commands.MemberConverter()
        self.r_conv = commands.RoleConverter()
        self.client = bot.client

        table = bot.client['Bot']

        self.mute_col = table['Mutes']

        bot.mutes = self.mute_col

        self.cache = bot.cache

        if not self.cache.cache.get('Mute-Tasks'):
            self.cache.cache.update({'Mute-Tasks': {}})
            print('Added Sub Section Into `Internal Cache` - `Mute-Tasks`')

    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    async def muterole(self, ctx):
        role = self.mute_col.find_one({'_id': ctx.guild.id})
        if not role:
            desc = 'You currently have no mute role setup!'
            colour = discord.Colour.red()
        else:
            _id = role['role']
            role = discord.utils.get(ctx.guild.roles, id=_id)

            if not role:
                desc = 'I can no longer trace your mute role, Please update it!'
                colour = discord.Colour.red()
            else:
                role = getattr(role, 'mention', None) or '*Deleted Role*'
                desc = 'Your mute role as been set as {}'.format(role)
                colour = discord.Colour.green()
        await ctx.send(embed=discord.Embed(
            description=desc,
            colour=colour
        ))

    @muterole.command()
    @commands.cooldown(1, 10, BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    async def set(self, ctx, role: discord.Role):
        has_role = self.mute_col.find_one({'_id': ctx.guild.id})
        if not has_role:
            desc = 'Set your mute role as %s' % role.mention
            self.mute_col.insert_one({'_id': ctx.guild.id, 'role': role.id})
        else:

            if has_role['role'] == role.id:
                return await ctx.send('Your mute role has already been set to this role!')

            prev_role = discord.utils.get(ctx.guild.roles, id=has_role['role'])
            prev_role = getattr(prev_role, 'mention', None) or '*Deleted Role*'

            desc = 'Replaced your current mute role (%s) with %s' % (prev_role, role.mention)
            self.mute_col.update_one({'_id': ctx.guild.id}, {'$set': {'role': role.id}})

        await ctx.send(embed=discord.Embed(
            description=desc,
            colour=discord.Colour.green()
        ))

    @muterole.command(aliases=['delete'])
    @commands.cooldown(1, 10, BucketType.user)
    @commands.has_guild_permissions(manage_guild=True)
    async def remove(self, ctx):
        has_role = self.mute_col.find_one({'_id': ctx.guild.id})

        if not has_role:
            return await ctx.send(embed=discord.Embed(
                description='You have not set your mute role yet!',
                colour=discord.Colour.red()
            ))

        prev_role = discord.utils.get(ctx.guild.roles, id=has_role['role'])
        prev_role = getattr(prev_role, 'mention', None) or '*Deleted Role*'

        self.mute_col.delete_one({'_id': ctx.guild.id})
        await ctx.send(embed=discord.Embed(
            description='Deleted your current mute role which was set as %s' % prev_role,
            colour=discord.Colour.green()
        ))

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @cooldown(1, 5, BucketType.user)
    async def clear(self, ctx, amount: str, *, _filter: str = None) -> discord.Member:
        global passed, _re

        try:
            amount = int(amount)
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Amount to purge must be number!',
                colour=discord.Colour.red()
            ))
        if amount > 100:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Amount to purge must be cannot be larger than **100**!',
                colour=discord.Colour.red()
            ))
        if not _filter:
            await ctx.channel.purge(limit=(amount + 1), check=lambda m: m.id != ctx.message.id)
            return await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Cleared **{}** messages.'.format(amount),
                colour=discord.Colour.green()
            ))

        try:
            member = await self.m_conv.convert(ctx, _filter)
        except commands.errors.MemberNotFound:
            member = None
        if member:
            passed = 0

            def check(m):
                global passed

                if m.author.id == member.id and m.id != ctx.message.id:
                    passed += 1
                    return True
                return False

            await ctx.channel.purge(limit=(amount + 1), check=check)
            return await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Cleared **{}** messages from **{}**'.format(passed, member),
                colour=discord.Colour.green()
            ))

        try:
            role = await self.r_conv.convert(ctx, _filter)
        except commands.errors.RoleNotFound:
            role = None
        if role:
            passed = 0

            def check(m):
                global passed
                if role in m.author.roles and m.id != ctx.message.id:
                    passed += 1
                    return True
                return False

            await ctx.channel.purge(limit=(amount + 1), check=check)
            return await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Cleared **{}** messages from the role **{}**.'.format(passed,
                                                                                                                 role),
                colour=discord.Colour.green()
            ))
        try:
            _re = re.compile(_filter, re.I)
        except Exception:
            _re = None

        if _re:
            passed = 0

            def check(m):
                global passed

                if _re.match(m.content) and m.id != ctx.message.id:
                    passed += 1
                    return True
                return False

            await ctx.channel.purge(limit=(amount + 1), check=check)
            return await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Cleared **{}** which matched the expression!'.format(passed),
                colour=discord.Colour.green()
            ))

        await ctx.send(embed=discord.Embed(
            description='<a:nope:787764352387776523> Filter provided was incorrect!',
            colour=discord.Colour.red()
        ))

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="Wasn't Provided."):

        if member.id == ctx.guild.owner.id:
            return await ctx.send('<a:nope:787764352387776523> | You cannot kick the owner!')
        if member.top_role >= ctx.author.top_role:
            return await ctx.send(
                '<a:nope:787764352387776523> | You cannot kick members with the same/higher role then you!')

        try:
            if ctx.channel.permissions_for(member).manage_messages and ctx.author.id != ctx.guild.owner.id:
                return await ctx.send('{} I cannot kick this members as they are a **mod/admin**.'.format(
                    emoji.KAREN_ADDITIONS_ANIMATED['nope']))
            try:
                await member.send(embed=discord.Embed(
                    title='You Have Been Kicked From {}'.format(ctx.guild),
                    description='**{}** Has Kicked You From this server.\n**Reason:**\n```{}```'.format(
                        ctx.author.mention, reason),
                    color=discord.Color.red()
                ).set_thumbnail(url=ctx.author.avatar))
            except discord.errors.HTTPException:
                pass
            await member.kick(reason=reason)
        except discord.errors.Forbidden:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('{} I cannot **Kick** this member due to role hierarchy.'.format(
                emoji.KAREN_ADDITIONS_ANIMATED['nope']))
        await ctx.send(embed=discord.Embed(
            description='{} Successfully kicked **{}**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['pass'], member),
            color=0x008000,
        )
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @cooldown(1, 5, BucketType.user)
    async def ban(self, ctx, member: discord.User, *, reason="Wasn't Provided."):
        local = ctx.guild.get_member(member.id)
        if member.id == ctx.guild.owner.id:
            return await ctx.send('<a:nope:787764352387776523> | You cannot kick the owner!')

        if local:
            if local.top_role >= ctx.author.top_role:
                return await ctx.send(
                    '<a:nope:787764352387776523> | You cannot kick members with the same/higher role then you!')

        try:
            if ctx.channel.permissions_for(member).manage_messages and ctx.author.id != ctx.guild.owner.id:
                return await ctx.send('{} I cannot kick this members as they are a **mod/admin**.'.format(
                    emoji.KAREN_ADDITIONS_ANIMATED['nope']))
            if not local:
                pass
            else:
                await member.send('You have been banned from **{}**.\n**Reason:**\n\n{}'.format(ctx.guild, reason))
        except Exception:
            pass
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=7)
        except discord.errors.Forbidden:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('I cannot **Ban** this member due to role hierarchy.')
        await ctx.send(embed=discord.Embed(
            description='{} Successfully banned **{}**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['pass'], member),
            color=0x008000,
        )
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @cooldown(1, 5, BucketType.user)
    async def unban(self, ctx: commands.Context, member: str, *, reason: typing.Optional[str] = "Wasn't Provided."):
        banned_users = await ctx.guild.bans()
        try:
            id_ = int(member)
            for user in banned_users:
                user_ = user.user
                if user_.id == id_:
                    try:
                        await ctx.guild.unban(user_, reason=reason)
                        return await ctx.send(embed=discord.Embed(
                            description='{} Successfully unbanned **{}**.'.format(
                                emoji.KAREN_ADDITIONS_ANIMATED['pass'], member),
                            color=0x008000,
                        )
                        )
                    except discord.errors.Forbidden:
                        return await ctx.send(
                            "I cannot **Unban** this member. I either don't have **Permission (s)** or due to role hierarchy.")
            if id_ not in [i.id for i in self.bot.users]:
                return await ctx.send(embed=discord.Embed(
                    description="<a:nope:787764352387776523> I couldn't find a user with the ID matching: **{}**.".format(
                        id_),
                    colour=colours.HEX_RED_SHADES[random.choice(list(colours.HEX_RED_SHADES.keys()))]
                ))
            user = [i for i in self.bot.users if i.id == id_]
            return await ctx.send(embed=discord.Embed(
                description="<a:nope:787764352387776523> The user **{}** isn't banned!".format(user[0]),
                colour=colours.HEX_RED_SHADES[random.choice(list(colours.HEX_RED_SHADES.keys()))]
            ))
        except ValueError:
            try:
                member_name, member_disc = member.split('#')
            except ValueError:
                return await ctx.send(
                    embed=discord.Embed(
                        description="<a:nope:787764352387776523> Use the correct format! **e.g. **_-*™#7519",
                        colour=discord.Color.red()
                    )
                )
            for banned_entry in banned_users:
                user = banned_entry.user

                if (user.name, user.discriminator) == (member_name, member_disc):
                    await ctx.guild.unban(user)
                    try:
                        return await ctx.send(embed=discord.Embed(
                            description='{} Successfully unbanned **{}**.'.format(
                                emoji.KAREN_ADDITIONS_ANIMATED['pass'], member),
                            color=0x008000,
                        )
                        )
                    except discord.errors.Forbidden:
                        return await ctx.send('I cannot **Unban** this member due to role hierarchy.')
            user = [i.name + '#' + i.discriminator for i in self.bot.users if i.name == member_name]
            if len(user) == 0:
                return await ctx.send(embed=discord.Embed(
                    description="<a:nope:787764352387776523> I couldn't find the user with the name matching: **{}**".format(
                        member),
                    colour=discord.Color.red()
                ))
            return await ctx.send(embed=discord.Embed(
                description="<a:nope:787764352387776523> The user **{}** isn't banned!".format(user[0]),
                colour=colours.HEX_RED_SHADES[random.choice(list(colours.HEX_RED_SHADES.keys()))]
            ))

    @commands.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @checks.is_guild_owner()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    async def nuke(self, ctx, channels: discord.TextChannel = None):
        channels = channels or ctx.channel

        await ctx.send('Are you sure you want to nuke {}!\nType in `yes`. To proceed'.format(channels.mention))

        def check(m):
            user = ctx.author
            return m.author.id == user.id and m.content.lower() == 'yes'

        position = channels.position

        await self.bot.wait_for('message', check=check)
        await ctx.channel.send('Theres no going back!\n**Are you sure.**')
        await self.bot.wait_for('message', check=check)
        try:
            new = await channels.clone()
            await channels.delete()
            await new.edit(positon=position)
        except discord.errors.Forbidden:
            return await ctx.send('**Nuke Failed. I am missing permissions!**')

        await new.send('https://media1.tenor.com/images/6c485efad8b910e5289fc7968ea1d22f/tenor.gif?itemid=5791468')
        await asyncio.sleep(2)
        await new.send('**Mecha Karen** has nuked this channel!')

    @commands.command(aliases=['nick'])
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def nickname(self, ctx, member: discord.Member, *, new_nickname: str):
        if member == ctx.guild.owner:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You cannot change the owners nickname!',
                colour=discord.Color.red()
            ))
        else:
            try:
                old = member.display_name
                await member.edit(nick=new_nickname[:32])
            except discord.errors.Forbidden:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Cannot change **{}** nickname due to role hierarchy.'.format(
                        member),
                    colour=discord.Color.red()
                ))
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully renamed **{}** to **{}**.'.format(old,
                                                                                                          new_nickname[
                                                                                                          :32]),
                colour=discord.Color.green()
            ))

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 60, BucketType.user)
    async def slowmode(self, ctx, time='0', channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        try:
            time = int(time)
        except ValueError:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Slowmode delay must be a number!',
                colour=discord.Color.red()
            ))
        if time < 0:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Slowmode delay must be a positive number!'
            ))
        if time > 21600:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(
                embed=discord.Embed(
                    description='<a:nope:787764352387776523> Channel can only have a maximum slowmode of **21600** seconds (6 Hours).',
                    colour=discord.Color.red()
                )
            )
        else:
            await channel.edit(slowmode_delay=time)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> The channel {} now has a slowmode delay of **{}** seconds'.format(
                    channel.mention, time),
                colour=discord.Color.green()
            ))

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.bot_has_permissions(manage_channels=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def lock(self, ctx, channel: discord.TextChannel = None, role: discord.Role = None):
        channel = channel or ctx.channel

        role = role or ctx.guild.default_role
        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully locked the channel {}.'.format(channel.mention),
                colour=discord.Color.green()
            ))
        elif channel.overwrites[role].send_messages or channel.overwrites[role].send_messages == None:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = False
            await channel.set_permissions(role, overwrite=overwrites)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully locked the channel {}.'.format(channel.mention),
                colour=discord.Color.green()
            ))
        else:
            overwrites = channel.overwrites[role]
            overwrites.send_messages = True
            await channel.set_permissions(role, overwrite=overwrites)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully unlocked the channel {}.'.format(
                    channel.mention),
                colour=discord.Color.green()
            ))

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_channels=True, manage_roles=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mute(self, ctx, user: discord.Member, time='10s', *, reason: str = None):
        if ctx.channel.permissions_for(user).manage_messages:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> This member is a **mod/admin**, I cannot mute them.',
                colour=discord.Colour.red()
            ))
        try:
            time = time.lower()

            if time[-1].isdigit():
                time += 's'

            if time[-1] not in ['s', 'h', 'd', 'm'] and not time[-2].isnumeric():
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Incorrect time format used! `S | M | H | D`',
                    colour=discord.Colour.red()
                ))
            timex = convert(int(time[:-1]), time[-1])
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Duration must be a number!',
                colour=discord.Colour.red()
            ))

        client = self.bot.client
        table = client['Bot']
        column = table['Mutes']

        _id = column.find_one({'_id': ctx.guild.id})
        if not _id:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You have no mute role setup!',
                colour=discord.Colour.red()
            ))

        async def mute_(member: discord.Member):
            role = discord.utils.get(ctx.guild.roles, id=_id['role'])
            if not role:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Your mute role is no longer traceable - Please update it!',
                    colour=discord.Colour.red()
                ))
            if role in member.roles:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> This member is already muted!',
                    colour=discord.Colour.red()
                ).set_footer(text='Cause: Mute-role located in roles'))

            await member.add_roles(role, reason=reason or f'{ctx.author} Has muted you - No reason provided.')

            try:
                embed = discord.Embed(
                    title='You Have Been Muted in {}'.format(ctx.guild.name),
                    colour=discord.Colour.red(),
                    description=reason,
                    url=ctx.message.jump_url,
                    timestamp=ctx.message.created_at,
                ).set_author(name=ctx.author, icon_url=ctx.author.avatar)
                embed.set_footer(text=f'User ID: {ctx.author.id} | Message ID: {ctx.message.id}')

                await member.send(embed=embed)
            except Exception:
                pass

            await asyncio.sleep(timex)
            try:
                await member.remove_roles(role, reason='Mute Duration Expired')
                try:
                    await member.send(embed=discord.Embed(
                        description='🔉 | Your mute has expired in {}, you can now speak again'.format(ctx.guild.name),
                        colour=discord.Colour.green()
                    ))
                except discord.errors.Forbidden:
                    pass
            except Exception:
                await ctx.send(f'Failed to remove {member.mention}\'s mute!')
            return True

        task = self.bot.loop.create_task(mute_(user))
        await asyncio.sleep(1)
        if task.done():
            if type(task.result()) != bool:
                return

        self.cache.cache['Mute-Tasks'].update({f'{ctx.guild.id}/{user.id}': task})

        if time[-1].lower() == 'm':
            form = 'Minutes'
        elif time[-1].lower() == 'h':
            form = 'Hours',
        elif time[-1].lower() == 'd':
            form = 'Days'
        else:
            form = 'Seconds'
        await ctx.send(
            embed=discord.Embed(
                description='{} Successfully muted **{}** for **{}** {}.'.format('<a:Passed:757652583392215201>', user,
                                                                                 time[:-1], form),
                colour=discord.Color.green()
            )
        )

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def unmute(self, ctx, user: discord.Member, *, reason: str = None):

        if user.id == ctx.guild.owner.id:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You cannot mute the owner!',
                colour=discord.Colour.red()
            ))
        if user.top_role >= ctx.author.top_role:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You cannot unmute users with the same/higher role then you!',
                colour=discord.Colour.red()
            ))

        client = self.bot.client
        table = client['Bot']
        column = table['Mutes']

        collection = column.find_one({'_id': ctx.guild.id})
        if not collection:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You have no mute role setup!',
                colour=discord.Colour.red()
            ))
        role = discord.utils.get(ctx.guild.roles, id=collection['role'])
        if not role:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Your mute role is no longer traceable - Please update it!',
                colour=discord.Colour.red()
            ))
        if role not in user.roles:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> {} Is not muted!'.format(user),
                colour=discord.Colour.red()
            ))
        await user.remove_roles(role, reason=(reason or '{} Has unmuted this member'.format(ctx.author)))

        task = self.cache.cache['Mute-Tasks'].get(f'{ctx.guild.id}/{user.id}')
        if task:
            task.cancel()
            self.cache.cache['Mute-Tasks'].pop(f'{ctx.guild.id}/{user.id}')

        try:
            embed = discord.Embed(
                title='You\'ve Been Unmuted In {}'.format(ctx.guild),
                description='{}'.format(reason or 'No Reason Provided'),
                colour=discord.Colour.green(),
                url=ctx.message.jump_url,
                timestamp=ctx.message.created_at
            ).set_author(name=ctx.author, icon_url=ctx.author.avatar)
            embed.set_footer(
                text=f'User ID: {ctx.author.id} | Message ID: {ctx.message.id}'
            )
            await user.send(embed=embed)
        except discord.errors.Forbidden:
            pass

        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Unmuted **{}**.'.format(user),
            colour=discord.Color.green()
        ))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True, embed_links=True)
    async def asciify(self, ctx, member: discord.Member, *, reason: str = 'Nickname Not Mentionable') -> discord.Embed:
        current_name = member.display_name
        normalize = await self.bot.loop.run_in_executor(None, unicodedata.normalize, 'NFKD', current_name)
        new_name = normalize.encode('ascii', errors='ignore').decode('ascii')

        if new_name == current_name:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> | **{}**\'s name is already in ASCII format'.format(member),
                colour=discord.Colour.red()
            ))

        try:
            await member.edit(nick=new_name or 'Moderated Nickname', reason=reason)
        except Exception:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> | I cannot change {}\'s Nickname due to role hierachy'.format(
                    member.mention),
                colour=discord.Colour.red()
            ), content=f'The nickname would have been changed to **{new_name}**.')
        return await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> | Changed {}\'s Nickname from **{}** to **{}**.'.format(
                member.mention, current_name, new_name),
            colour=discord.Colour.green()
        ))

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(attach_files=True, read_message_history=True)
    async def archive(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        await ctx.send('Archiving your messages now! This may take a while.')
        messages = []
        async for message in channel.history(limit=2147483646):
            if message.content:
                messages.append(
                    ('**' + str(message.author) + '**' + ' -> ' + message.content).encode('utf-8', errors='ignore'))
        with io.BytesIO() as buffer:
            buffer.write('\n\n'.join([i.decode('utf-8', errors='ignore') for i in messages]))
            buffer.seek(0)
            await ctx.message.reply(content='I have archived your channels messages for you!',
                                    file=discord.File(fp=buffer, filename='archived.md'))

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def warn(self, ctx, user: discord.Member, *, reason: str = 'Not provided.'):
        if user.top_role > ctx.author.top_role and not ctx.author == ctx.guild.owner:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn members with a higher role then you!',
                colour=discord.Colour.red()
            ), mention_author=False)

        if user.bot:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn bots!',
                colour=discord.Colour.red()
            ), mention_author=False)

        if user == ctx.author:
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Cannot warn yourself!',
                colour=discord.Colour.red()
            ), mention_author=False)

        table = self.client['Bot']
        column = table['Warns']

        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})
        if not warns:
            column.insert_one({'_id': f'{ctx.guild.id}/{user.id}', 'warnings': []})
        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})
        warn_data = {
            'warned_at': datetime.datetime.utcnow().strftime('%d/%m/%Y - %I:%M %p'),
            'moderator': f'{ctx.author} ({ctx.author.id})',
            'reason': reason
        }

        warns['warnings'].append(warn_data)
        column.update_one({'_id': f'{ctx.guild.id}/{user.id}'}, {'$set': {'warnings': warns['warnings']}})

        await ctx.message.reply(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Logged warning for **{}**'.format(user),
            colour=discord.Colour.green()
        ), mention_author=False)
        self.bot.dispatch('member_warn', ctx.author, user,
                          {'reason': reason, 'id': (warns['warnings'].index(warn_data) + 1)}, ctx.message)

    @commands.command(aliases=['warns'])
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def warnings(self, ctx, user: discord.Member, page: str = '1'):
        try:
            page = int(page)
        except Exception:
            return await ctx.send('Page number must be a number!')

        table = self.client['Bot']
        column = table['Warns']

        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})

        if not warns:
            return await ctx.send(embed=discord.Embed(
                description="<a:nope:787764352387776523> **{}** doesn't have any warns".format(user),
                colour=discord.Colour.red()
            ), mention_author=False)

        warns_ = len(warns['warnings'])
        page = page * 10

        warns['warnings'] = warns['warnings'][(page - 10):page]

        embed = discord.Embed(
            colour=discord.Colour.red(),
            title='📖 Logs ({}):'.format(warns_),
            timestamp=datetime.datetime.utcnow()).set_footer(
            text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar)
        embed.set_author(icon_url=user.avatar, name=user)

        for i in range(warns_):
            reason = warns['warnings'][i]['reason']
            mod = warns['warnings'][i]['moderator']
            time = warns['warnings'][i]['warned_at']
            embed.add_field(
                name='#{} | Warn | {}'.format((i + 1), time),
                value='Responsible Mod: {}\nReason: {}'.format(mod, reason), inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def delwarn(self, ctx, user: discord.Member, warn: str, *, reason: str = 'Wasn\'t Provided'):
        try:
            warn = int(warn)
        except ValueError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Number provided must be a number not letters!',
                colour=discord.Colour.red()
            ))

        table = self.client['Bot']
        column = table['Warns']
        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})

        if not warns:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> **{}** doesnt have any warns!'.format(user),
                colour=discord.Colour.red()
            ))
        try:
            data = warns['warnings'].pop(warn - 1)
        except IndexError:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Warn number not found!',
                colour=discord.Colour.red()
            ))
        if len(warns['warnings']) == 0:
            column.delete_one({'_id': f'{ctx.guild.id}/{user.id}'})
        else:
            column.update_one({'_id': f'{ctx.guild.id}/{user.id}'}, {'$set': {'warnings': warns['warnings']}})
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.green(),
            description='<a:Passed:757652583392215201> Removed warn #{} for **{}**'.format(warn, user)
        ))
        data['mod_reason'] = reason
        data['id'] = warn
        self.bot.dispatch('warn_remove', ctx.author, user, data, ctx.message)

    @commands.command(aliases=['cw', 'clearwarns'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.has_guild_permissions(manage_messages=True)
    async def clear_warns(self, ctx, user: discord.Member, *, reason: str = 'Wasn\'t Provided') -> discord.Embed:
        table = self.client['Bot']
        column = table['Warns']
        warns = column.find_one({'_id': f'{ctx.guild.id}/{user.id}'})

        if not warns:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> **{}** doesnt have any warns!'.format(user),
                colour=discord.Colour.red()
            ))
        column.delete_one({'_id': f'{ctx.guild.id}/{user.id}'})
        await ctx.send(embed=discord.Embed(
            colour=discord.Colour.green(),
            description='<a:Passed:757652583392215201> Cleared warns for **{}**'.format(user)
        ))
        self.bot.dispatch('warn_clear', ctx.author, user, {'bulk': len(warns['warnings']), 'reason': reason},
                          ctx.message)


def setup(bot):
    bot.add_cog(moderation(bot))
