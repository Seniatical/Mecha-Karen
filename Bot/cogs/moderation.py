import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown
import asyncio

from Others import *

class moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases = ['purge'])
    @commands.has_permissions(manage_messages=True)
    @cooldown(1, 5, BucketType.user)
    async def clear(self, ctx, amount=2):
        if amount > 100:
            await ctx.send('Amount cant be larger than **100**.')
            return
        await ctx.channel.purge(limit=amount)
        await ctx.send(f'Cleared {amount} messages from the channel {ctx.channel.name}')

    @commands.command()
    @cooldown(1, 5, BucketType.user)
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member=None, *, reason='Wasnt Provided.'):
        if member == None:
            await ctx.send('Please provide a member.')
            return
        try:
            await member.send('You have been kicked from {}.\n**Reason:**\n\n{}'.format(reason))
        except Exception:
            pass
        await member.kick(reason=reason)
        await ctx.send('Sucessfully kicked **{}**.'.format(member))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def ban(self, ctx, member: discord.Member=None, *, reason='Wasnt Provided.'):
        if member == None:
            await ctx.send('Please provide a member.')
            return
        try:
            await member.send('You have been banned from **{}**.\n**Reason:**\n\n{}'.format(reason))
        except Exception:
            pass
        await member.ban(reason=reason)
        await ctx.send('Sucessfully banned **{}**.'.format(member))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @cooldown(1, 5, BucketType.user)
    async def unban(self, ctx, member=None, *, reason='Wasnt Provided.'):
        if member == None:
            await ctx.send('Who would you like unbanned?\nNext time provide a user.')
        banned_users = await ctx.guild.bans()
        member_name, member_disc = member.split('#')

        for banned_entry in banned_users:
            user = banned_entry.user

            if (user.name, user.discriminator) == (member_name, member_disc):
                await ctx.guild.unban(user)
                await ctx.send(member_name + f' was unbanned. | {reason}')
                return
        await ctx.send(member + ' was not found')

    @commands.command()
    @commands.has_guild_permissions(manage_messages=True)
    @cooldown(1, 5, BucketType.user)
    async def Mute(self, ctx, member: discord.Member=None, *, reason='Not Given'):
        if member == None:
            await ctx.send('Please provide a member.')
            return
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if role not in ctx.guild.roles:
            perms = discord.Permissions(add_reactions=False, send_messages=False, connect=False)
            await ctx.guild.create_role(name='Muted', permissions=perms)
            await member.add_roles(role)
            for x in member.roles:
                if x == ctx.guild.default_role:
                    pass
                else:
                    y = discord.utils.get(ctx.guild.roles, name=x.name)
                    await member.remove_roles(y)
            await ctx.send(f"{member} has been muted by {ctx.author.name}")
        else:
            for x in member.roles:
                if x == ctx.guild.default_role:
                    pass
                else:
                    y = discord.utils.get(ctx.guild.roles, name=x.name)
                    await member.remove_roles(y)
            await member.add_roles(role)
            await ctx.send(f"{member} has been muted by {ctx.author.name} using the role: {role}")

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    @commands.has_guild_permissions(manage_messages=True)
    async def Unmute(self, ctx, member : discord.Member=None):
        if member == None:
            await ctx.send('Please give a member.')
            return
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        try:
            await member.remove_roles(role)
            await ctx.send('Sucessfully unmuted {}.'.format(member))
        except Exception:
            await ctx.send('That user isnt muted!')

    @commands.command()
    @cooldown(1, 300, BucketType.user)
    @commands.is_owner()
    async def nuke(self, ctx, channels : discord.TextChannel=None):
        if channels == None:
            await ctx.send('Give a channel')
            return
        if ctx.author != ctx.guild.owner:
            await ctx.send('Only **{}** Can use this Command'.format(ctx.guild.owner))
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
            new = await channels.clone()
            await channels.delete()
            await new.send('https://media1.tenor.com/images/6c485efad8b910e5289fc7968ea1d22f/tenor.gif?itemid=5791468')
            await asyncio.sleep(2)
            await new.send('**Mecha Karen** has nuked this channel!')

                
    @commands.command(aliases=['nick'])
    @commands.has_guild_permissions(manage_nicknames=True)
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
    async def slowmode(self, ctx, time : int=0):
        if time < 0:
            await ctx.send('Give a positive number.')
            return
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
    bot.add_cog(moderation(bot))
