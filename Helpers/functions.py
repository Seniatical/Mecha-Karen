async def is_guild_owner(ctx):
    if ctx.author != ctx.guild.owner:
        return False
    return True
