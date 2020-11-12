import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
import datetime
import time
import sys
import asyncio
import math

from Utils import main

def convert_size(bytes):
   if bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(bytes, 1024)))
   p = math.pow(1024, i)
   s = round(bytes / p, 2)
   return "%s %s" % (s, size_name[i])

class Checks(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['info', 'whois', 'Userinfo'])
    @cooldown(1, 30, BucketType.user)
    async def user(self, ctx, member: discord.Member=None):
        member = ctx.author if not member else member
        roles = [role for role in member.roles]
        roles.pop(0)
        embed = discord.Embed(color=member.color, timestamp=datetime.datetime.utcnow())
        embed.set_author(name=f"{member}", icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name="Joined at:", value=member.joined_at.strftime("%a, %#d %B %Y, %I:%M %p"))
        embed.add_field(name='Registered at:', value=member.created_at.strftime('%a, %#d %B %Y, %I:%M %p'))
        if len(roles) == 0:
            embed.add_field(name='Roles (0)', value='There are no roles for this user.', inline=False)
        else:
            embed.add_field(name=f"Roles ({len(roles)})", value="   ".join([role.mention for role in roles]), inline=False)
        embed.set_footer(icon_url=ctx.author.avatar_url,
                         text=f'ID: {member.id}\nPrompted by  {ctx.author.name}')
        await ctx.send(embed=embed)


    @commands.command(aliases=['avatar'])
    @cooldown(1, 60, BucketType.user)
    async def av(self, ctx, member: discord.Member=None):
        if member == None:
            member = ctx.author
        else:
            pass
        user = ctx.author
        embed = discord.Embed(
            title=f"{member}'s avatar",
            color=member.color, timestamp=datetime.datetime.utcnow(),
        )
        embed.set_image(url=member.avatar_url)
        embed.set_footer(text=f'Requested by: {user}')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 5, BucketType.guild)
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
            banner = ctx.guild.region[0]
            banner = list(banner)
            x = banner[0].upper()
            banner.pop(0)
            banner.insert(0, x)
            banner = ''.join(map(str, banner))
            embed.add_field(name='Region?', value=f'{banner}')
            embed.add_field(name=f'Created at?', value=f"{ctx.guild.created_at.strftime('%a, %#d %B %Y, %I:%M %p')}", inline=False)
            embed.add_field(name="Emoji's?", value=f'{len(ctx.guild.emojis)}')
            embed.add_field(name=f'Members?', value=f'{len(ctx.guild.members)}')
            verif = ctx.guild.verification_level[0]
            verif = list(verif)
            x = verif[0].upper()
            verif.pop(0)
            verif.insert(0, x)
            verif = ''.join(map(str, verif))
            embed.add_field(name=f'Verification Level?', value=f'{verif}')
            if ctx.guild.afk_channel == True:
                embed.add_field(name='AFK Channel?', value=f'{ctx.guild.afk_channel.name}', inline=False)
                embed.add_field(name='AFK Timeout?', value=f'{ctx.guild.afk_timeout}')
            else:
                pass
            
            true = ctx.guild.mfa_level
            if true == 1:
                true = 'Yes!'
            else:
                true = 'No!'
            embed.add_field(name='Admin 2FA?', value=f'{true}')
            boost = ctx.guild.premium_subscription_count
            if boost == 0:
                boost = 'None 😭'
            else:
                pass
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
            bots = 0
            for member in ctx.guild.members:
                if member.bot == True:
                    bots += 1
                else:
                    pass
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
                await self.bot.wait_for('raw_reaction_add', timeout=300.0, check=reaction_check)
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
                await msg.delete()
                await ctx.send('You never reacted in time!')
        except Exception as e:
            await ctx.send(e)

    @commands.command()
    async def history(self, ctx):
        limit = 2147483646
        counter = 0
        async for message in ctx.channel.history(limit=limit):
            if message.author == self.bot.user:
                counter += 1
                if counter == limit:
                    await ctx.send('Your channel History is to Large!')
                else:
                    pass
        await ctx.send(f"Messages sent: {counter}")

    @commands.command(aliases=['stat'])
    @cooldown(1, 3, BucketType.user)
    async def stats(self, ctx):
        embed = discord.Embed(
            title='Mecha Karen Current Stats:',
            color=discord.Color.red(), timestamp=datetime.datetime.utcnow(),
        )
        embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
        embed.add_field(name='Servers?', value=f'{len(self.bot.guilds)}')
        embed.add_field(name='Commands?', value=f'{len(self.bot.commands)}')
        embed.add_field(name='Users?', value=f'{len(self.bot.users)}')
        embed.add_field(name='Cogs?', value=f'{len(self.bot.cogs)}')
        embed.add_field(name='Case Insensitive?', value=f'{self.bot.case_insensitive}')
        embed.add_field(name="Emoji's?", value=f'{len(self.bot.emojis)}')
        embed.add_field(name='Cached Messages?', value=f'{len(self.bot.cached_messages)}')
        embed.add_field(name='Prefix?', value=f'{main.get_prefix(self.bot, ctx.message)}')
        embed.add_field(name='Extensions?', value=f'{len(self.bot.extensions)}')
        embed.add_field(name='All Commands?', value=f'{len(self.bot.all_commands)}')
        embed.add_field(name='Help Command?', value=f'Help')
        embed.add_field(name='Extra Events?', value=f'{len(self.bot.extra_events)}')
        embed.add_field(name='Voice Clients?', value=f'{len(self.bot.voice_clients)}')
        embed.add_field(name='Bot Latency?', value=f'{round(self.bot.latency * 1000)} ms')
        embed.add_field(name='Discord.py Version?', value=f'{discord.__version__}')
        embed.add_field(name='Python Version?', value =f"{sys.version.major}.{sys.version.minor}.{sys.version.micro}")
        embed.set_footer(text=f'Requested by {ctx.author} 🔸 {datetime.date.today()}')
        await ctx.send(embed=embed)

    @commands.command(aliases=['member'])
    @commands.cooldown(1, 10, BucketType.user)
    async def Members(self, ctx):
        counter = 0
        counter1 = 0
        counter2 = 0
        counter3 = 0
        for member in ctx.guild.members:
            if member.status == discord.Status.offline:
                counter +=1
            elif member.status == discord.Status.idle:
                counter1 +=1
            elif member.status == discord.Status.do_not_disturb:
                counter2 +=1
            elif member.status == discord.Status.online:
                counter3 +=1
        embed = discord.Embed(
            title='Members? **({})**'.format(len(ctx.guild.members)),
            color=discord.Color.red(),
            description='**Member Statuses:**\n\n<:medium:756904264424620103> **Offline: {}\n\n🟢 Online: {}\n\n🟠 Idle: {}\n\n🔴 Do Not disturb: {}**'.format(counter, counter3, counter1, counter2)
        )
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(checks(bot))
