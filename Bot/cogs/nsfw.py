import discord
from discord.ext import commands
from Utils import API as api
from Utils.API import NSFW as nsfw
import random
import asyncio
import time
from Utils import __logging__

'''
Version Info:
    Intergrated the API into the bot
    Attempted to make the API async didnt go well
    Brought it up to current version of 1.4.2
    Custom Handling
    Doesnt work on sometimes as gifv isnt supported
    
Improvements:
    Faster Response
    Library is updated everyday
    Members can contribute to the library
    
Disadvantages:
    Less Reliable
    May Crash
    Need to intergrate caching to prevent API timing out
    
Version Info:
    Added Caching
'''

## NSFW bot developed by 1 retard and 2 geniuses
## Thanks Mark and Joe gl with your degrees

def cache_(reg : __logging__.col, **kwargs):
    y = reg.load_col()
    if y:
        raise AttributeError('Column is already in use')
    reg.update(
        **kwargs
    )
    return True

def load_(reg : __logging__.col):
    return reg.load_col()

class nsfw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reload_content.add_exception_type(__logging__.RequestTimeoutError)
        self.reload_content.start()

    @tasks.loop(minutes=60.0)
    async def batch_update(self):
        await __logging__.conv
        async with __logging__.dumps('NSFW') as cxn:
            key = __logging__.CALC(cxn)['API_KEY']
            
            __logging__.update_cache('NSFW', others = {
                "APIKEY": key,
                "TYPE": 'Blob'
            })
        
    @commands.command()
    @commands.is_nsfw()
    async def MILF(self, ctx):
        embed = discord.Embed(
            title='MILF Topic',
            color=discord.Color.red()
        )
        embed.set_image(url=f'{api(nsfw.milf)}')
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_nsfw()
    async def Pussy(self, ctx):
        embed = discord.Embed(
            title='Wet or Dry?',
            color=discord.Color.red()
        )
        embed.set_image(url=api(nsfw.pussy))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_nsfw()
    async def Teen(self, ctx):
        embed = discord.Embed(
            title='You like them small?',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.teen))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_nsfw()
    async def Spreading(self, ctx):
        embed = discord.Embed(
            title='Speechless',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.spreading))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_nsfw()
    async def Ass(self, ctx):
        embed = discord.Embed(
            title='Drums!',
            color=discord.Color.red()
        )
        embed.set_image(url=api(nsfw.ass))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_nsfw()
    async def creampie(self, ctx):
        embed = discord.Embed(
            title='Drench them white.',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.creampie))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_nsfw()
    async def Fisting(self, ctx):
        embed = discord.Embed(
            title='Doesnt that hurt?',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.fisting))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command()
    @commands.is_nsfw()
    async def Closeup(self, ctx):
        embed = discord.Embed(
            title='Got that good `V` Shape.',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.closeup))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['BJ'])
    @commands.is_nsfw()
    async def Blowjob(self, ctx):
        embed = discord.Embed(
            title='Tingling goodness. Bet your a girl!',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.bj))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['FS'])
    @commands.is_nsfw()
    async def FaceSitting(self, ctx):
        embed = discord.Embed(
            title='Can they breathe?',
            color=discord.Color.red()
            )
        embed.set_image(url=api(nsfw.facesitting))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['gif'])
    @commands.is_nsfw()
    async def porn(self, ctx):
        embed = discord.Embed(
            title='Live Action.',
            color=discord.Color.red()
            )
        y = api(nsfw.animated)
        embed.set_image(url=y)
        if not y in load_():
            cache_('NSFW_TABLE/animated')
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)
        
    @commands.command(alises=['tits', 'titties', 'tit', 'boob'])
    @commands.is_nsfw()
    async def boobs(self, ctx):
        embed = discord.Embed(
            title='Bouncing!',
            color=discord.Color.purple()
        )
        embed.set_image(url=api(nsfw.tits))
        embed.set_footer(text='From a weird source')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(nsfw(bot))
