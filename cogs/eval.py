import requests
import time
import discord
import re
import textwrap
from discord.ext import commands
username = 'go to pythonanywhere'
token = 'and get a api token'

ESCAPE_REGEX = re.compile("[`\u202E\u200B]{3,}")
FORMATTED_CODE_REGEX = re.compile(
    r"(?P<delim>(?P<block>```)|``?)"        # code delimiter: 1-3 backticks; (?P=block) only matches if it's a block
    r"(?(block)(?:(?P<lang>[a-z]+)\n)?)"    # if we're in a block, match optional language (only letters plus newline)
    r"(?:[ \t]*\n)*"                        # any blank (empty or tabs/spaces only) lines before the code
    r"(?P<code>.*?)"                        # extract all code inside the markup
    r"\s*"                                  # any more whitespace before the end of the code markup
    r"(?P=delim)",                          # match the exact same delimiter from the start again
    re.DOTALL | re.IGNORECASE               # "." also matches newlines, case insensitive
)
RAW_CODE_REGEX = re.compile(
    r"^(?:[ \t]*\n)*"                       # any blank (empty or tabs/spaces only) lines before the code
    r"(?P<code>.*?)"                        # extract all the rest as code
    r"\s*$",                                # any trailing whitespace until the end of the string
    re.DOTALL                               # "." also matches newlines
)

def prepare_input(code: str) -> str:
    if match := list(FORMATTED_CODE_REGEX.finditer(code)):
        blocks = [block for block in match if block.group("block")]

        if len(blocks) > 1:
            code = '\n'.join(block.group("code") for block in blocks)
        else:
            match = match[0] if len(blocks) == 0 else blocks[0]
            code, block, lang, delim = match.group("code", "block", "lang", "delim")
            if block:
                info = (f"'{lang}' highlighted" if lang else "plain") + " code block"
            else:
                info = f"{delim}-enclosed inline code"
    else:
        code = RAW_CODE_REGEX.fullmatch(code).group("code")
        info = "unformatted or badly formatted code"

    code = textwrap.dedent(code)
    return code

class Eval(commands.Cog):

    def __init__(self,bot):
        self.bot = bot

    async def result(self,code):
        requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/main.py/'.format(username = username),
        files = {"content":code},headers={'Authorization': 'Token {token}'.format(token=token)})

        requests.post('https://www.pythonanywhere.com/api/v0/user/{username}/consoles/17872672/send_input/'.format(username = username),
        data = {"input":"python3 main.py &> output.txt\n"},headers={'Authorization': 'Token {token}'.format(token=token)})

        response = requests.get(
            'https://www.pythonanywhere.com/api/v0/user/{username}/files/path/home/{username}/output.txt/'.format(
                username=username
            ),
            headers={'Authorization': 'Token {token}'.format(token=token)}
        )
        if response.status_code == 200:
            return response.content.decode('ascii')
        else:
            return False

    @commands.command()
    async def eval(self,ctx,*,code):
        try:
            embed = discord.Embed(title = "Evaluating Code...", color = discord.Colour.green())
            await ctx.send(embed = embed)
            code = prepare_input(code)
            data = await self.result(code)
            if data == False:
                embed = discord.Embed(title = "The Result is too Large!", color = discord.Colour.red())
                await ctx.send(embed = embed)
                return
            embed = discord.Embed(title = "Eval Complete!", color = discord.Colour.green())
            embed.add_field(name = "**Results:** ", value = f"```{data}```")
            await ctx.send(embed = embed)
        except Exception as e:
            print(e)

def setup(bot):
    bot.add_cog(Eval(bot))
