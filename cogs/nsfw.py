import discord
from discord.ext import commands
from Others import Stuff
import random
import asyncio
import time

class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_nsfw()
    async def MILF(self, ctx):
        embed = discord.Embed(
            title='MILF Topic',
            color=discord.Color.red()
        )
        embed.set_image(url=f'{random.choice(Stuff.MILF)}')
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command()
    @commands.is_nsfw()
    async def Pussy(self, ctx):
        embed = discord.Embed(
            title='Wet or Dry?',
            color=discord.Color.red()
        )
        embed.set_image(url=random.choice(Stuff.Pussy))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def Teen(self, ctx):
        embed = discord.Embed(
            title='You like them small?',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.Teen))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command()
    @commands.is_nsfw()
    async def Spreading(self, ctx):
        embed = discord.Embed(
            title='Speechless',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.Spreading))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command()
    @commands.is_nsfw()
    async def Ass(self, ctx):
        embed = discord.Embed(
            title='Drums!',
            color=discord.Color.red()
        )
        embed.set_image(url=random.choice(Stuff.Ass))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command()
    @commands.is_nsfw()
    async def Facial(self, ctx):
        embed = discord.Embed(
            title='Drench them white.',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.Facial))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command()
    @commands.is_nsfw()
    async def Fisting(self, ctx):
        embed = discord.Embed(
            title='Doesnt that hurt?',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.Fisting))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command()
    @commands.is_nsfw()
    async def Closeup(self, ctx):
        embed = discord.Embed(
            title='Got that good `V` Shape.',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.Closeup))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command(aliases=['BJ'])
    @commands.is_nsfw()
    async def Blowjob(self, ctx):
        embed = discord.Embed(
            title='Tingling goodness. Bet your a girl!',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.BlowJob))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command(aliases=['FS'])
    @commands.is_nsfw()
    async def FaceSitting(self, ctx):
        embed = discord.Embed(
            title='Can they breathe?',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.FaceSitting))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command(aliases=['gif'])
    @commands.is_nsfw()
    async def Gifs(self, ctx):
        embed = discord.Embed(
            title='Live Action.',
            color=discord.Color.red()
            )
        embed.set_image(url=random.choice(Stuff.Gifs))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
    @commands.command(alises=['tits', 'titties', 'tit', 'boob'])
    @commands.is_nsfw()
    async def boobs(self, ctx):
        embed = discord.Embed(
            title='Bouncing!',
            color=discord.Color.purple()
        )
        embed.set_image(url=random.choice(Stuff.Boobs))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(nsfw(bot))
