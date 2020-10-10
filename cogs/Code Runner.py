import discord
from discord.ext import commands
import contextlib
import sys
import io
import venv

class run(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def run(self,ctx,*,code:str=None):
        if code == None:
            await ctx.send('> You cannot run nothing')
        if 'while' in code:
            await ctx.send('> You cannot use **`while`**!')
        elif 'for' in code:
            await ctx.send('> You cannot use **`for`**!')
        elif 'import' in code:
            await ctx.send('> You cannot use **`import`**!')
        elif 'os' in code:
            await ctx.send('> You cannot use **`OS`**!')
        elif 'system' in code:
            await ctx.send('> You cannot use **`System`**!')
        elif 'sys' in code:
            await ctx.send('> You cannot use **`Sys`**!')
        elif 'eval' in code:
            await ctx.send('> You cannot use **`Eval`**!')
        elif 'exec' in code:
            await ctx.send('> You cannot use **`Exec`**!')
        elif 'exit' in code:
            await ctx.send('> You cannot use **`Exit`**!')
        elif 'io' in code:
            await ctx.send('> You cannot use **`Io`**!')
        elif 'contextlib' in code:
            await ctx.send('> You cannot use **`Contextlib`**!')
        elif 'input' in code:
            await ctx.send('> You cannot use **`Input`**!')
        elif '@' in code:
            await ctx.send('> You cannot use **`@`**!\n> This is because it can be destructive.')
        elif 'disable' in code:
            await ctx.send('> You cannot use **`Disable`**')
        elif 'quit' in code:
            await ctx.send('> You cannot use **`Quit`**')
        elif 'raise' in code:
            await ctx.send('> You cannot use **`Raise`**')
        elif 'crash' in code:
            await ctx.send('> You cannot use **`Crash`**')
        elif 'del' in code:
            await ctx.send('> You cannot use **`Del`**')
        else:
            try:
                if code.startswith('py') and code.endswith(''):
                    code = code[5:-3]
                elif code.startswith('`') and code.endswith('`'):
                    code = code[1:-1]
                elif code.startswith('```') and code.endswith('```'):
                    code = code[3:-3]
                @contextlib.contextmanager
                def evaluate(stdout = None):
                    old = sys.stdout
                    if stdout == None:
                        sys.stdout = io.StringIO()
                    yield sys.stdout
                    sys.stdout = old

                with evaluate() as e:
                    exec(code, {})
                msg = await ctx.send('Evaluating...')
                await msg.delete()
                await ctx.send(f"{ctx.author.mention} Finished Evaluating!")
                await ctx.send(f'```py\n{e.getvalue()}```')
            except Exception as e:
                await ctx.send(f'**Sorry but we ran into an error!**\n\n> {e}')



def setup(bot):
    bot.add_cog(run(bot))
