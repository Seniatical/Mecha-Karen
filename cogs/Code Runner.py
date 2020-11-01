import discord
from discord.ext import commands
import contextlib
import sys
import io

class run(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.nono = ['while', 'for', 'None', 'import', 'os', 'system', 'sys', 'eval', 'exec', 'exit', 'io', 'contextlib', 'input', '@', 'disable', 'quit', 'raise', 'crash', 'del']
        
    @commands.command()
    async def run(self,ctx,*,code:str=None):
        if self.nono in code:
            await ctx.send('There is a forbidden keyword in your code. Process Cancelled.')
            return
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
