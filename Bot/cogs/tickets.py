# !/usr/bin/python

"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0

A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.

FULL LISENCE CAN BE FOUND:
    https://www.apache.org/licenses/LICENSE-2.0.html

Any voilations to the lisence, will result in moderate action

Your required to mention (original author, lisence, source, any changes made)
"""

from typing import Dict, Any

import discord
from discord import PermissionOverwrite
from discord.ext import commands
from Utils import db
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

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.emoji.name == '🔒' and not payload.member.bot:
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if not message.embeds:
                return
            dict_ = message.embeds[0].to_dict()
            if dict_['color'] != 1752220 and len(dict_['title'].split('#')) != 2:
                return
            if not str(payload.member) == dict_['title'].split("'")[0]:
                return
            channel = self.bot.get_channel(payload.channel_id)
            await channel.delete()
        if not payload.emoji.name == '📩':
            return
        category, message, root, count, role = db.record(
            'SELECT TicketChannel, TicketMessage, TMC, Count, HelperRole FROM tickets WHERE GuildID = ?',
            payload.guild_id) or (None, None, None, 0, None)
        if not message or not root or payload.member.bot:
            return
        ticket_message = await self.bot.get_channel(root).fetch_message(message)
        if payload.member != self.bot.user:
            await ticket_message.remove_reaction(payload.emoji, payload.member)
        guild: discord.Guild = self.bot.get_guild(payload.guild_id)
        helper: discord.Role = discord.utils.get(guild.roles, name=role)
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
        db.execute(
            'UPDATE tickets SET Count = Count + 1 WHERE GuildID = ?', payload.guild_id)
        db.commit()
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
                         channel: discord.TextChannel = None,
                         helper: discord.Role = None,
                         category: discord.CategoryChannel = None,
                         *, notes: str = None) -> None:
        if not channel:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Provide the channel were the Tickets will be created at!',
                colour=discord.Colour.red()
            ))
        if not helper:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Provide the minimum role for a user to help in the ticket channels!',
                colour=discord.Colour.red()
            ))
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

            Users with roles {helper.mention} and higher can only help you.
            **Notes:** {'None Provided.' if not notes else notes}
            ''')
        else:
            embed.add_field(name='Info:', value=f'''
            Once your **Ticket** has been opened, You will be redirected to the top of your server.
            Please wait patiently for a user to come help you!

            **ADDITIONS**:
            
            Users with roles **{helper.name}** and higher can only help you.
            **Notes:** {'None Provided.' if not notes else notes}
            ''')
        embed.set_footer(text='Opened Tickets', icon_url=self.bot.user.avatar_url)
        embed.set_thumbnail(url='https://cdn.onlinewebfonts.com/svg/img_63409.png')
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('📩')
        try:
            db.execute(
                'INSERT INTO tickets (GuildID, TicketChannel, TicketMessage, TMC, HelperRole) VALUES (?, ?, ?, ?, ?)',
                ctx.guild.id, category.id, msg.id, channel.id, helper.name)
        except sqlite3.IntegrityError:
            db.execute(
                'UPDATE tickets SET TicketChannel = ?, TicketMessage = ?, TMC = ?, HelperRole = ? WHERE GuildID = ?',
                category.id, msg.id, channel.id, helper.name, ctx.guild.id)
        db.commit()

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 20, commands.BucketType.guild)
    async def remove_tickets(self, ctx):
        is_active = db.record(
            'SELECT TicketMessage FROM tickets WHERE GuildID = ?', ctx.guild.id) or (None,)
        if not is_active[0]:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> You have not got any running tickets for this sever!.',
                colour=discord.Colour.red()
            ))
        db.execute(
            'DELETE FROM tickets WHERE GuildID = ?', ctx.guild.id)
        db.commit()
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> Tickets is no longer active with your server!',
            colour=discord.Colour.green()
        ))

def setup(bot):
    bot.add_cog(tickets(bot))
