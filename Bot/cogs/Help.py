import discord
from discord.ext import commands
from datetime import timedelta
from discord.ext.commands import BucketType, cooldown

import time
import asyncio

from Utils.main import GET_OWNER
from Utils.main import get_prefix

index = 0

class Help(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.index = index

    @commands.command()
    async def Help(self, ctx, option=None):
        prefix = get_prefix(self.bot, ctx.message)
        if option == None:
            pass
        else:
            x = option.lower()
        if option == None:
            e = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            e.add_field(name=':scales: **Moderation**‎‏‏‎‎', value='`{}Help Mod`'.format(prefix))
            e.add_field(name=':jigsaw: **Fun**', value='`{}Help Fun`'.format(prefix))
            e.add_field(name=':v: **Motivation**', value='`{}Help Motivation`'.format(prefix))
            e.add_field(name=':camera: **Images**', value='`{}Help Images`'.format(prefix))
            e.add_field(name=':bowling: **Games**', value='`{}Help Games`'.format(prefix))
            e.add_field(name=':wrench: **Management**', value='`{}Help Manage`'.format(prefix))
            e.add_field(name='<a:finger_hole:744627487027494984> NSFW‏‏‎‎', value='`{}Help NSFW`'.format(prefix))
            e.add_field(name='‏', value=f'‏Join our [support server](https://discord.gg/Q5mFhUM) | Invite [Mecha Karen](https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)', inline=False)
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.set_footer(text='Use command {}Invite to invite the Bot or {}Source to view the source code!'.format(prefix, prefix),
                icon_url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            await ctx.send(embed=e)

        elif x == 'mod' or x == 'moderation':
            e = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            e.add_field(name="**Mod Help:**",
                        value='`Ban` `Kick` `Clear` `Unban` `Nuke` `WhoIs` `Server` `Avatar` `Mute` `Actions` `History` `Nickname` `Members` `Slowmode` `Lock`')
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
            e.add_field(name="**Fun Help:**",
                        value='`Ping`‏‏‎ ‎`MagicKaren`‏‏‎ ‎`Gay`‏‏‎ ‎`IQ`‏‏‎ ‎`Penis`‏‏‎ ‎`Roast`‏‏‎ ‎`Status`‏‏‎ ‎`Dad` ‎`Kill`‏‏‎ ‎`Retard` ‎`Human` ‎`Simp` ‎`Waifu` ‎`PunchMachine` ‎`Joke` `Fly` `Parent` `Wobbler` `Stabrate` `Begrate` `Facts` `Slots` `Beer` `Useless` `LifeExpectancy` `BWeight` `WeighIn` `Reverse` `Time` `Date` `F` `Weather` `Say` `Annoy`')
            e.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=e)

        elif x == 'image' or x == 'images' or x == 'img':
            embed = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            embed.add_field(name="**Image Help:**", value='`Memes` `Trash` `Slap` `Spank` `Obese` `BreakingBad` `Reddit` `Bird` `HighFive` `Delete`')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)

        elif x == 'motivation' or x == 'motiv':
            embed = discord.Embed(
                title='**Motivation Help**',
                Color=discord.Color.teal()
            )
            embed.add_field(name='**Commands:**',
                                value='`Quote`‏‏‎ ‎`ImgQuote`‏‏‎ ‎`Speech`‏‏‎ ‎`GreatSpeech`')
            embed.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)

        elif x == 'games' or x == 'game':
            embed = discord.Embed(
                title='**Games**',
                color=discord.Color.red()
            )
            embed.add_field(name='**Current Games:**', value='`RPS` `Decipher` `Roll` `Maths` `Flip`')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)

        elif x == 'manage' or x == 'mng' or x == 'manage':
            embed = discord.Embed(
                title='**Management**',
                color=discord.Color.red()
            )
            embed.add_field(name='**Management:**',
                            value='`Enable` **Makes a disabled cog enabled again.**\n`Disable` **Makes a running cog disabled. (Unusable) **\n`Refresh` **Reloads a running cog.**\n`Remove` **Disables a command. Which stops it from being used.**\n`Allow` **Makes a disabled command usable again.**\n`Sync` **Reloads the entire bot. Can only be used by {}**.\n`Cogs` **Allows you to see all the current cogs.**\n`Uptime` **How long has karen been up for.**'.format(ctx.guild.owner))
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)

        elif x == 'nsfw':
            if ctx.channel.is_nsfw() == False:
                await ctx.send('Please use this command in a channel marked with **NSFW**. This due to the naming of commands being graphic.')
                return
            embed = discord.Embed(
                title='NSFW Commands',
                color=discord.Color.purple()
            )
            embed.set_thumbnail(url='http://avoiderdragon.com/wp-content/uploads/2016/02/thumbnail_vr-porn.jpg')
            embed.add_field(name='‏‏‎ ‎', value='`MILF` `Pussy` `Teen` `Spreading` `Ass` `Facial` `Fisting` `CloseUp` `BlowJob` `FaceSitting` `Gifs` `Boobs`')
            embed.set_footer(
                icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
                text='Bot created by _-*™#7139')
            await ctx.send(embed=embed)

        else:
            e = discord.Embed(title="", description="__**Mecha Karen Support**__", color=0x50C878)
            e.add_field(name=':scales: **Moderation**‎‏‏‎‎', value='`-Help Mod`')
            e.add_field(name=':jigsaw: **Fun**', value='`-Help Fun`')
            e.add_field(name=':v: **Motivation**', value='`-Help Motivation`')
            e.add_field(name=':camera: **Images**', value='`-Help Images`')
            e.add_field(name=':wrench: **Management**', value='`-Help Manage`')
            e.add_field(name=':bowling: **Games**', value='`-Help Games`')
            e.add_field(name='<a:finger_hole:744627487027494984> NSFW‏‏‎‎', value='`-Help NSFW`')
            e.add_field(name=f'‏‏‎ ‎‎', 
            value=f'‏Join our [support server](https://discord.gg/Q5mFhUM) | Invite [Mecha Karen](https://discord.com/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)‎', inline=False)
            e.set_thumbnail(
                url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            e.set_footer(text='Use command -Invite to invite the Bot or -Source to view the source code!',
                        icon_url='https://cdn.discordapp.com/avatars/740514706858442792/3d4c161d2bfa97ec86cc82102df5cad5.webp?size=256')
            await ctx.send(embed=e)
        
    @commands.command()
    @cooldown(1, 10, BucketType.user)
    async def status(self, ctx):
        await ctx.send('Are you blind. Click my profile for the love of god')

    @commands.command(aliases=['inv'])
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
            icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
            text='Bot created by _-*™#7139')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 30, BucketType.guild)
    async def source(self, ctx):
        embed = discord.Embed(
            title='**Source Code**',
            color=discord.Color.red()
        )
        embed.add_field(name='**The source code may or may not be updated to the latest version!**', value='[Click here to view the source code](https://github.com/Seniatical/Mecha-Karen-Source-Code)')
        embed.set_footer(
            icon_url='https://cdn.discordapp.com/avatars/475357293949485076/a0c190d9ffeea49f85d5468f9501b507.webp?size=256',
            text='Bot created by _-*™#7139')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
