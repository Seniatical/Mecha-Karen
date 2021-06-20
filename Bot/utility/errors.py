from discord.ext import commands

class NotGuildOwner(commands.CheckFailure):
    pass

class NotInVoice(commands.CheckFailure):
    pass

class Occupied(commands.CheckFailure):
    pass

class Blacklisted(commands.CheckFailure):
    pass
