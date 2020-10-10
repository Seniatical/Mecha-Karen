import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import aiofiles
import os

from Others import *
'''
START COG "./BRACK.LOAD-HYPER>FUNC["file"]" ;
    IF NOT NIL :
        {
        LOAD-UP => TRUE ;
            EXCEPT ERROR AS FAILURE ;
                DASHPANEL.ERROR => TRUE ;
                    PASS CONTEXT :
                        {
                        ERROR
                        LINE
                        ERROR-TYPE
                    }
    }
'''
class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @cooldown(1, 5, BucketType.user)
    async def clear(self, ctx, amount=2):
        channel = self.bot.get_channel(Channel.log)
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared {amount} messages from the channel {ctx.channel.name}')
        embed = discord.Embed(title='Moderation Action!', color=discord.Color.red(), description=f'`{ctx.author.name}` has cleared `{amount}` of messages in the channel **`{ctx.channel}`**')
        await channel.send(embed=embed)

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='`not given`'):
        channel = self.bot.get_channel(Channel.log)
        await member.kick(reason=reason)
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Kick**', value=(f'{member} was kicked from the server.\n\nReason: {reason}.'))
        embed = discord.Embed(title='Moderation Action!', color=discord.Color.red(), description=f'`{ctx.author.name}` has cleared has kicked {member} from the guild!\n\n**Reason:**\n```\n{reason}\n```**')
        await channel.send(embed=embed)
        await ctx.send(embed=e)
        try:
            await member.send(embed=e)
        except Exception:
            pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason='`not given`'):
        channel = self.bot.get_channel(Channel.log)
        await member.ban(reason=reason)
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Ban**', value=(
            f'{member} was banned from the server.\n\nReason: {reason}.\n'))
        e.set_image(url='https://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif')
        await ctx.send(embed=e)
        await member.send(embed=e)
        try:
            await member.send(embed=e)
        except Exception:
            pass

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def unban(self, ctx, member, *, reason):
        channel = self.bot.get_channel(Channel.log)
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(member_name + f' was unbanned. | {reason}')
                return
        await ctx.send(member + ' was not found')

    @commands.command(aliases=['msg'])
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def message(self, ctx, *, reason=''):
        channel = self.bot.get_channel(Channel.log)
        e = discord.Embed(title="", description="**Mecha Karen:**", color=0x50C878)
        e.add_field(name='‏‏‎ ‎', value=f'**{reason}**')
        await ctx.send(embed=e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def send(self, ctx, member: discord.Member=None, *, reason='Didnt say anything',):
        channel = self.bot.get_channel(Channel.log)
        if member == None:
            await ctx.send('Who you sending the message to then?')
        elif member == member.display_name:
            e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
            e.add_field(name='**Msg Sent**', value=(f'Dear {member}:\n\n**{reason}**'))
            amount = 1
            for am in range(amount):
                await ctx.channel.purge(limit=1)
                await member.send(embed=e)
                time.sleep(0.7)
        else:
            e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
            e.add_field(name='**Msg Sent**', value=(f'Dear {member}:\n\n**{reason}**'))
            amount = 1
            for am in range(amount):
                await ctx.channel.purge(limit=1)
                await member.send(embed=e)

    @commands.command()
    @commands.has_guild_permissions(administrator=True)
    @cooldown(1, 5, BucketType.user)
    async def Mute(self, ctx, member: discord.Member, *, reason=None):
        if reason == None:
            reason = 'Not given'
        else:
            pass
        channel = self.bot.get_channel(Channel.log)
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role not in ctx.guild.roles:
            await guild.create_role(name="Muted", permissions=discord.Permissions(send_messages=False))
            await member.add_roles(role)
            await ctx.send(f"{member} has been muted by {ctx.author.name}")
            embed = discord.Embed(title='Moderation Action!', color=discord.Color.red(), description=f'{ctx.author.name} has muted {member}.\n**Reason:**\n```\n{reason}\n```')
            await channel.send(embed=embed)
        else:
            await member.add_roles(role)
            await ctx.send(f"{member} has been muted by {ctx.author.name} using the role: {role}")
            embed = discord.Embed(title='Moderation Action!', color=discord.Color.red(), description=f'{ctx.author.name} has muted {member}.\nReason {reason}')
            await channel.send(embed=embed)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def Unmute(self, ctx, member : discord.Member):
        channel = self.bot.get_channel(Channel.log)
        guild = ctx.guild
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        try:
            await member.remove_roles(role)
            embed = discord.Embed(title='Moderation Action!', color=discord.Color.red(), description=f'{ctx.author.name} has unmuted the user {member.display_name}.')
            await channel.send(embed=embed)
        except Exception:
            await ctx.send('That user isnt muted!')

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def nuke(self, ctx, channels : discord.TextChannel=None):
        if ctx.author != ctx.guild.owner:
            await ctx.channel.purge(limit=1)
            await ctx.send('**You are not the owner of the server!**')
        else:
            if channels == None:
                await ctx.send('Give a channel')
            else:
                verif = await ctx.send('Are you sure!')
                await ctx.send('Type in `yes`. To proceed')

                def check(m):
                    user = ctx.author
                    return m.author.id == user.id and m.content == 'yes'

                msg = await self.bot.wait_for('message', check=check)
                await ctx.channel.send('Theres no going back!\n**Are you sure.**')
                def check(m):
                    user = ctx.author
                    return m.author.id == user.id and m.content == 'yes'

                msg = await self.bot.wait_for('message', check=check)
                await ctx.send('Ok Nuking channel now!')
                name = channels.name
                category = channels.category
                position = channels.position
                topic = channels.topic
                if channels.is_nsfw() == True:
                    nsfw = True
                else:
                    nsfw = False
                await channels.delete()
                await ctx.guild.create_text_channel(category=category, position=position, name=name, topic=topic, nsfw=nsfw)
                await ctx.guild.channels.send('Hello')

                time.sleep(5)

    @commands.command()
    @commands.is_owner()
    async def change(self, ctx, *args):
        Nick = ' '.join(map(str, args))
        if Nick == None:
            await ctx.send('You cant name everybody nothing.')
        else:
            for member in ctx.guild.members:
                if member == ctx.guild.owner:
                    pass
                else:
                    await member.edit(nick=f'{Nick}')
                    time.sleep(0.5)
        await ctx.send(f'The entire guild user name was set to `{Nick}`!!!')

    @commands.command()
    @commands.is_owner()
    async def revert(self, ctx):
        for member in ctx.guild.members:
            if member == ctx.guild.owner:
                pass
            else:
                await member.edit(nick=f'{member.name}')
                time.sleep(0.5)
        await ctx.send('All your guild users name have returned to normal!')

    @commands.command(aliases=['nick'])
    @commands.has_guild_permissions(administrator=True)
    async def nickname(self, ctx, member : discord.Member, *args):
        if member == None:
            await ctx.send('Give me a user dumbass')
        elif member == ctx.guild.owner:
            await ctx.send('You cant name the owner!')
        else:
            x = ' '.join(map(str, args))
            await member.edit(nick=f'{x}')
            await ctx.send(f'{member.name} has been changed to {x}')

    @commands.command()
    @commands.has_guild_permissions(manage_channels=True)
    @commands.cooldown(1, 60, BucketType.user)
    async def slowmode(self, ctx, time : int):
        try:
            if time > 21600:
                await ctx.send('Number is too large. You can only have a maximum time of `21600` seconds (6 Hours)')
            else:
                await ctx.channel.edit(slowmode_delay=time)
                await ctx.send(f'The channel {ctx.channel.name} now has a slowmode of {time} seconds')
        except Exception:
            await ctx.send('Not a number!')

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx, channel: discord.TextChannel=None):
        channel = channel or ctx.channel

        if ctx.guild.default_role not in channel.overwrites:
            overwrites = {
            ctx.guild.default_role: discord.PermissionOverwrite(send_messages=False)
            }
            await channel.edit(overwrites=overwrites)
            await ctx.send("**The channel `{}` has successfully been locked!**".format(ctx.channel.name))
        elif channel.overwrites[ctx.guild.default_role].send_messages == True or channel.overwrites[ctx.guild.default_role].send_messages == None:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = False
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send("**The channel `{}` has successfully been locked!**".format(ctx.channel.name))
        else:
            overwrites = channel.overwrites[ctx.guild.default_role]
            overwrites.send_messages = True
            await channel.set_permissions(ctx.guild.default_role, overwrite=overwrites)
            await ctx.send('**The channel `{}` has now been unlocked!**'.format(ctx.channel.name))

def setup(bot):
    bot.add_cog(Moderation(bot))
