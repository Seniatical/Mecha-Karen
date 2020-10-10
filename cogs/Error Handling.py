import traceback
import discord
import asyncio
from discord.ext import commands
from Others import Channel
import test
from asyncio import sleep

def convert(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%d:%d:%d:%d" % (day, hour, minutes, seconds)

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            global time
            if isinstance(error, commands.CommandNotFound):
                pass
            if isinstance(error, commands.CommandOnCooldown):
                time = error.retry_after
                time = convert(time)
                x = time.split(':')
                if x[1] != '0' and x[2] != '0':
                    if x[1] == 1:
                        message = f'Retry this command after **{x[1]}** hour and **{x[2]}** minutes!'
                    else:
                        message = f'Retry this command after **{x[1]}** hours and **{x[2]}** minutes!'
                elif x[1] == '0' and x[2] != '0' and x[3] != '0':
                    message = f'Retry this command after **{x[2]}** minutes and **{x[3]}** seconds!'
                elif x[3] != '0' and x[1] == '0' and x[2] == '0':
                    message = f'Retry this command after **{x[3]}** seconds!'
                msg = await ctx.send(message)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.MissingRequiredArgument):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='You need to finish the command off!', value=f'You cant just give half a command!\n\n`{error.args[0]}`')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.TooManyArguments):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='What are you attempting?', value='That command doesnt take that many options!')
                await ctx.send(embed=embed)
            if isinstance(error, commands.BotMissingPermissions):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='I dont have them permissions!', value=f'{ctx.author.mention} i do not have access to them permissions. Sorry!')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.ExtensionAlreadyLoaded):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='The Cog is already loaded!', value=f'The cog {error.args[0]} isnt disabled!')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.MissingPermissions):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='You dont have the correct roles', value=f'Dear {ctx.author.mention} you do not have {error.args[0]}')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.BotMissingAnyRole):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='Oopsie!', value='Im missing roles.')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.CheckAnyFailure):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='Error', value='There was an error somewhere!')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.errors.NSFWChannelRequired):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.set_thumbnail(url='https://rlv.zcache.com/return_to_sender_wrong_address_rubber_stamp-rabe45bc54d524b0ca9b150ee9d222490_6o1xx_540.jpg?rlvnet=1')
                embed.add_field(name='NOPE', value='This command must be used in a `NSFW` channel since this command is explicit!')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.errors.NotOwner):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='Not your house!', value='Your not the owner. Retarded yute.')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.errors.NoPrivateMessage):
                embed = discord.Embed(
                    title='❌ Error ❌',
                    color=discord.Color.dark_red()
                )
                embed.add_field(name='User isnt accepting any messages', value=f'The user you just tried to send a message to has either blocked me :(. Or are not accepting any messages')
                msg = await ctx.send(embed=embed)
                await sleep(3)
                await msg.delete()
            if isinstance(error, commands.errors.BotMissingPermissions):
                msg = await ctx.send('Sorry, I do not have `{}` permissions!'.format(error.missing_perms))
            print(error)
        except Exception:
            pass

def setup(bot):
    bot.add_cog(Events(bot))
