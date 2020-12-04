import discord
import asyncio
from discord.ext import commands
from asyncio import sleep
import traceback
import string, random

errors = ('ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError',
          'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError',
          'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError',
          'EnvironmentError', 'FileExistsError', 'FileNotFoundError','FloatingPointError', 'FutureWarning',
          'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning',
          'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError',
          'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError',
          'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError',
          'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError',
          'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration',
          'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError',
          'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError',
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
    chars = list(string.ascii_lowercase)
    num = list(string.digits) + list(string.hexdigits) + list(string.octdigits)
    former = []
    for i in range(random.randint(10, 20)):
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
        self.logging = __logging__

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            pass
        elif isinstance(error, commands.CommandOnCooldown):
            global time, message
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
            await ctx.send(message)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send('**You have made an error.**\n\n{}'.format(error.param))
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send('You have given too many args.\nPlease use the command as directed.')
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send('I am missing permissions.')
        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            await ctx.send('The cog {} is already loaded.'.format(error.args[0]))
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send('You need **{}** perms to complete this actions.'.format(' '.join(error.missing_perms[0].split('_'))))
        elif isinstance(error, commands.BotMissingAnyRole):
            await ctx.send('**Woops!**\n\nLooks like i am missing the {} role.'.format(error.missing_role))
        elif isinstance(error, commands.CheckAnyFailure):
            await ctx.send('An unknown error has occured.')
        elif isinstance(error, commands.errors.NSFWChannelRequired):
            await ctx.send('You must use this command in a channel marked as **NSFW**.')
        elif isinstance(error, commands.errors.NotOwner):
            await ctx.send('Only **_-*™#1234** can use this command.')
        elif isinstance(error, commands.errors.NoPrivateMessage):
            await ctx.send("The user has blocked me or has the DM's closed.")
        elif isinstance(error, discord.ext.commands.DisabledCommand):
            await ctx.send('This command is disabled.')
        elif isinstance(error, discord.errors.Forbidden):
            await ctx.send('I do not have permissions for this command!')
        elif isinstance(error, commands.errors.MemberNotFound):
            await ctx.send('Please give a valid user!')
        else:
            try:
                code = gen_code()
                error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
                channel = self.bot.get_channel(779051230373740546)
                await channel.send('**Error in the command {}**\n```\n'.format(ctx.command.name) + ''.join(map(str, error)) + '\n```')
                await ctx.send('**An unknown error has occurred. It has been reported automatically!**\n**Your error code:** `{}`'.format(code))
                errortype = 'Unspecified'
                for i in range(len(error)):
                    for j in errors:
                        if j in error[i]:
                            errortype = j
                            break
                data = self.logging.get('error_code.log', 'msfw').json()
                data[code] = {}
                data[code]['Command'] = ctx.command.name.title()
                data[code]['Error Type'] = errortype
                data[code]['Shortened Error'] = error[-1][:-1]
                self.logging.update(data)
            except discord.errors.HTTPException:
                print(error)

def setup(bot):
    bot.add_cog(Events(bot))
