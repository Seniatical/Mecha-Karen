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

import datetime
import typing
import asyncio
import discord
from discord.ext import commands


class logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client
        self.logs = {}

        self.bot.loop.create_task(self.update_logs())

    async def update_logs(self):
        client = self.client
        table = client['Bot']
        logs_ = table['Logging']

        while True:
            self.logs.clear()

            for collection in logs_.find():
                self.logs.update({collection['_id']: collection['channel']})
            await asyncio.sleep(20)

    @staticmethod
    async def get_audit_log_entry(guild: discord.Guild, action: discord.AuditLogAction,
                                  target: discord.abc.Snowflake) -> typing.Optional[discord.AuditLogEntry]:
        try:
            entry = await guild.audit_logs(action=action).find(lambda _entry: _entry.target.id == target.id)
        except discord.errors.Forbidden:
            return None
        return entry

    @staticmethod
    async def format_time(time: datetime.datetime) -> str:
        days = (datetime.datetime.now(time.tzinfo) - time).days
        years, months = 0, 0

        string = ''

        if days >= 365:
            years, days = divmod(days, 365)

            if days >= 30:
                months, days = divmod(days, 30)

            if years == 1 and months > 1:
                string += f'1 Year and {months} Months'
            elif years > 1 and months > 1:
                string += f'{years} Year and {months} Months'
            elif years > 1 and not months and days > 1:
                string += f'{years} Years and {days} Days'

        elif days >= 30:
            months, days = divmod(days, 30)

            if months > 1 and days > 1:
                string += f'{months} Months and {days} Days'
            elif months > 1 and days == 1:
                string += f'{months} Months and 1 Day'
            elif months == 1 and days > 1:
                string += f'1 Month and {days} Days'

        else:
            if days > 1:
                string += f'{days} Days and {time.hour} Hours'
            else:
                string += f'{time.hour} Hour(s), {time.minute} Minute(s) and {time.second} Second(s)'

        return string

    @commands.command()
    @commands.cooldown(1, 60, commands.BucketType.guild)
    @commands.has_guild_permissions(manage_guild=True)
    async def logs(self, ctx, action: str, channel: discord.TextChannel = None):
        if action.lower() not in ['set', 'remove', 'add', 'delete', 'view']:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Action must be either `SET` or `REMOVE`',
                colour=discord.Colour.red()
            ), mention_author=False)

        table = self.client['Bot']
        column = table['Logging']
        current = column.find_one({'_id': ctx.guild.id})

        if action.lower() in ['set', 'add']:
            if not channel:
                return await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Give the channel to set the logs for!',
                    colour=discord.Colour.red()
                ), mention_author=False)
            if not current:
                column.insert_one({'_id': ctx.guild.id, 'channel': channel.id})
            elif current['channel'] == channel.id:
                return await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Channel {} is already in use for logs'.format(
                        channel.mention),
                    colour=discord.Colour.red()
                ), mention_author=False)
            else:
                column.update_one({'_id': ctx.guild.id}, {'$set': {'channel': channel.id}})
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Logs set for {}'.format(channel.mention),
                colour=discord.Colour.green()
            ), mention_author=False)

        elif action.lower() == 'view':
            check = column.find_one({'_id': ctx.guild.id})
            channel = self.bot.get_channel(check['channel'])
            if not check or not channel:
                return await ctx.send('Logs haven\t been setup for this server.')
            await ctx.send('Current logs channel is {}.'.format(channel.mention))

        else:
            if not current:
                return await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Logs aren\'t setup for this server!',
                    colour=discord.Colour.red()
                ), mention_author=False)
            column.delete_one({'_id': ctx.guild.id})
            await ctx.message.reply(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Logged has been disabled!'.format(channel.mention),
                colour=discord.Colour.green()
            ), mention_author=False)
        await self.update_logs()

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        embed = discord.Embed(
            colour=message.author.color,
            timestamp=datetime.datetime.utcnow(),
            description='**Message Deleted in channel {}**\n'.format(message.channel.mention)
        ).set_author(
            name=message.author,
            icon_url=message.author.avatar)

        try:
            channel = self.bot.get_channel(self.logs[message.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return

        if message.channel.id == channel.id:
            return

        ctx = await self.bot.get_context(message)
        perms = channel.permissions_for(ctx.me)
        if not perms.send_messages or not perms.embed_links or not perms.attach_files:
            return

        if message.attachments:
            attachment = message.attachments[0]
            try:
                file_ = await attachment.to_file()
                await channel.send(
                    content=f'File deleted by user {message.author.mention}, in channel {message.channel.mention}.',
                    file=file_)
            except Exception:
                pass

        if message.content:
            content = message.content
            if len(content) > 500:
                content = content[:497] + '...'

            embed.description += content

        embed.set_footer(text=f'User ID: {message.author.id} | Message ID: {message.id}')

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, b_message, a_message):
        try:
            channel = self.bot.get_channel(self.logs[a_message.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel or b_message.author.bot:
            return

        ctx = await self.bot.get_context(a_message)
        perms = channel.permissions_for(ctx.me)
        if not perms.send_messages or not perms.embed_links or not perms.attach_files:
            return

        embed = discord.Embed(colour=a_message.author.colour, timestamp=b_message.created_at,
                              description=f'**[Jump URL]({a_message.jump_url})**').set_footer(
            text=f'ID: {b_message.author.id} | Message ID: {b_message.id}')
        embed.set_author(name=a_message.author, icon_url=a_message.author.avatar)

        if b_message.attachments and not a_message.attachments:
            file_ = await b_message.attachments[0].to_file()

            await channel.send(content='File edited in {a_message.channel.mention} by {a_message.author}.', file=file_)

        if b_message.content == a_message.content and not b_message.embeds and a_message.embeds:
            return

        if b_message.content and a_message.content:
            b_content = b_message.content

            if len(b_content) > 59:
                b_content = b_content[:55] + '....'

            a_content = a_message.content

            if len(a_content) > 59:
                a_content = a_content[:55] + '....'

            embed.add_field(name='Before', value=b_content)
            embed.add_field(name='After:', value=a_content, inline=False)
            return await channel.send(embed=embed)
        else:
            await channel.send(
                embed=discord.Embed(description=f'[Message]({a_message.jump_url}) Edited in {channel.mention}',
                                    colour=discord.Colour.blue()).set_footer(
                    text=f'User ID: {b_message.author.id} | Message ID: {b_message.id}'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            colour=discord.Colour.green(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar)

        embed.set_footer(text=f'User ID: {member.id}')
        embed.add_field(name=f'{member} Joined',
                        value=f'**Account Created:** {member.created_at.strftime("%a, %#d, %B %Y, %I:%M %p UTC")}\n{await self.format_time(member.created_at)}')

        try:
            channel = self.bot.get_channel(self.logs[member.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar)

        embed.set_footer(text=f'User ID: {member.id}')
        embed.add_field(name=f'{member} Left',
                        value=f'**Joined On:** {member.joined_at.strftime("%a, %#d, %B %Y, %I:%M %p UTC")}\n{await self.format_time(member.joined_at)}')

        try:
            channel = self.bot.get_channel(self.logs[member.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_edit(self, b_member: discord.Member, a_member: discord.Member):
        try:
            channel = self.bot.get_channel(self.logs[a_member.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return

        if b_member.nick != a_member.nick:
            embed = discord.Embed(
                colour=discord.Colour.blue(),
                timestamp=datetime.datetime.utcnow(),
                title='Nickname Updated')
            embed.set_author(name=a_member, icon_url=member.avatar)
            embed.set_footer(text=f'User ID: {a_member.id}')

            embed.add_field(name='Before', value=b_member.nick)
            embed.add_field(name='After', value=a_member.nick, inline=False)

            return await channel.send(embed=embed)

        elif b_member.roles != a_member.roles:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title='Member Roles Updated',
                timestamp=datetime.datetime.utcnow()
            )
            _old = b_member.roles
            _new = b_member.roles
            _changed = None
            for role in _new:
                if role not in _old:
                    _changed = [role, True]
                    break
            for role in _old:
                if role not in _new:
                    _changed = [role, False]
                    break
            embed.set_author(name=a_member, icon_url=a_member.avatar)
            if _changed[1]:
                embed.add_field(name='Role Added:', value=_changed[0].mention)
            else:
                embed.add_field(name='Role Removed:', value=_changed[0].mention)
            embed.set_footer(text=f'User ID: {a_member.id}')

            return await channel.send(embed=embed)

        elif b_member.pending and not a_member.pending:
            embed = discord.Embed(
                title='Verification',
                colour=discord.Colour.red(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(name=a_member, icon_url=a_member.avatar)
            embed.set_footer(text=f'User ID: {a_member.id}')
            embed.description = f'**{a_member.mention} has successfully been verified.**'

        else:
            return

    @commands.Cog.listener()
    async def on_invite_create(self, invite):

        try:
            channel = self.bot.get_channel(self.logs[invite.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=invite.inviter,
            icon_url=invite.inviter.avatar)

        embed.add_field(name=f'Invite Created', value=f'Code: {invite}')

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):

        try:
            channel = self.bot.get_channel(self.logs[channel.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        channel_audit_log_entry = await self.get_audit_log_entry(channel.guild, discord.AuditLogAction.channel_create,
                                                                 channel)

        if not channel_audit_log_entry:
            return

        member = channel_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar)

        embed.add_field(name=f'Channel Created', value=f'Channel: {channel.mention}')
        embed.set_footer(text=f'User ID: {member.id} | Channel ID: {channel.id}')

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):

        try:
            channel = self.bot.get_channel(self.logs[channel.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        channel_audit_log_entry = await self.get_audit_log_entry(channel.guild, discord.AuditLogAction.channel_delete,
                                                                 channel)

        if not channel_audit_log_entry:
            return

        member = channel_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar)

        embed.add_field(name=f'Channel Deleted', value=f'Channel: {channel.name}')
        embed.set_footer(text=f'User ID: {member.id} | Channel ID: {channel.id}')

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):

        try:
            channel = self.bot.get_channel(self.logs[role.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        role_audit_log_entry = await self.get_audit_log_entry(role.guild, discord.AuditLogAction.role_create, role)
        if not role_audit_log_entry:
            return

        member = role_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar)

        embed.add_field(name=f'Role Created', value=f'Role: {role.mention}')
        embed.set_footer(text=f'User ID: {member.id} | Role ID: {role.id}')

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        role_audit_log_entry = await self.get_audit_log_entry(role.guild, discord.AuditLogAction.role_delete, role)
        if not role_audit_log_entry:
            return

        member = role_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar)

        embed.add_field(name=f'Role Deleted', value=f'Role: {role}')
        embed.set_footer(text=f'User ID: {member.id} | Role ID: {role.id}')

        try:
            channel = self.bot.get_channel(self.logs[role.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_warn(self, author, member, warn, message):
        try:
            channel = self.bot.get_channel(self.logs[message.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return

        embed = discord.Embed(title=f'{member} Has Been Warned', url=message.jump_url, colour=discord.Colour.blue(),
                              timestamp=message.created_at)
        embed.set_author(name=author, icon_url=author.avatar)
        embed.description = warn['reason']
        embed.set_footer(text=f'Warn ID: #{warn["id"]} | User ID: {member.id}')
        return await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_warn_remove(self, author, member, warn, message):
        try:
            channel = self.bot.get_channel(self.logs[message.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return

        embed = discord.Embed(title=f'Deleted warn for {member}', url=message.jump_url, colour=discord.Colour.blue(),
                              timestamp=message.created_at)
        embed.set_author(name=author, icon_url=author.avatar)
        embed.set_footer(text=f'Warn ID: #{warn["id"]} | User ID: {member.id}')

        embed.description = warn['mod_reason']
        embed.add_field(name='Warn Details',
                        value=f'**Reason:** {warn["reason"]}\n**Time:** {warn["warned_at"]}\n**Moderator:** {warn["moderator"]}')
        return await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_warn_clear(self, author, member, data, message):
        try:
            channel = self.bot.get_channel(self.logs[message.guild.id])
        except (KeyError, AttributeError):
            return

        if not channel:
            return
        embed = discord.Embed(title=f'Warns Cleared For {member}', url=message.jump_url, colour=discord.Colour.blue(),
                              timestamp=message.created_at)
        embed.set_author(name=author, icon_url=author.avatar)
        embed.set_footer(text=f'Warns Cleared: {data["bulk"]} | User ID: {member.id}')
        embed.description = data['reason']
        return await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(logging(bot))
