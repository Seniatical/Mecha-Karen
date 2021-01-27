"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0

A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.

FULL LISENCE CAN BE FOUND:
    https://www.apache.org/licenses/LICENSE-2.0.html

Any voilations to the lisence, will result in moderate action

Your required to mention (original author, lisence, source, any changes made)
"""

import requests
import time
import discord
import re
import asyncio
import textwrap
from discord.ext import commands, tasks
import os


class DATA:
    def __init__(self):
        #       replace it with your pythonanywhere user name
        self.username = os.environ.get("eval_name")
        
        #       replace it with your pythonanywhere user token
        self.token = os.environ.get("eval_token")


ESCAPE_REGEX = re.compile("[`\u202E\u200B]{3,}")
FORMATTED_CODE_REGEX = re.compile(
    r"(?P<delim>(?P<block>```)|``?)"
    r"(?(block)(?:(?P<lang>[a-z]+)\n)?)"
    r"(?:[ \t]*\n)*"
    r"(?P<code>.*?)"
    r"\s*"
    r"(?P=delim)",
    re.DOTALL | re.IGNORECASE
)
RAW_CODE_REGEX = re.compile(
    r"^(?:[ \t]*\n)*"
    r"(?P<code>.*?)"
    r"\s*$",
    re.DOTALL
)

def prepare_input(code: str) -> str:
    if match := list(FORMATTED_CODE_REGEX.finditer(code)):
        blocks = [block for block in match if block.group("block")]

        if len(blocks) > 1:
            code = '\n'.join(block.group("code") for block in blocks)
        else:
            match = match[0] if len(blocks) == 0 else blocks[0]
            code, block, lang, delim = match.group(
                "code", "block", "lang", "delim")
            if block:
                info = (
                    f"'{lang}' highlighted" if lang else "plain") + " code block"
            else:
                info = f"{delim}-enclosed inline code"
    else:
        code = RAW_CODE_REGEX.fullmatch(code).group("code")
        info = "unformatted or badly formatted code"

    code = textwrap.dedent(code)
    return code


class Eval(commands.Cog):
    """
    + go to website --> 
        https://www.pythonanywhere.com/

    + make an accout
    + make a new bash
    + then get api token
    + to get api token --> 
        https://www.pythonanywhere.com/user/User_Name/account/#api_token

    + replace 
        self.username = os.environ.get("eval_name") (line 14)
        self.token = os.environ.get("eval_token")      (line 17)

    with your username and token
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.keep_alive.start()

    @tasks.loop(minutes=30)
    async def keep_alive(self):
        console_id = await self.get_console()

        requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/send_input/'.format(username=DATA().username, console_id=console_id),
                      data={"input": "ls\n"}, headers={'Authorization': 'Token {token}'.format(token=DATA().token)})

    async def get_console(self):
        consoles = requests.get('https://www.pythonanywhere.com/api/v0/user/{username}/consoles/'.format(
            username=DATA().username), headers={'Authorization': 'Token {token}'.format(token=DATA().token)})

        for x in consoles.json():
            if x['executable'] == 'bash':
                console_id = x['id']
                return console_id

    async def result(self, code):
        console_id = await self.get_console()
        requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/main.py/'.format(username=DATA().username),
                      files={"content": code}, headers={'Authorization': 'Token {token}'.format(token=DATA().token)})

        requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/consoles/{console_id}/send_input/'.format(username=DATA().username, console_id=console_id),
                      data={"input": "python3 main.py &> output.txt\n"}, headers={'Authorization': 'Token {token}'.format(token=DATA().token)})

        await asyncio.sleep(3)

        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/output.txt/'.format(
                username=DATA().username
            ),
            headers={'Authorization': 'Token {token}'.format(
                token=DATA().token)}
        )

        if response.status_code == 200:
            return response.content.decode('ascii')

        else:
            return False

    @commands.command(aliases=["e"])
    async def eval(self, ctx, *, code=None):
        embed = discord.Embed(
            title=f"Eval command",
            description=eval_command,
            color=discord.Color.random()
        )
        embed.set_footer(
        text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Eval(bot))
