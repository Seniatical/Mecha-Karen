import discord
import asyncio
from discord.ext import commands
from asyncio import sleep
import traceback
import string
import random
import json
from utility import emojis as emoji
from utility import errors
import hashlib
from inspect import Parameter
import io
import textwrap

_errors = ('ArithmeticError', 'AssertionError', 'BaseException', 'BlockingIOError',
           'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
           'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
           'EnvironmentError', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning',
           'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'UnexpectedQuoteError',
           'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
           'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError',
           'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
           'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError',
           'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
           'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
           'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
           'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning',
           'WindowsError', 'ZeroDivisionError')


async def convert(time):
    days = time // (24 * 3600)
    time = time % (24 * 3600)
    hours = time // 3600
    time %= 3600
    minutes = time // 60
    time %= 60
    seconds = time
    if days:
        if hours:
            return f'**{days}** Days and **{hours}** Hours.'
        if minutes:
            return f'**{days}** Days and **{minutes}** Minutes.'
        return f'**{days}** Days.'
    if hours:
        if minutes:
            return f'**{hours}** Hours and **{minutes}** Minutes.'
        return f'**{hours}** Hours and **{seconds}** Seconds.'
    if minutes:
        if seconds:
            return f'**{minutes}** Minutes and **{seconds}** Seconds.'
        return f'**{minutes}** Minutes.'
    return f'**{seconds}** Seconds.'


async def gen_code(name: str):
    return hashlib.sha256(name.encode('ascii', errors='ignore')).hexdigest()


class ErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandOnCooldown):
            time = error.retry_after
            time = await convert(round(time))
            message = f'The command **{ctx.command.name}** is on cooldown for {time}'
            return await ctx.message.reply(content=message)

        elif isinstance(error, discord.ext.commands.DisabledCommand):
            if not ctx.command.enabled:
                return await ctx.message.reply(embed=discord.Embed(
                    description='<a:nope:787764352387776523> This command has been disabled by one of our owners - Most likely due to a bug.',
                    colour=discord.Colour.red()
                ), mention_author=False)

            return await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> This command has been disabled. Re-enable it use it again!',
                colour=discord.Colour.red()
            ), mention_author=False)

        elif isinstance(error, commands.MissingRequiredArgument):
            ctx.command.reset_cooldown(ctx)
            prefix_ = ctx.prefix if not ctx.prefix == f'<@!{ctx.bot.user.id}>' else '-'

            params = [ctx.command.clean_params[i] for i in ctx.command.clean_params]
            listed_message = ['```{}{} '.format(prefix_, ctx.command.name), '```']
            for param in params:
                if param.default == Parameter.empty:
                    listed_message.insert(-1, '<' + param.name + '> ')
                else:
                    listed_message.insert(-1, '[' + param.name + '={}] '.format(param.default))

            listed_message.insert(-1, '\n' + error.args[0])

            missing = error.param
            try:
                index = listed_message.index('<' + missing.name + '> ', 0)
            except ValueError:
                index = listed_message.index('[' + missing.name + '] ', 0)

            listed_message.insert(-2, '\n')
            for i in range(index):
                listed_message.insert(-2, (' ' * (len(listed_message[index - 1]) - 3)))
            listed_message.insert(-2, '^' * len('<' + missing.name + '>'))

            await ctx.send(''.join(listed_message))

        elif isinstance(error, commands.MissingPermissions):
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> You need **{}** perms to complete this actions.'.format(
                    ' '.join(error.missing_perms[0].split('_'))),
                colour=discord.Colour.red()
            ), mention_author=False)

        elif isinstance(error, commands.BotMissingPermissions):
            if error.missing_perms[0] == 'send_messages':
                return
            await ctx.message.reply(
                embed=discord.Embed(
                    description='<a:nope:787764352387776523> I am missing **{}** permissions.'.format(
                        ' '.join(error.missing_perms[0].split('_'))),
                    colour=discord.Colour.red()
                ), mention_author=False)

        elif isinstance(error, commands.errors.NSFWChannelRequired):
            embed = discord.Embed(
                title='Error 404!',
                colour=discord.Color.red(),
                description="You must use this command in a channel marked as **NSFW**.",
                timestamp=ctx.message.created_at,
            ).set_footer(text='Invoked by {}'.format(ctx.author), icon_url=ctx.author.avatar)
            embed.set_image(url='https://i.imgur.com/cy9t3XN.gif')
            await ctx.message.reply(embed=embed)

        elif isinstance(error, commands.errors.NotOwner):
            await ctx.message.reply('Only **_-*™#1234** can use this command.', mention_author=False)

        elif isinstance(error, errors.Blacklisted):
            try:
                await ctx.author.send(embed=discord.Embed(
                    description='You have been blacklisted from using Mecha Karen!',
                    colour=discord.Colour.red()
                ))
            except discord.error.Forbidden:
                return

        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.message.reply(embed=discord.Embed(
                description="{} Member named **{}** was not found!".format(emoji.KAREN_ADDITIONS_ANIMATED['nope'],
                                                                           error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.UserNotFound):
            await ctx.message.reply(embed=discord.Embed(
                description="{} Member named **{}** was not found!".format(emoji.KAREN_ADDITIONS_ANIMATED['nope'],
                                                                           error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, errors.NotGuildOwner):
            await ctx.message.reply(embed=discord.Embed(
                description="{} Only **{}** has access to this command!".format(emoji.KAREN_ADDITIONS_ANIMATED['nope'],
                                                                                ctx.guild.owner),
                colour=discord.Colour.red()
            ), mention_author=False)
            ctx.command.reset_cooldown(ctx)

        elif isinstance(error, commands.errors.ChannelNotFound):
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Channel named **{}** cannot be found! Retry with a valid channel.'.format(
                    error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)

        elif isinstance(error, commands.errors.RoleNotFound):
            ctx.command.reset_cooldown(ctx)
            await ctx.message.reply(embed=discord.Embed(
                description='<a:nope:787764352387776523> Role named **{}** cannot be found!'.format(error.argument),
                colour=discord.Colour.red()
            ), mention_author=False)

        else:
            if ctx.command.name.lower() == 'eval_fn':
                return

            code = await gen_code(ctx.command.name.lower())
            error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
            error = ''.join(error)

            if error.endswith('Missing Permissions'):
                try:
                    return await ctx.send(
                        'I am missing permissions inorder to run this command. I cannot identify the correct one.')
                except discord.errors.Forbidden:
                    return

            channel = self.bot.get_channel(800315954008948747)
            try:
                await channel.send(
                    '**Error in the command {}**, Located from `{}` by user `{}`\n```\n'.format(ctx.command.name,
                                                                                                ctx.guild.name,
                                                                                                ctx.author) + error + '\n```')
            except Exception:
                await channel.send(
                    content='**Error in the command {}**, Located from `{}` by user `{}`'.format(ctx.command.name,
                                                                                                 ctx.guild.name,
                                                                                                 ctx.author),
                    file=discord.File(fp=io.BytesIO(error.encode(errors='ignore')), filename='error.log')
                )

            try:
                await ctx.send(
                    '**An unknown error has occurred. It has been reported automatically!**\n**Your error code:** `{}`'.format(
                        code))
            except discord.errors.Forbidden:
                pass


def setup(bot):
    bot.add_cog(ErrorHandler(bot))
