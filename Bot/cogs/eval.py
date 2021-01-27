"""
Copyright ©️: 2021 Seniatical / _-*™#7519
License: Apache 2.0

A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.

Licensed works, modifications, and larger works may be distributed under different terms and without source code.
FULL LICENSE CAN BE FOUND AT:
    https://www.apache.org/licenses/LICENSE-2.0.html
    
Any violation to the lisence, will result in moderate action
You are required to mention (original author, lisence, source, any changes made)
"""


import discord
import re
import textwrap
from discord.ext import commands
import aiohttp



## so we dont have to call it everytime we need it

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


def format_code(code: str):
    try:
        if match := list(FORMATTED_CODE_REGEX.finditer(code)):
            blocks = [block for block in match if block.group("block")]
            if len(blocks) > 1:
                code = '\n'.join(block.group("code") for block in blocks)
            else:
                match = match[0] if len(blocks) == 0 else blocks[0]
                code, block = match.group("code", "block")
        else:
            code = RAW_CODE_REGEX.fullmatch(code).group("code")
        code = textwrap.dedent(code)
        return code
    except Exception as e:
        print(e)


class Eval(commands.Cog):
    """
    THIS EVAL IS DEPENDENT ON DOCKER
    This is a better alternative to pythonanywhere becuase it's safe, and faster by alot.
    + IF ON LINUX -->
        curl -sSL https://get.docker.com/ | CHANNEL=stable bash
    + Once you do that run this -->
        docker run --ipc=none --privileged -p 8060:8060 ghcr.io/python-discord/snekbox
    This installs snekbox if not already installed and runs it
    From there, you can start making requests to localhost:8060
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def eval(self, ctx, *, code) -> discord.Embed:
        try:
            embed = discord.Embed(title="Evaluating Code...", color=discord.Colour.green())
            msg = await ctx.send(embed=embed)
            code = format_code(code)
            async with aiohttp.ClientSession() as session:
                async with session.post('http://localhost:8060/eval', json={'input': code}) as resp: # Making the request
                    response = await resp.json()
            if response['stdout'] == '':
                response['stdout'] = "[No Result]"  # If no return value was given
            embed = discord.Embed(title="Eval Complete!", color=discord.Colour.green())
            embed.add_field(name="**Results:** ", value=f"```\n{response['stdout']}```")
            await msg.edit(embed=embed)
        except discord.HTTPException:
            embed = discord.Embed(title="The Results of the Eval was too large to send!", color=discord.Colour.red())
            await msg.edit(embed=embed)
        except Exception as e:
            print(e)


def setup(bot):
    bot.add_cog(Eval(bot))
