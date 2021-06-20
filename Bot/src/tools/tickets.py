from typing import Dict, Any

import discord
from discord import PermissionOverwrite
from discord.ext import commands
import sqlite3

def over(member, role):
    overwrites: Dict[Any, PermissionOverwrite] = {
        member: discord.PermissionOverwrite(
            send_messages=True, read_messages=True, read_message_history=True,
            attach_files=True, add_reactions=True, use_external_emojis=True
            ),
        role: discord.PermissionOverwrite(
            send_messages=True, read_messages=True, read_message_history=True,
            attach_files=True, add_reactions=True, use_external_emojis=True
        )
        }
    return overwrites

class tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client
        
        self.table = self.client['Bot']
        self.col = self.table['Tickets']

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == '🔒' and not payload.member.bot:
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.embeds:
                return
            dict_ = message.embeds[0].to_dict()
            try:
                if dict_['color'] != 1752220 and len(dict_['title'].split('#')) != 2:
                    return
                if not str(payload.member) == dict_['title'].split("'")[0]:
                    return
            except KeyError:
                return
            channel = self.bot.get_channel(payload.channel_id)
            await channel.delete()
            
        if not payload.emoji.name == '📩':
            return
        data = self.col.find_one({'_id': payload.guild_id})

        if not data or payload.member.bot:
            return
        
        category, message, root, count, role = (
            data['c'], data['m'], data['r'],
            data['co'], data['ro']
        )
        
        try:
            ticket_message = await self.bot.get_channel(root).fetch_message(message)
        except Exception:
            return
        ## Message not found
        
        if payload.member != self.bot.user:
            await ticket_message.remove_reaction(payload.emoji, payload.member)
            
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        helper: discord.Role = discord.utils.get(guild.roles, id=role)
            
        if not category:
            channel = await guild.create_text_channel(
                name='ticket-{}'.format(count),
                overwrites=over(payload.member, helper),
                reason='Ticket Opened by {}'.format(payload.member)
            )
            
        else:
            category: discord.CategoryChannel = self.bot.get_channel(category)
            channel = await category.create_text_channel(
                name='ticket-{}'.format(count),
                overwrites=over(payload.member, helper),
                reason='Ticket Opened by {}'.format(payload.member)
            )
            
        self.col.update_one({'_id': payload.guild_id}, {'$set': {'co': (count + 1)}})
        
        msg = await channel.send(embed=discord.Embed(
            title="{}'s Ticket:".format(payload.member),
            description=f'''
            This is your support ticket, State your problems here and a user with the role {helper.mention} will be with you.
            To close this ticket react with a \🔒 to close this ticket.
            ''',
            colour=discord.Colour.teal()
        ))
        await msg.add_reaction('🔒')

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def set_ticket(self, ctx,
                         channel: discord.TextChannel,
                         helper: discord.Role,
                         category: discord.CategoryChannel = None,
                         *, notes: str = None) -> None:

        embed = discord.Embed(
            title='Tickets!',
            description='React to the message below to open a ticket!',
            colour=discord.Colour.teal(),
            timestamp=ctx.message.created_at
        )
        
        if category:
            embed.add_field(name='Info:', value=f'''
            Once your **Ticket** has been opened, You will be redirected to {category.mention}.
            Please wait patiently for a user to come help you!

            **ADDITIONS:**

            Users with roles {helper.mention} and higher can only access your tickets.
            **Notes:** {'None Provided.' if not notes else notes}
            ''')
        else:
            embed.add_field(name='Info:', value=f'''
            Once your **Ticket** has been opened, You will be redirected to the top of your server.
            Please wait patiently for a user to come help you!

            **ADDITIONS**:
            
            Users with roles **{helper.name}** and higher can only access your tickets.
            **Notes:** {'None Provided.' if not notes else notes}
            ''')
        embed.set_footer(text='Opened Tickets', icon_url=self.bot.user.avatar)
        embed.set_thumbnail(url='https://cdn.onlinewebfonts.com/svg/img_63409.png')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('📩')
        try:
            self.col.insert_one({'_id': ctx.guild.id, 'c': category.id, 'm': msg.id, 'r': channel.id, 'co': 1, 'ro': helper.id})
        except Exception:
            ## Too lazy to put the mongo exception
            ## Exception raised is todo with the existing key
            self.col.update_one({'_id': ctx.guild.id}, {'$set': {'c': category.id, 'm': msg.id, 'r': channel.id, 'co': 1, 'ro': helper.id}})
        return await ctx.send('Successfully setup tickets for your server!')

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def remove_tickets(self, ctx):
        is_active = self.col.find_one({'_id': ctx.guild.id})
        
        if not is_active:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> No tickets have been set for this server',
                colour=discord.Colour.red()
            ))
        
        self.col.delete_one({'_id': ctx.guild.id})
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Tickets is no longer active with your server!',
            colour=discord.Colour.green()
        ))

def setup(bot):
    bot.add_cog(tickets(bot))
