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

import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
import asyncio
from Helpers import functions
from Helpers import emoji
from Helpers import colours
import random

from Others import *

def convert(time: int, unit):
    unit = unit.lower()
    if unit == 's':
        return time
    elif unit == 'm':
        return time*60
    elif unit == 'h':
        return (time*60)*60
    elif unit == 'd':
        return ((time*60)*60)*24

'''
Added alot more error handling

More nicer unban commands

Soon to come logging!
'''
    
class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['purge'])
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_messages=True)
    @cooldown(1, 5, BucketType.user)
    async def clear(self, ctx, amount='5', member: discord.Member = None) -> discord.Embed:
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
        try:
            if member == None:
                await ctx.channel.purge(limit=amount)
                return await ctx.send(embed=discord.Embed(
                    description='<a:Passed:757652583392215201> Successfully clear **{}** messages from {}.'.format(amount, ctx.channel.mention),
                    colour=discord.Colour.red()
                ))
            else:
                def check(m):
                    return m.author == member
                await ctx.channel.purge(limit=amount, check=check)
                return await ctx.send(embed=discord.Embed(
                    description='<a:Passed:757652583392215201> Cleared any messages from **{}** in the last **{}** messages.'.format(amount, member),
                    colour=discord.Colour.red()
                ))
        except discord.errors.Forbidden:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> I do not Have the Permissions to complete this action!',
                colour=discord.Colour.red()
            ))

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member = None, *, reason='Wasn\'t Provided.') -> discord.Embed:
        ## Added the \ for the reason
        if member == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('Please provide a member.')
        try:
            if ctx.channel.permissions_for(member).kick_members and ctx.author != ctx.guild.owner:
                return await ctx.send('{} I cannot kick this members as they are a **mod/admin**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['nope']))
            try:
                await member.send(embed=discord.Embed(
                    title='You Have Been Kicked From {}'.format(ctx.guild),
                    description='**{}** Has Kicked You From this server.\n**Reason:**\n```{}```'.format(ctx.author.mention, reason),
                    color=discord.Color.red()
                ).set_thumbnail(url=ctx.author.avatar_url))
            except discord.errors.HTTPException:
                pass
            await member.kick(reason=reason)
        except discord.errors.Forbidden:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('{} I cannot **Kick** this member due to role hierarchy.'.format(emoji.KAREN_ADDITIONS_ANIMATED['nope']))
        await ctx.send(embed=discord.Embed(
            description='{} Successfully kicked **{}**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['pass'],member),
            color=0x008000,
            )
        )

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @cooldown(1, 5, BucketType.user)
    async def ban(self, ctx, member: discord.User = None, *, reason="Wasn't Provided.") -> discord.Embed:
        ## Ban system works cross guild
        ## So u can ban a person whos not in your server
        ## As long as the bot has access to the user
        if member == None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send('Please provide a member.')
            return
        try:
            if ctx.channel.permissions_for(member).kick_members and ctx.author != ctx.guild.owner:
                return await ctx.send('{} I cannot ban this members as they are a **mod/admin**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['nope']))
            if str(ctx.guild.get_member(member.id)) == 'None':
                pass
            else:
                await member.send('You have been banned from **{}**.\n**Reason:**\n\n{}'.format(ctx.guild, reason))
        except Exception:
            pass
        try:
            await ctx.guild.ban(member, reason=reason, delete_message_days=7)
            ## Delete after has become a week
            ## we dont want to see the banned scums messages
        except discord.errors.Forbidden:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('I cannot **Ban** this member due to role hierarchy.')
        ## Role hierachy prevents the bot from banning a user with a higher role
        ## Quick little addition
        await ctx.send(embed=discord.Embed(
            description='{} Successfully banned **{}**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['pass'],member),
            color=0x008000))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_guild_permissions(ban_members=True, embed_links=True)
    @cooldown(1, 5, BucketType.user)
    async def unban(self, ctx, member=None, *, reason="Wasn't Provided."):
        if member == None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send('Who would you like unbanned?\nNext time provide a user.')
        banned_users = await ctx.guild.bans()
        try:
            id_ = int(member)
            for user in banned_users:
                user_ = user.user
                if user_.id == id_:
                    try:
                        await ctx.guild.unban(user_, reason=reason)
                        return await ctx.send(embed=discord.Embed(
                            description='{} Successfully unbanned **{}**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['pass'],member),
                            color=0x008000))
                    except discord.errors.Forbidden:
                        return await ctx.send("I cannot **Unban** this member. I either don't have **Permission (s)** or due to role hierarchy.")
            if id_ not in [i.id for i in self.bot.users]:
                return await ctx.send(embed=discord.Embed(
                    description="<a:nope:787764352387776523> I couldn't find a user with the ID matching: **{}**.".format(id_),
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
                        colour=discord.Color.red()))
            for banned_entry in banned_users:
                user = banned_entry.user
    
                if (user.name, user.discriminator) == (member_name, member_disc):
                    await ctx.guild.unban(user)
                    try:
                        return await ctx.send(embed=discord.Embed(
                            description='{} Successfully unbanned **{}**.'.format(emoji.KAREN_ADDITIONS_ANIMATED['pass'],member),
                            color=0x008000))
                    except discord.errors.Forbidden:
                        return await ctx.send('I cannot **Unban** this member due to role hierarchy.')
            user = [i.name+'#'+i.discriminator for i in self.bot.users if i.name == member_name]
            ## this will give us a cleaner look with the ID
            ## so we dont see 2424537658 like dyno
            ## we see fish#1234
            ## Much more nicer
            if len(user) == 0:
                return await ctx.send(embed=discord.Embed(
                    description="<a:nope:787764352387776523> I couldn't find the user with the name matching: **{}**".format(member),
                    colour=discord.Color.red()
                ))
            await ctx.send(embed=discord.Embed(
                description="<a:nope:787764352387776523> The user **{}** isn't banned!".format(user[0]),
                colour=colours.HEX_RED_SHADES[random.choice(list(colours.HEX_RED_SHADES.keys()))]
            ))  ## If the user is found
            ## but there not banned
            ## we see this
            ## Very much user friendly

    @commands.command()
    @commands.bot_has_guild_permissions(manage_channels=True)
    @functions.is_guild_owner()
    @cooldown(1, 300, BucketType.user)
    async def nuke(self, ctx, channels: discord.TextChannel = None):
        if channels == None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send('Give a channel')
            return
        else:
            await ctx.send('Are you sure!')
            await ctx.send('Type in `yes`. To proceed')

            def check(m):   ## Message object
                return m.author.id == ctx.author.id and m.content.lower() == 'yes'

            await self.bot.wait_for('message', check=check)
            await ctx.channel.send('Theres no going back!\n**Are you sure.**')
            await self.bot.wait_for('message', check=check)
            try:
                new = await channels.clone()
                await channels.delete()
            except discord.errors.Forbidden:
                return await ctx.send('**Nuke Failed. I am missing permissions!**')
            await new.send('https://media1.tenor.com/images/6c485efad8b910e5289fc7968ea1d22f/tenor.gif?itemid=5791468')
            await asyncio.sleep(1)  ## Reduced cooldown, all we wanna see is boom boom.
            await new.send('**Mecha Karen** has nuked this channel!')
                
    @commands.command(aliases=['nick'])
    @commands.has_guild_permissions(manage_nicknames=True)
    @commands.bot_has_guild_permissions(manage_nicknames=True)
    async def nickname(self, ctx, member: discord.Member = None, *args):
        if member == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Give a member. **-nickname <MEMBER> <NICKNAME>**',
                colour=discord.Color.red()
            ))
        '''
        Alot more error handling
        
        And also much more nicer error handling
        '''
        elif member == ctx.guild.owner:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You cannot change the owners nickname!',
                colour=discord.Color.red()
            ))
        else:
            if len(args) == 0:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Need to give a new nickname!',
                    colour=discord.Color.red()
                ))
            old = member.display_name
            x = ' '.join(map(str, args))
            if x == old:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> New nickname needs to be different to the old nickname',
                    colour=discord.Color.red()
                ))
            try:
                await member.edit(nick=f'{x}')
            except discord.errors.Forbidden:
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Cannot change **{}** nickname due to role hierarchy.'.format(member),
                    colour=discord.Color.red()
                ))
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully renamed **{}** to **{}**.'.format(old, x),
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
                description='<a:Passed:757652583392215201> The channel {} now has a slowmode delay of **{}** seconds'.format(channel.mention, time),
                colour=discord.Color.green()
            ))

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
                ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully locked the channel {}.'.format(channel.mention),
                colour=discord.Color.green()
            ))
        elif channel.overwrites[ctx.guild.default_role].send_messages or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully locked the channel {}.'.format(channel.mention),
                colour=discord.Color.green()
            ))
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Successfully unlocked the channel {}.'.format(channel.mention),
                colour=discord.Color.green()
            ))

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @commands.bot_has_guild_permissions(manage_channels=True, manage_roles=True)
    async def mute(self, ctx, user: discord.Member = None, time='10s'):
        if user == None:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Need to provide a member! -Mute <MEMBER> <TIME>',
                colour=discord.Colour.red()
            ))
        if ctx.channel.permissions_for(user).manage_messages:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> This member is a **mod/admin**, I cannot mute them.',
                colour=discord.Colour.red()
            ))
        try:
            time = time.lower()
            if time[-1] not in ['s', 'h', 'd', 'm'] and not time[-2].isnumeric():
                return await ctx.send(embed=discord.Embed(
                    description='<a:nope:787764352387776523> Incorrect time format used! `S | M | H | D`',
                    colour=discord.Colour.red()
                ))
            timex = convert(int(time[:-1]), time[-1])
        except ValueError:
            return await ctx.send('Duration must be a number!')

        async def mute_(member: discord.Member):
            role = discord.utils.get(ctx.guild.roles, name='Muted')
            if not role:
                role = await ctx.guild.create_role(
                    name='Muted',
                    reason='Mute Role has been set automatically!',
                    permissions=discord.Permissions(
                        send_messages=False,
                        add_reactions=False,
                        view_channel=True,
                        change_nickname=False,
                        connect=False
                    )
                )
            await member.add_roles(role)
            for channel in ctx.guild.text_channels:
                overwrites = channel.overwrites
                if member not in overwrites:
                    overwrites[user] = discord.PermissionOverwrite(
                        send_messages=False,
                        add_reactions=False,
                        view_channel=True,
                        change_nickname=False,
                        connect=False
                    )
                    await channel.edit(overwrites=overwrites)
            await asyncio.sleep(timex)
            try:
                await member.remove_roles(role)
            except AttributeError:
                pass
        self.bot.loop.create_task(mute_(user))
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
                description='{} Successfully muted **{}** for **{}** {}.'.format('<a:Passed:757652583392215201>', user, time, form),
                colour=discord.Color.green()
            )
        )

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.bot_has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 10, BucketType.user)
    async def unmute(self, ctx, user: discord.Member = None):
        if user == None:
            return await ctx.send('Provide a user to be unmuted!')
        if user == ctx.guild.owner:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> The Server Owner can Never be Muted.',
                colour=discord.Color.red()
            ))
        for channel in ctx.guild.text_channels:
            overwrites = channel.overwrites
            if user in overwrites:
                del overwrites[user]
                await channel.edit(overwrites=overwrites)
            else:
                ctx.command.reset_cooldown(ctx)
                return await ctx.send(embed=discord.Embed(
                    description="<a:nope:787764352387776523> This user **{}** isn't muted!".format(user),
                    color=discord.Color.red()
                ))
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Successfully unmuted the user **{}**.'.format(user),
            colour=discord.Color.green()
        ))

def setup(bot):
    bot.add_cog(moderation(bot))
