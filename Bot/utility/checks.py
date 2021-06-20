from discord.ext import commands
from .errors import *

def is_guild_owner():
    async def predicate(ctx):
        if ctx.author != ctx.guild.owner:
            raise NotGuildOwner('Your not the owner of the guild!')
        return True
    return commands.check(predicate)
