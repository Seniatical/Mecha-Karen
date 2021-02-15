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

    @commands.Cog.listener()
    async def on_ready(self):
        async def log_loop():
            await self.update_logs()
            await asyncio.sleep(20)
        self.bot.loop.create_task(log_loop())

    async def update_logs(self):
        client = self.client
        table = client['Bot']
        logs_ = table['Logging']

        self.logs.clear()

        for collection in logs_.find():
            self.logs.update({collection['_id']: collection['channel']})
        return True

    async def get_audit_log_entry(self, guild: discord.Guild, action: discord.AuditLogAction, target: discord.abc.Snowflake) -> typing.Optional[discord.AuditLogEntry]:
        try:
            entry = await guild.audit_logs(action=action).find(lambda entry: entry.target.id == target.id)
        except discord.errors.Forbidden:
            return False
        return entry

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
                    description='<a:nope:787764352387776523> Channel {} is already in use for logs'.format(channel.mention),
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
            description='Message Deleted in channel {}'.format(message.channel.mention)
        ).set_author(
            name=message.author,
            icon_url=message.author.avatar_url)

        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

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
            attachment: discord.Attachment = message.attachments[0]
            file_ = await attachment.to_file()
            await channel.send(content=f'File deleted by user {message.author.mention}, in channel {message.channel.mention}.', file=file_)

        if message.content:
            embed.add_field(name='Content:', value=message.content)
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

        embed = discord.Embed(colour=a_message.author.colour, timestamp=b_message.created_at, description=f'[Jump URL]({a_message.jump_url})')
        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)
        embed.set_author(name=a_message.author, icon_url=a_message.author.avatar_url)

        if b_message.attachments and not a_message.attachments:
            file_ = await b_message.attachments[0].to_file()
            return await channel.send(content='File edited in {a_message.channel.mention} by {a_message.author}.', file=file_)

        if b_message.content == a_message.content and not b_message.embeds and a_message.embeds:
            return

        if b_message.content and a_message.content:
            embed.add_field(name='Message Content (Non-Edited):', value=b_message.content)
            embed.add_field(name='Message Content (Edited):', value=a_message.content, inline=False)
            return await channel.send(embed=embed)
        else:
            await channel.send(embed=discord.Embed(description=f'[Message]({a_message.jump_url}) Edited in {channel.mention}'))

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar_url)

        embed.add_field(name = f'{member} joined', value = f'**Account Created:** {member.created_at.strftime("%a, %#d, %B %Y, %I:%M %p UTC")}')

        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

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
            icon_url=member.avatar_url)

        embed.add_field(name = f'{member} left', value = f'**Joined On:** {member.joined_at.strftime("%a, %#d, %B %Y, %I:%M %p UTC")}')
        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

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
                colour=discord.Colour.red(),
                title='Nickname Updated')
            embed.set_author(name=a_member, icon_url=member.avatar_url)
            embed.add_field(name='Before:', value=b_member.nick)
            embed.add_field(name='After:', value=a_member.nick, inline=False)
            embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

        elif b_member.roles != a_member.roles:
            embed = discord.Embed(
                colour=discord.Colour.red(),
                title='Member Roles Updated'
            )
            _old = b_member.roles
            _new = b_member.roles
            _changed = None
            for role in _new:
                if not role in _old:
                    _changed = [role, True]
                    break
            for role in _old:
                if role not in _new:
                    _changed = [role, False]
                    break
            embed.set_author(name=a_member, icon_url=a_member.avatar_url)
            if _changed[1]:
                embed.add_field(name='Role Added:', value=_changed[0].mention)
            else:
                embed.add_field(name='Role Removed:', value=_changed[0].mention)

        elif b_member.pending and not a_member.pending:
            embed = discord.Embed(
                title='Verification',
                colour=discord.Colour.red()
            )
            embed.set_author(name=a_member, icon_url=a_member.avatar_url)
            embed.description = 'Member has successfully been verified.'
        else:
            return
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=invite.inviter,
            icon_url=invite.inviter.avatar_url)

        embed.add_field(name = f'Invite Created', value = f'Code: {invite}')

        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

        try:
            channel = self.bot.get_channel(self.logs[invite.inviter.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        channel_audit_log_entry = await self.get_audit_log_entry(channel.guild, discord.AuditLogAction.channel_create, channel)
        member = channel_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar_url)

        embed.add_field(name = f'Channel Created', value = f'Channel: {channel.mention}')

        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

        try:
            channel = self.bot.get_channel(self.logs[channel.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        channel_audit_log_entry = await self.get_audit_log_entry(channel.guild, discord.AuditLogAction.channel_delete, channel)
        member = channel_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar_url)

        embed.add_field(name = f'Channel Deleted', value = f'Channel: {channel.mention}')

        embed.set_footer(text='Timezone: UTC+0', icon_url=self.bot.user.avatar_url)

        try:
            channel = self.bot.get_channel(self.logs[channel.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        role_audit_log_entry = await self.get_audit_log_entry(role.guild, discord.AuditLogAction.role_create, role)
        member = role_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar_url)

        embed.add_field(name = f'Role Created', value = f'Role: {role.mention}')

        try:
            channel = self.bot.get_channel(self.logs[role.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        role_audit_log_entry = await self.get_audit_log_entry(role.guild, discord.AuditLogAction.role_delete, role)
        member = role_audit_log_entry.user

        embed = discord.Embed(
            colour=discord.Colour.red(),
            timestamp=datetime.datetime.utcnow()
        ).set_author(
            name=member,
            icon_url=member.avatar_url)

        embed.add_field(name = f'Role Deleted', value = f'Role: {role}')

        try:
            channel = self.bot.get_channel(self.logs[role.guild.id])
        except (KeyError, AttributeError):
            return
        if not channel:
            return

        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(logging(bot))
