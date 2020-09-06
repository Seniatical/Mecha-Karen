import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath

class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Moderation cog is ready')

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @cooldown(1, 5, BucketType.user)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount)
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Clear**', value=(f'{amount} messages were deleted.'))
        await ctx.send(embed=e)

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason='`not given`'):
        await member.kick(reason=reason)
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Kick**', value=(f'{member} was kicked from the server.\n\nReason: {reason}.'))
        await ctx.send(embed=e)
        await member.send(embed=e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def ban(self, ctx, member: discord.Member, *, reason='`not given`'):
        await member.ban(reason=reason)
        await member.kick(reason=reason)
        e = discord.Embed(title="", description="__**Mecha Karen:**__", color=0x50C878)
        e.add_field(name='**Ban**', value=(
            f'{member} was banned from the server.\n\nReason: {reason}.\nhttps://media.tenor.com/images/fe829734d0d3b1d5faf7bb92c1a951aa/tenor.gif'))
        await ctx.send(embed=e)
        await member.send(embed=e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def unban(self, ctx, member, *, reason):
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
        e = discord.Embed(title="", description="**Mecha Karen:**", color=0x50C878)
        e.add_field(name='‏‏‎ ‎', value=f'**{reason}**')
        await ctx.send(embed=e)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def send(self, ctx, member: discord.Member=None, *, reason='Didnt say anything',):
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
    async def Mute(self, ctx, member: discord.Member):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if role not in guild.roles:
            perms = discord.Permissions(send_messages=False, speak=False)
            await guild.create_role(name="Muted", permissions=perms)
            await member.add_roles(role)
            await ctx.send(f"{member} has been muted by {ctx.author.name}")
        else:
            await member.add_roles(role)
            await ctx.send(f"{member} has been muted by {ctx.author.name} using the role: {role}")

    @commands.command(pass_context=True)
    @commands.has_guild_permissions(administrator=True)
    @cooldown(1, 5, BucketType.user)
    async def unmute(self, ctx, user: discord.Member):
        role = discord.utils.find(lambda r: r.name == 'Muted', ctx.message.server.roles)
        if user.has_role(role):
            await bot.say("{} is not muted".format(user))
        else:
            await bot.add_roles(user, role)
        '''
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        guild = ctx.guild
        if member.has_role(role):
            await member.remove_roles("Muted")
            await ctx.send(f'{member} has been unmuted')
        else:
            await ctx.send('Member is not muted')
        '''

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    async def nuke(self, ctx, channels : discord.TextChannel=None):
        if ctx.author != ctx.guild.owner:
            await ctx.channel.purge(limit=1)
            await ctx.send('**You are not the owner of the server!**')
            sif = ctx.guild.channels
            if sif == True:
                await sif.send(f'**{ctx.author} tried to nuke {channels}!**')
        else:
            if channels == None:
                await ctx.send('Give a channel')
            else:
                verif = await ctx.send('Are you sure!')
                await ctx.send('Type in `yes`. To proceed')

                def check(m):
                    return m.content == 'yes'

                msg = await self.bot.wait_for('message', check=check)
                await ctx.channel.send('Theres no going back!\n**Are you sure.**')
                def check(m):
                    return m.content == 'yes'

                msg = await self.bot.wait_for('message', check=check)
                await ctx.send('Ok Nuking channel now!')
                name = channels.name
                category = channels.category
                position = channels.position
                topic = channels.topic
                await channels.delete()
                await ctx.guild.create_text_channel(category=category, position=position, name=name, topic=topic)
                await ctx.guild.channels.send('Hello')

                time.sleep(5) 

def setup(bot):
    bot.add_cog(Moderation(bot))
