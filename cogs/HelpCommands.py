# Imports!
import discord
from discord.ext import commands
from datetime import timedelta
from discord import ChannelType, Guild, Member, Message, Role, Status, utils, Embed
from discord.abc import GuildChannel
from discord.ext.commands import BucketType, Cog, Context, Paginator, command, group, cooldown
from discord.utils import escape_markdown
import time
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps, ImageMath
import os
import asyncio

# Class
class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Main Code
    @commands.Cog.listener()
    async def on_ready(self):
        print('Help Cog is ready')

    # Help Codes. Make sure to change it to what ever tf you want.
    @commands.command()
    @cooldown(1, 3, BucketType.user)
    async def Help(self, ctx, option=None):
        if option == None:
            pass
        else:
            x = option.lower()
        if option == None:
            e = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            e.add_field(name=':scales:\t**Moderation**‎‏‏‎‎', value='`-Help Mod`')
            e.add_field(name=':jigsaw:\t**Fun**', value='`-Help Fun`')
            e.add_field(name=':v:\t**Motivation**', value='`-Help Motiv`')
            e.add_field(name=':camera:\t**Images**', value='`-Help Images`')
            e.add_field(name=':wrench:\t**Management**', value='`-Help Manage`')
            e.add_field(name=':bowling:\t**Games**', value='`-Help Games`')
            e.add_field(name=':speech_balloon:\t**Quizzes**', value='`Coming Soon`')
            e.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
            e.add_field(name='‏‏‎ ‎', value='‏‏‎ ‎')
            e.add_field(name=' ‎', value=f'Join our [Support Server](https://discord.gg/Q5mFhUM) and help our Bot grow.')
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.set_footer(text='Use command  -Help Aliases  to view all the aliases!\nUse command -Help Invite to invite the Bot to your server!!!',
                         icon_url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            await ctx.send(embed=e)
        elif x == 'mod':
            e = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            e.add_field(name="**Mod Help:**\n**Remember to use - before every commands**",
                        value='`Ban`‏‏‎ ‎`Kick`‏‏‎ ‎`Clear`‏‏‎ ‎`Unban`‏‏‎ ‎`Sync`‏‏‎ ‎`Message`‏‏‎ ‎`Send`‏‏‎ ‎`Nuke` `WhoIs` `Server` `Stats` `Avatar` `Mute` `Actions` `History`')
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=e)
        elif x == 'fun':
            e = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.add_field(name="**Fun Help:**\n**Remember to use - before all commands**",
                        value='`Ping`‏‏‎ ‎`MagicKaren`‏‏‎ ‎`Gay`‏‏‎ ‎`IQ`‏‏‎ ‎`Penis`‏‏‎ ‎`Roast`‏‏‎ ‎`Status`‏‏‎ ‎`Bio`‏‏‎ ‎`Dad`‏‏‎ ‎`GirlFriends`‏‏‎ ‎`Compliment`‏‏‎ ‎`Kill`‏‏‎ ‎`Kiss`‏‏‎ ‎`Friend`‏‏‎‏‏‎ ‎`Retard` ‎`Human` ‎`Simp` ‎`Waifu` ‎`PunchMachine` ‎`Joke` ‎`Fight` `Fly` `Parent` `Urban_Dictionary` `WhatsTheWeather` `Pussy` `Stabrate` `Begrate` `Facts` `Slots` `Beer`')
            e.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=e)
        elif x == 'image':
            embed = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            embed.add_field(name="**Image Help:**\n**Remember to use - before all commands**", value='`Memes` `Trash` `Slap` `Spank` `Obese` `Simulate`')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)
        elif x == 'motivation':
            embed = discord.Embed(
                title='**Motivation Help**',
                Color=discord.Color.teal()
            )
            embed.add_field(name='**Commands:**\n**Remember to use - before all commands**',
                            value='`Quote`‏‏‎ ‎`ImgQuote`‏‏‎ ‎`Speech`‏‏‎ ‎`GreatSpeech` `Art`')
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)
        elif x == 'invite':
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
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)
        elif x == 'aliases':
            embed = discord.Embed(
                title='**Aliases:**',
                color=discord.Color.teal()
            )
            embed.add_field(name='__**Moderation:**__',
                            value='`Mod` `Moderation` `Fun` `Image` `Images` `Motiv` `Motivation` `Inv` `Aliases` `User` `Stats` `UserInfo` `Av` `Action`\n\n__**Images:**__\n`Meme` `Vid` `Video`\n\n__**Fun:**__\n`Latency` `MagicK` `KMagic` `MK`‏‏‎ ‎‎`Comp` ‎`Punch` `UD` `WTW` `Weather` `W` `Stab` `Beg` `Facts` `PP` `Insult` `Murder` `GF` `Gender` `Slots` `Bet`\n\n__**Motivation:**__\n`Quotes` `VQ` `ImgQ` `Speeches` `GreatSpeech` `GSpeech` `GS` `IQuote` `Arts` `MP` `Masterpiece` `Masterpieces`\n\n__**Games:**__\n`Coming Soon`\n\n__**Quizzes:**__\n`Coming Soon`\n\n__**Management:**__\n`Doesnt need any :P (Yet)`')
            embed.set_footer(
                text='All commands are no longer case sensitive :P\nThere are also hidden commands. Find them all!')
            await ctx.send(embed=embed)
        elif x == 'games':
            embed = discord.Embed(
                title='**Games**',
                color=discord.Color.red()
            )
            embed.add_field(name='**Current Games:**', value='`RPS` `Decipher` `roll` ``')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(
                title='Mistake?',
                color=discord.Color.red(),
                description=f'The help command you typed may not exist to it is coming soon!\n\nYou may have also mistyped the command. The help command has changed from `Help{option}` to `Help {option}`.'
            )
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)

    # Little bit of banter
    @commands.command()
    @cooldown(1, 2, BucketType.user)
    async def status(self, ctx):
        await ctx.send('Are you blind. Click my profile for the love of god')
        
# Bot setup
def setup(bot):
    bot.add_cog(Help(bot))
