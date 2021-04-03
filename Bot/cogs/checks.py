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
import datetime
import time
import sys
import asyncio
import math, json, version
import os
from Utils import db, parser

def convert_size(bytes):
    if bytes == 0:
        return "0B"
    size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
    i = int(math.floor(math.log(bytes, 1024)))
    p = math.pow(1024, i)
    s = round(bytes / p, 2)
    return "%s %s" % (s, size_name[i])

class checks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.image_types = ['PNG', 'JPG', 'WEBP', 'GIF']

    @commands.command(aliases=['info', 'whois', 'Userinfo'])
    @cooldown(1, 10, BucketType.user)
    async def user(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        if member.premium_since:
            name = str(member) + ' | (💎 Booster)'
        else:
            name = member
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        flag = ' | '.join(list(flags(member).values()))
        if len(flag) == 0:
            flag = 'This user has no badges!'
        embed.add_field(name='Public Badges ({})'.format(len(list(flags(member).values()))), value="{}".format(flag), inline=False)
        embed.set_author(name=f"{name}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %b %Y, %I:%M %p"))
        embed.add_field(name='Registered at:', value=member.created_at.strftime('%a, %#d %b %Y, %I:%M %p'))
        if len(member.roles) == 1:
            embed.add_field(name='Roles (0):', value='There are no roles for this user.', inline=False)
        else:
            embed.add_field(name=f"Roles ({len(member.roles)-1})", value=" ".join([role.mention for role in member.roles if not role == ctx.guild.default_role]), inline=False)
        embed.add_field(name='Join Position:', value=sum(m.joined_at < member.joined_at for m in ctx.guild.members if m.joined_at is not None))
        web = member.web_status
        app = member.desktop_status,
        mob = member.mobile_status
        default = '<:offline:787764149706031104> Offline'
        status = parser.nano('STATUS', member)
        embed.add_field(name='Discord Client:', value=status or default)
        if not member.activity:
            pass
        else:
            embed.add_field(name='Activity:', value=str(member.activity.type).split('.')[-1].title() if not member.activity.type == discord.ActivityType.custom else member.activity, inline=False)
            embed.set_thumbnail(url=member.avatar_url)
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'ID: {member.id}\nPrompted by  {ctx.author.name}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['avatar'])
    @cooldown(1, 10, BucketType.user)
    async def av(self, ctx, member: discord.Member = None):
        member = member or ctx.author
        embed = discord.Embed(title=f"{member}'s avatar",color=member.color, timestamp=datetime.datetime.utcnow())
        if not member.is_avatar_animated():
            types = self.image_types[:-1]
        else:
            types = self.image_types
        modes = []
        for type in types:
            modes.append([type, str(member.avatar_url_as(static_format=type.lower(), size=512))])
        
        embed.description = ' | '.join(['[%s](%s)' % (i[0], i[1]) for i in modes])
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, BucketType.guild)
    async def server(self, ctx):
        try:
            embed = discord.Embed(
                title=f'{ctx.guild.name}',
                color=discord.Color.red(),
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_thumbnail(url=ctx.guild.icon_url)
            embed.add_field(name='Owner?', value=f'{ctx.guild.owner}')
            embed.add_field(name='Owner ID?', value=f'`{ctx.guild.owner.id}`')
            embed.add_field(name='Owner Created at?', value=f"{ctx.guild.owner.created_at.strftime('%a, %#d %B %Y, %I:%M %p')}", inline=False)
            embed.add_field(name='Server Name?', value=f'{ctx.guild.name}')
            embed.add_field(name='Server ID?', value=f'`{ctx.guild.id}`')
            embed.add_field(name='Region?', value=f'{ctx.guild.region[0].title()}')
            embed.add_field(name=f'Created at?', value=f"{ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p')}", inline=False)
            embed.add_field(name="Emoji's?", value=f'{len(ctx.guild.emojis)}')
            embed.add_field(name=f'Members?', value=f'{len(ctx.guild.members)}')
            embed.add_field(name=f'Verification Level?', value=f'{ctx.guild.verification_level[0].title()}')
            true = ctx.guild.mfa_level
            if true == 1:
                true = 'Yes!'
            else:
                true = 'No!'
            embed.add_field(name='Admin 2FA?', value=f'{true}')
            boost = ctx.guild.premium_subscription_count
            if boost == 0:
                boost = 'None 😭'
            embed.add_field(name='Boosts!', value=f'{boost}')
            level = ctx.guild.premium_tier
            if level == 0:
                count = 2 - ctx.guild.premium_subscription_count
                level = 'Level 0. You need {} more boosts for level 1!'.format(count)
            elif level == 1:
                count = 15 - ctx.guild.premium_subscription_count
                level = 'Level 1. You need {} more boosts for level 2'.format(count)
            elif level == 2:
                count = 30 - ctx.guild.premium_subscription_count
                level = 'Level 2. You need {} more boosts for level 3'.format(count)
            elif level == 3:
                count = ctx.guild.premium_subscription_count
                level = 'Level 3. Max level with a whopping {} boosts!!!'.format(count)
            embed.add_field(name='Channels?', value=f'{len(ctx.guild.channels)}')
            bots = len([i for i in ctx.guild.members if i.bot])
            embed.add_field(name=f'Bots?', value=f'{bots}')
            embed.add_field(name=f'Main Lang?', value=f'{ctx.guild.preferred_locale}')
            embed.add_field(name=f'Emoji Limit?', value=f'{ctx.guild.emoji_limit}')
            embed.add_field(name=f'Bitrate Limit?', value=f'{convert_size(ctx.guild.bitrate_limit)}')
            embed.add_field(name='Filesize Limit?', value=f'{convert_size(ctx.guild.filesize_limit)}')
            embed.add_field(name='Large?', value=f'{ctx.guild.large}')
            embed.add_field(name='Server Level!', value=f'{level}', inline=False)
            embed.set_footer(text=f'Prompted by {ctx.author}', icon_url=ctx.author.avatar_url)
            msg = await ctx.send(embed=embed)
            def reaction_check(m):
                user = ctx.author
                if m.message_id == msg.id and m.user_id == user.id and str(m.emoji) == "▶️":
                    return True
                return False
            try:
                await msg.add_reaction('▶️')
                await self.bot.wait_for('raw_reaction_add', timeout=20.0, check=reaction_check)
                embed = discord.Embed(
                    title=f'{ctx.guild.name} Features!',
                    color=ctx.author.colour, timestamp=datetime.datetime.utcnow()
                )
                embed.set_thumbnail(url=ctx.guild.icon_url)
                if 'VIP_REGIONS' in ctx.guild.features:
                    embed.add_field(name='VIP Region?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='VIP Region?', value='<:Nope:757666131854098726> Nope!')
                if 'VANITY_URL' in ctx.guild.features:
                    embed.add_field(name='Vanity URL?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Vanity URL?', value='<:Nope:757666131854098726> Nope!')
                if 'INVITE_SPLASH' in ctx.guild.features:
                    embed.add_field(name='Invite Splash?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Invite Splash?', value='<:Nope:757666131854098726> Nope!')
                if 'VERIFIED' in ctx.guild.features:
                    embed.add_field(name='Verified?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Verified?', value='<:Nope:757666131854098726> Nope!')
                if 'PARTENERED' in ctx.guild.features:
                    embed.add_field(name='Partner?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Partner?', value='<:Nope:757666131854098726> Nope!')
                if 'MORE_EMOJI' in ctx.guild.features:
                    embed.add_field(name="50+ Emoji Allowance?", value=f'<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='50+ Emoji Allowance?', value='<:Nope:757666131854098726> Nope!')
                if 'DISCOVERABLE' in ctx.guild.features:
                    embed.add_field(name='Discoverable?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Discoverable?', value='<:Nope:757666131854098726> Nope!')
                if 'FEATURABLE' in ctx.guild.features:
                    embed.add_field(name='Featured?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Featured?', value='<:Nope:757666131854098726> Nope!')
                if 'COMMUNITY' in ctx.guild.features:
                    embed.add_field(name='Community?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Community?', value='<:Nope:757666131854098726> Nope!')
                if 'COMMERCE' in ctx.guild.features:
                    embed.add_field(name='Commerce?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Commerce?', value='<:Nope:757666131854098726> Nope!')
                if 'PUBLIC' in ctx.guild.features:
                    embed.add_field(name='Public?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Public?', value='<:Nope:757666131854098726> Nope!')
                if 'NEWS' in ctx.guild.features:
                    embed.add_field(name='Announcements?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Announcements?', value='<:Nope:757666131854098726> Nope!')
                if 'BANNER' in ctx.guild.features:
                    embed.add_field(name='Banners?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Banners?', value='<:Nope:757666131854098726> Nope!')
                if 'ANIMATED_ICON' in ctx.guild.features:
                    embed.add_field(name='Animated Icon?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Animated Icon?', value='<:Nope:757666131854098726> Nope!')
                if 'WELCOME_SCREEN_ENABLED' in ctx.guild.features:
                    embed.add_field(name='Welcome Screen?', value='<a:Passed:757652583392215201> Yes!')
                else:
                    embed.add_field(name='Welcome Screen?', value='<:Nope:757666131854098726> Nope!')
                embed.set_footer(text=f'Prompted by {ctx.author}', icon_url=ctx.author.avatar_url)
                await msg.clear_reactions()
                await msg.edit(embed=embed)
            except asyncio.TimeoutError:
                await msg.clear_reactions()
                await msg.edit(content='You never reacted within **20** Seconds.', embed=None)
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    @commands.bot_has_guild_permissions(read_message_history=True)
    async def history(self, ctx, channel:discord.TextChannel = None, user : discord.Member=None):
        channel = channel or ctx.channel
        msg = await ctx.send('> Fetching **all** messages in the channel: {}'.format(channel.mention))
        limit, counter = 2147483646, 0
        async for message in channel.history(limit=limit):
            counter += 1
            if counter == limit:
                await ctx.send("This channel's history is too large!")
                break
        await msg.edit(content=ctx.author.mention)
        await msg.edit(content='> The total amount of message in the channel `{}`, is **{}**.'.format(channel.name, counter))

    @commands.command(aliases=['stat'])
    @cooldown(1, 3, BucketType.user)
    async def stats(self, ctx):
        embed = discord.Embed(
            title='Mecha Karen Current Stats:',
            color=discord.Color.red(), timestamp=datetime.datetime.utcnow(),
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
        x = 0
        for i in self.bot.guilds:
            for j in i.channels:
                x += 1
        embed.add_field(name='General Stats:', value='''\
```yaml
Servers: {}
Users: {}
Channels: {}
Prefix: {}
Bot Version: {}
Discord.py ver: {}```'''.format(
            len(self.bot.guilds), len(self.bot.users), x,
            ctx.prefix,
            version.__version__, discord.__version__), inline=False)
        embed.add_field(name='Description:', value='I am Mecha Karen. An Open Sourced Bot Inspiring Others!', inline=False)
        embed.add_field(name='Server Details:', value=f'> **OS**: {os.name}\n> **Current OS**: {os.uname().sysname}\n> **CPU Usage**: {psutil.cpu_percent()}%\n> **Memory Usage**: {psutil.virtual_memory().percent}%\n> **Bandwidth Used**: {await main()} (Gbits)')
        await ctx.send(embed=embed)

    @commands.command(aliases=['member'])
    @commands.cooldown(1, 10, BucketType.user)
    async def Members(self, ctx):
        counter, counter1, counter2, counter3 = 0, 0, 0, 0
        for member in ctx.guild.members:
            if member.status == discord.Status.offline:     counter +=1
            elif member.status == discord.Status.idle:    counter1 +=1
            elif member.status == discord.Status.do_not_disturb:    counter2 +=1
            elif member.status == discord.Status.online:    counter3 +=1
        embed = discord.Embed(
            title='Members? **({})**'.format(len(ctx.guild.members)),
            color=discord.Color.red(),
            description='**Member Statuses:**\n\n<:offline:787764149706031104> **Offline: {}\n\n<:4941_online:787764205256310825> Online: {}\n\n<:3488_Idle_oxzy:787764233416736808> Idle: {}\n\n<:8608_do_not_disturb:787764218232569886> Do Not disturb: {}**'.format(counter, counter3, counter1, counter2)
        )
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(checks(bot))
