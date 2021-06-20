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

import binascii
import os
import typing
import time
import discord
import asyncio
from discord.ext import commands, tasks
import ast
import traceback

def insert_returns(body):
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)

class Eval(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def eval_fn(self, ctx, *, cmd):
        if ctx.author.id not in [491630879085559808, 475357293949485076]:
            return await ctx.send('You do not own me.')
        start = time.perf_counter()
        fn_name = "KarenEvalBody"
        cmd = cmd.strip("` ")
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
        body = f"async def {fn_name}():\n{cmd}"
        parsed = ast.parse(body)
        body = parsed.body[0].body
        insert_returns(body)
        env = {
            'api_token': self.bot.env('API_TOKEN'),
            'self': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            'os': os,
            'time': time,
            '__import__': __import__
        }

        async def eval_worker():
            exec(compile(parsed, filename="<ast>", mode="exec"), env)
            result = (await eval(f"{fn_name}()", env))
            end = time.perf_counter()
            return [result, end]
        task: asyncio.Task = self.bot.loop.create_task(eval_worker())
        assigned_name = binascii.hexlify(os.urandom(20)).decode()

        self.eval_tasks.update({assigned_name: task})
        message = await ctx.send('Starting task, Assigned name: `{}`'.format(assigned_name))
        await asyncio.wait_for(task, timeout=100000000000000000000000000.0)
        result, end = task.result()

        try:
            self.eval_tasks.pop(assigned_name)
        except KeyError:
            return
        ## MEANS TASK IS DEAD!

        embed = discord.Embed(title='Evaluated Code:', colour=discord.Colour.green())
        embed.add_field(name='Input:', value='```py\n{}\n```'.format('\n'.join([i.strip() for i in cmd.split('\n')])))
        embed.add_field(name='Output:', value='```{}```'.format(result), inline=False)
        embed.set_footer(text='Evaluation took {!r}ms'.format(round((end - start) * 1000, 5)), icon_url=ctx.me.avatar)
        await message.reply(embed=embed)

    @eval_fn.command()
    async def kill(self, ctx: commands.Context, taskname: str) -> typing.Union[typing.Optional[discord.Embed], discord.MessageReference]:
        if ctx.author.id not in [491630879085559808, 475357293949485076]:
            return await ctx.message.reply('You do not own me.')
        task: asyncio.Task = self.eval_tasks.get(taskname)
        if not task:
            return await ctx.message.reply('This take doesn\'t exist!')
        task.cancel()
        self.eval_tasks.pop(taskname)
        return await ctx.message.reply('Killed this eval task for you!')

    @eval_fn.error
    async def bent_code(self, ctx, error):
        if ctx.author.id not in [491630879085559808, 475357293949485076]:
            return
        if isinstance(error, commands.errors.NotOwner):
            return
        error = traceback.format_exception(etype=type(error), value=error, tb=error.__traceback__)
        return await ctx.send('```' + ''.join(map(str, error)) + '```')

def setup(bot):
    bot.add_cog(Eval(bot))
