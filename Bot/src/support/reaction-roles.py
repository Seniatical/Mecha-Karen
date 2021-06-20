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

class roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colour = ('black', 'yellow', 'red', 'green', 'pink')
        self.find = {'black' : '⚫', 'yellow' : '🟡', 'red' : '🟢', 'green' : '🔴', 'pink' : '🟣'}
        self.reverse = {'⚫' : 'black', '🟡' : 'yellow', '🟢' : 'red', '🔴' : 'green', '🟣' : 'pink'}

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        '''
        Verification
        Area
        '''
        if payload.message_id == 746333872546906144 and payload.emoji.name == '✅':
            try:
                await payload.member.add_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Supporters'))
            except AttributeError:
                return

        '''
        Ping Role
        Area
        '''
        if payload.message_id == 777208106932240386 and payload.emoji.name == '🔔':
            try:
                await payload.member.add_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Ping'))
            except AttributeError:
                return
        if payload.message_id == 777208106932240386 and payload.emoji.name == '📣':
            try:
                await payload.member.add_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Announcements'))
            except AttributeError:
                return
        if payload.message_id == 777208106932240386 and payload.emoji.name == '💝':
            try:
                await payload.member.add_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Giveaways'))
            except AttributeError:
                return
        if payload.message_id == 777208106932240386 and payload.emoji.name == 'blobidea':
            try:
                await payload.member.add_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Miscellaneous'))
            except AttributeError:
                return

        '''
        Colour Role
        Area
        '''
        if payload.message_id == 779373859769155605 and payload.emoji.name == '⚫':
            try:
                x = [i.name.lower() for i in payload.member.roles]
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Black')
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for i in x:
                    if i in self.colour:
                        await payload.member.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=i.title()))
                        for j in range(len(msg.reactions)):
                            for user in await msg.reactions[j].users().flatten():
                                if msg.reactions[j].emoji == payload.emoji.name:
                                    continue
                                elif user == payload.member:
                                    await msg.remove_reaction(msg.reactions[j].emoji, payload.member)
                await payload.member.add_roles(role)
            except AttributeError:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🟡':
            try:
                x = [i.name.lower() for i in payload.member.roles]
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Yellow')
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for i in x:
                    if i in self.colour:
                        await payload.member.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=i.title()))
                        for j in range(len(msg.reactions)):
                            for user in await msg.reactions[j].users().flatten():
                                if msg.reactions[j].emoji == payload.emoji.name:
                                    continue
                                elif user == payload.member:
                                    await msg.remove_reaction(msg.reactions[j].emoji, payload.member)
                await payload.member.add_roles(role)
            except AttributeError:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🟢':
            try:
                x = [i.name.lower() for i in payload.member.roles]
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Green')
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for i in x:
                    if i in self.colour:
                        await payload.member.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=i.title()))
                        for j in range(len(msg.reactions)):
                            for user in await msg.reactions[j].users().flatten():
                                if msg.reactions[j].emoji == payload.emoji.name:
                                    continue
                                elif user == payload.member:
                                    await msg.remove_reaction(msg.reactions[j].emoji, payload.member)
                await payload.member.add_roles(role)
            except AttributeError:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🔴':
            try:
                x = [i.name.lower() for i in payload.member.roles]
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Red')
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for i in x:
                    if i in self.colour:
                        await payload.member.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=i.title()))
                        for j in range(len(msg.reactions)):
                            for user in await msg.reactions[j].users().flatten():
                                if msg.reactions[j].emoji == payload.emoji.name:
                                    continue
                                elif user == payload.member:
                                    await msg.remove_reaction(msg.reactions[j].emoji, payload.member)
                await payload.member.add_roles(role)
            except AttributeError:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🟣':
            try:
                x = [i.name.lower() for i in payload.member.roles]
                role = discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Pink')
                msg = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
                for i in x:
                    if i in self.colour:
                        await payload.member.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name=i.title()))
                        for j in range(len(msg.reactions)):
                            for user in await msg.reactions[j].users().flatten():
                                if msg.reactions[j].emoji == payload.emoji.name:
                                    continue
                                elif user == payload.member:
                                    await msg.remove_reaction(msg.reactions[j].emoji, payload.member)
                await payload.member.add_roles(role)
            except AttributeError:
                return

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        '''
        Verification
        Area
        '''
        if payload.message_id == 746333872546906144 and payload.emoji.name == '✅':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Supporters'))
            except AttributeError as e:
                return

        '''
        Ping Roles
        Area
        '''
        if payload.message_id == 777208106932240386 and payload.emoji.name == '🔔':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Ping'))
            except AttributeError as e:
                return
        if payload.message_id == 777208106932240386 and payload.emoji.name == '📣':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Announcements'))
            except AttributeError as e:
                return
        if payload.message_id == 777208106932240386 and payload.emoji.name == '💝':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Giveaways'))
            except AttributeError as e:
                return
        if payload.message_id == 777208106932240386 and payload.emoji.name == 'blobidea':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Miscellaneous'))
            except AttributeError as e:
                return

        '''
        Self-Roles
        Area
        '''
        if payload.message_id == 779373859769155605 and payload.emoji.name == '⚫':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Black'))
            except AttributeError as e:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🟡':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Yellow'))
            except AttributeError as e:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🟢':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Green'))
            except AttributeError as e:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🔴':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Red'))
            except AttributeError as e:
                return
        if payload.message_id == 779373859769155605 and payload.emoji.name == '🟣':
            try:
                for i in self.bot.get_guild(payload.guild_id).members:
                    if i.id == payload.user_id:
                        await i.remove_roles(discord.utils.get(self.bot.get_guild(payload.guild_id).roles, name='Pink'))
            except AttributeError as e:
                return

def setup(bot):
    bot.add_cog(roles(bot))
