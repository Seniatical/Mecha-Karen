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
import datetime
from discord.ext.commands import BucketType, cooldown

import time
import asyncio
from Helpers import emoji

__all__ = (
    "fun",
    "mod",
    'image_',
    "misc",
    "games",
    "nsfw_",
    "music"
)

async def fun(bot):
    names = []
    cogs = bot.get_cog('fun')
    for command in cogs.get_commands():
        names.append('`' + str(command.name) + '`')
    return names

async def mod(bot):
    names = []
    cogs = bot.get_cog('moderation')
    for command in cogs.get_commands():
        names.append('`' + str(command.name).title() + '`')
    names.append('`Warn` `Warns` `Delwarn` `Clearwarns`')
    return names

async def image_(bot):
    names = []
    cogs = [bot.get_cog('reddit'), bot.get_cog('image')]
    for cog in cogs:
        for command in cog.get_commands():
            if not command.name.lower() == 'trigger':
                names.append('`' + str(command.name) + '`')
    return names

async def misc(bot):
    names = []
    cogs = [bot.get_cog('scrapers'), bot.get_cog('motivation'), bot.get_cog('misc'), bot.get_cog('checks'), bot.get_cog('checks')]
    for cog in cogs:
        for command in cog.get_commands():
            if not command.name == 'help':
                names.append('`' + str(command.name) + '`')
    names.append('`Snipe`')
    return names

async def games(bot):
    names = []
    cogs = bot.get_cog('games')
    for command in cogs.get_commands():
        if not command.name.lower() == 'snipe' or not command.name.lower() == 'bowling':
            names.append('`' + command.name.title() + '`')
    return names

async def nsfw_(bot):
    names = []
    cogs = bot.get_cog('nsfw')
    for command in cogs.get_commands():
        names.append('`' + command.name + '`')
    return names

async def music(bot):
    names = []
    cog = bot.get_cog('Music')
    for command in cog.get_commands():
        names.append('`' + command.name.title() + '`')
    return names

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 5, BucketType.user)
    async def help(self, ctx, option=None):
        global x
        prefix_ = ctx.prefix
        if option:
            x = option.lower()
        if not option:
            e = discord.Embed(color=discord.Color.red())
            e.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            e.add_field(name=':scales: **Moderation**‎‏‏‎‎', value='`{}Help Mod`'.format(prefix_))
            e.add_field(name=':jigsaw: **Fun**', value='`{}Help Fun`'.format(prefix_))
            e.add_field(name=':camera: **Images**', value='`{}Help Images`'.format(prefix_))
            e.add_field(name=':bowling: **Games**', value='`{}Help Games`'.format(prefix_))
            e.add_field(name=':wrench: **Management**', value='`{}Help Manage`'.format(prefix_))
            e.add_field(name='<a:finger_hole:744627487027494984> NSFW‏‏‎‎', value='`{}Help NSFW`'.format(prefix_))
            e.add_field(name='☛ Misc', value='`{}Help Misc`'.format(prefix_))
            e.add_field(name='🎶 Music', value='`{}Help Music`'.format(prefix_))
            e.add_field(name='​', value='​'.format(prefix_))
            e.add_field(name='‏',value=f'‏Join our **[Support Server](https://discord.gg/Q5mFhUM)** | Invite **[Mecha Karen](https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)**‎', inline=False)
            e.set_thumbnail(url=self.bot.user.avatar_url)
            e.set_footer(text='Bot Created by _-*™#7519 • 05/08/2020', icon_url='https://i.imgur.com/jSzSeva.jpg')
            await ctx.send(embed=e)

        elif x == 'mod' or x == 'moderation':
            e = discord.Embed(color=discord.Color.red())
            e.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            e.add_field(name="**Mod Help:**",
                        value=' '.join(await mod(self.bot)))
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            await ctx.send(embed=e)

        elif x == 'fun':
            x = await fun(self.bot)
            e = discord.Embed(color=discord.Color.red())
            e.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.add_field(name="**Fun Help:**",
                        value=' '.join(map(str, x)))
            e.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            await ctx.send(embed=e)

        elif x == 'image' or x == 'images' or x == 'img':
            img = await image_(self.bot)
            embed = discord.Embed(color=discord.Color.red())
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            embed.add_field(name="**Image Help:**",
                            value=' '.join(map(str, img))
                            )
            embed.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            await ctx.send(embed=embed)

        elif x == 'misc' or x == 'miscellaneous':
            misc_ = await misc(self.bot)
            embed = discord.Embed(
                title='Miscellaneous Help',
                colour=discord.Color.red()
            ).add_field(name='Commands:',
                        value=' '.join(map(str, misc_)))
            embed.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020'
            )
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

        elif x == 'games' or x == 'game':
            com = await games(self.bot)
            embed = discord.Embed(
                title='**Games**',
                color=discord.Color.red()
            )
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            embed.add_field(name='**Current Games:**', value=' '.join(map(str, com)))
            embed.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            await ctx.send(embed=embed)

        elif x == 'manage' or x == 'mng' or x == 'manage':
            embed = discord.Embed(
                title='**Management**',
                color=discord.Color.red(),
                description='**Note:** This section will be moved to the dashboard once its been completed:\nPreview: {}'.format('https://mechakaren.xyz/')
            )
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            embed.add_field(name='**Current Commands:**',
                            value='''
                            `Starboard` `Setboard` `SetStarLimit` `Disable` `Enable` `Set_Tickets` 
                            `Remove_Tickets` `Change_Prefix` `Prefix`
                            '''
                            )
            ## <a:nope:787764352387776523>
            embed.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            await ctx.send(embed=embed)

        elif x == 'nsfw':
            good_stuff = await nsfw_(self.bot)
            if not ctx.channel.is_nsfw():
                await ctx.send('Please use this command in a channel marked with **NSFW**. This due to the naming of commands being graphic.')
                return
            embed = discord.Embed(
                title='NSFW Commands',
                color=discord.Color.purple()
            )
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            embed.set_thumbnail(url='http://avoiderdragon.com/wp-content/uploads/2016/02/thumbnail_vr-porn.jpg')
            embed.add_field(name='‏‏‎ ‎', value=' '.join(map(str, good_stuff)))
            embed.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            await ctx.send(embed=embed)

        elif x == 'music' or x == 'm':
            commands = ' '.join(map(str, await music(self.bot)))
            embed = discord.Embed(
                title='Music Commands',
                color=discord.Color.red()
            )
            embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            embed.add_field(name='Commands:', value=commands)
            embed.set_footer(
                icon_url='https://i.imgur.com/jSzSeva.jpg',
                text='Bot Created by _-*™#7519 • 05/08/2020')
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

        else:
            y = None
            for command_ in self.bot.commands:
                if command_.name.lower() == x.lower() or x.lower() in [i.lower() for i in command_.aliases]:
                    params = [command_.clean_params[i] for i in command_.clean_params]
                    y = ['```{}{} '.format(prefix_, command_.name), '```']
                    for i in params:
                        y.insert(-1, '<' + i.name + '> ')
                    break
            if y:
                embed = discord.Embed(
                    title='Help: ' + x.title(),
                    colour=discord.Colour.red(),
                    description='Command Enabled: {}'.format(command_.enabled),
                    timestamp=ctx.message.created_at
                )

                embed.set_footer(text='Requested by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
                embed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
                embed.set_thumbnail(url=self.bot.user.avatar_url)
                embed.add_field(name='Params:', value=''.join(map(str, y)), inline=False)
                embed.add_field(name='Aliases:', value=' '.join(['`' + i + '`' for i in command_.aliases]) or 'None!', inline=False)
                return await ctx.send(embed=embed)

            e = discord.Embed(color=discord.Color.red())
            e.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.avatar_url)
            e.add_field(name=':scales: **Moderation**‎‏‏‎‎', value='`{}Help Mod`'.format(prefix_))
            e.add_field(name=':jigsaw: **Fun**', value='`{}Help Fun`'.format(prefix_))
            e.add_field(name=':camera: **Images**', value='`{}Help Images`'.format(prefix_))
            e.add_field(name=':bowling: **Games**', value='`{}Help Games`'.format(prefix_))
            e.add_field(name=':wrench: **Management**', value='`{}Help Manage`'.format(prefix_))
            e.add_field(name='<a:finger_hole:744627487027494984> NSFW‏‏‎‎', value='`{}Help NSFW`'.format(prefix_))
            e.add_field(name='☛ Misc', value='`{}Help Misc`'.format(prefix_))
            e.add_field(name='🎶 Music', value='`{}Help Music`'.format(prefix_))
            e.add_field(name='​', value='​')
            e.add_field(name='‏',value=f'‏Join our **[Support Server](https://discord.gg/Q5mFhUM)** | Invite **[Mecha Karen](https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)**‎', inline=False)
            e.set_thumbnail(url=self.bot.user.avatar_url)
            e.set_footer(text='Bot Created by _-*™#7519 • 05/08/2020', icon_url='https://i.imgur.com/jSzSeva.jpg')
            await ctx.send(embed=e)

    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def status(self, ctx):
        await ctx.send('Are you blind. Click my profile for the love of god')

    @commands.command()
    @cooldown(1, 30, BucketType.guild)
    async def invite(self, ctx):
        embed = discord.Embed(
            title='**Invite**',
            colour=ctx.author.color
        )
        embed.add_field(name='Mecha Karen',
                        value='\nIf you would like to invite me! \n[Click Here](https://discord.com/api/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)')
        embed.add_field(name='Need help?',
                        value='Join our Support Server! \n[Click Here](https://discord.gg/Q5mFhUM)')
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
        embed.set_footer(
            icon_url='https://i.imgur.com/jSzSeva.jpg',
            text='Bot created by _-*™#7139')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, BucketType.guild)
    async def source(self, ctx):
        embed = discord.Embed(
            title='**Source Code**',
            color=discord.Color.red()
        )
        embed.description = '[Click here](https://github.com/Seniatical/Mecha-Karen-Source-Code)'
        embed.set_footer(
            icon_url='https://i.imgur.com/jSzSeva.jpg',
            text='Bot created by _-*™#7139')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
