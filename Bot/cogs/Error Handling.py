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
import asyncio
from discord.ext import commands
from asyncio import sleep
import traceback
import string
import random
import prawcore
from Helpers import emoji, functions
from cogs.Help import get_prefix

errors = ('ArithmeticError', 'AssertionError', 'BaseException', 'BlockingIOError',
          'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
          'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
          'EnvironmentError', 'FileExistsError', 'FileNotFoundError','FloatingPointError', 'FutureWarning',
          'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'UnexpectedQuoteError',
          'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
          'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError',
          'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
          'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError',
          'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
          'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
          'TimeoutError', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
          'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning',
          'WindowsError', 'ZeroDivisionError')

def convert(time):
    day = time // (24 * 3600)
    time = time % (24 * 3600)
    hour = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    return "%d:%d:%d:%d" % (day, hour, minutes, seconds)

def gen_code():
    chars = list(string.hexdigits) + list(string.octdigits)
    num = list(string.digits) + list(string.hexdigits) + list(string.octdigits)
    former = []
    for i in range(random.randint(20, 30)):
        x = ('y', 'n')
        if random.choice(x) == 'y':
            if random.choice(x) == 'y':
                former.append(random.choice(chars).lower())
            else:
                former.append(random.choice(chars).upper())
        else:
            former.append(random.choice(num))
    return ''.join(map(str, former))

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            time = error.retry_after
            time = convert(time)
            x = time.split(':')
            message = '**Your On Cooldown!**'
            if x[1] != '0':
                if x[1] == 1:
                    message = 'The command **{}** is still on cooldown! Retry after **1** Hour and **{}** Minutes'.format(ctx.command.name.title(), x[2])
                else:
                    message = 'The command **{}** is still on cooldown! Retry after **{}** Hour and **{}** Minutes'.format(ctx.command.name.title(), x[1], x[2])
            elif x[1] == '0' and x[2] != '0':
                if x[2] == '1':
                    message = 'The command **{}** is still on cooldown! Retry after **1** Minute and **{}** Seconds.'.format(ctx.command.name.title(), x[3])
                else:
                    message = 'The command **{}** is still on cooldown! Retry after **{}** Minutes and **{}** Seconds.'.format(ctx.command.name, x[2], x[3])
            elif x[1] == '0' and x[2] == '0' and x[3] != '0':
                message = 'The command **{}** is still on cooldown! Retry after **{}** Seconds.'.format(ctx.command.name.title(), x[3])
            else:
                message = 'The command **{}** is still on cooldown! Retry after **1** Seconds.'
            await ctx.message.reply(message, mention_author=False)

        elif isinstance(error, commands.MissingRequiredArgument):
            prefix_ = get_prefix(ctx.guild.id)
            params = [ctx.command.clean_params[i] for i in ctx.command.clean_params]
            y = ['```{}{} '.format(prefix_, ctx.command.name), '```']
            for i in params:
                y.insert(-1, '<' + i.name + '> ')
            y.insert(-1, '\n\n' + error.args[0])
            await ctx.send(''.join(y))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> You need **{}** perms to complete this actions.'.format(' '.join(error.missing_perms[0].split('_'))),
                colour=discord.Colour.red()
            ), mention_author=False)

        elif isinstance(error, commands.BotMissingPermissions):
            if error.missing_perms[0] == 'send_messages':
                return
            await ctx.message.reply(
                embed=discord.Embed(
                    description='<a:nope:787764352387776523> I am missing **{}** permissions.'.format(' '.join(error.missing_perms[0].split('_'))),
                    colour=discord.Colour.red()
                ), mention_author=False)

        elif isinstance(error, commands.errors.NSFWChannelRequired):
            embed = discord.Embed(
                title='Error 404!',
                colour=discord.Color.red(),
                description="You must use this command in a channel marked as **NSFW**.",
                timestamp=ctx.message.created_at,
            ).set_footer(text='Invoked by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
            embed.set_image(url='https://i.imgur.com/cy9t3XN.gif')
            await ctx.message.reply(embed=embed)

        elif isinstance(error, commands.errors.NotOwner):
            await ctx.message.reply('Only **_-*™#1234** can use this command.', mention_author=False)

        elif isinstance(error, discord.ext.commands.DisabledCommand):
            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> This command has been disabled. Re-enable it use it again!',
                colour=discord.Colour.red()
            ), mention_author=False)

        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.message.reply(embed=discord.Embed(
                description="{} Member named **{}** was not found!".format(emoji.KAREN_ADDITIONS_ANIMATED['nope'], error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.UserNotFound):
            await ctx.message.reply(embed=discord.Embed(
                description="{} Member named **{}** was not found!".format(emoji.KAREN_ADDITIONS_ANIMATED['nope'], error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, prawcore.NotFound):
            return await ctx.send('Post Not Found!\nError 404: Give a subreddit with posts.')

        elif isinstance(error, functions.NotGuildOwner):
            await ctx.message.reply(embed=discord.Embed(
                description="{} Only **{}** has access to this command!".format(emoji.KAREN_ADDITIONS_ANIMATED['nope'], ctx.guild.owner),
                colour=discord.Colour.red()
            ), mention_author=False)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.ChannelNotFound):
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Channel named **{}** cannot be found! Retry with a valid channel.'.format(error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)

        elif isinstance(error, commands.errors.RoleNotFound):
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Role named **{}** cannot be found!'.format(error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)

        else:
            code = gen_code()
            error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
            channel = self.bot.get_channel(800315954008948747)
            try:
                await channel.send('**Error in the command {}**\n```\n'.format(ctx.command.name) + ''.join(map(str, error)) + '\n```')
            except discord.errors.HTTPException:
                with open('./Helpers/error.txt', 'w') as f:
                    f.writelines(error)
                    await channel.send('Error code in ./Bot/Helpers/error.txt')
            try:
                await ctx.send('**An unknown error has occurred. It has been reported automatically!**\n**Your error code:** `{}`'.format(code))
            except discord.errors.Forbidden:
                pass
            error_type = 'Unspecified'
            for i in range(len(error)):
                for j in errors:
                    if j in error[i]:
                        error_type = j
                        break
            data = self.bot.logging.load('errors.log')
            data = data.json()
            data[code] = {}
            data[code]['Command'] = ctx.command.name.title()
            data[code]['Error Type'] = error_type
            data[code]['Shortened Error'] = error[-1][:-1]
            self.bot.logging.update('errors.log', mode='logs', cm='json')

def setup(bot):
    bot.add_cog(Events(bot))
