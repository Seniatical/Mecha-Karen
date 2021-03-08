from Utils import hashes

async def get_command_by_aliases(bot, aliase):
    aliases = {}
    for command in bot.commands:
        if command.aliases:
            for _aliase in command.aliases:
                aliases[_aliase.lower()] = command
        else:
            aliases[(command.name).lower()] = command
    return aliases.get(aliases.lower())

async def get_command_by_hash(bot, hash):
    commands = bot.commands
    
    def hashmap():
        hashm = hashes.BASE_COMMAND_MAP
        return hashm if len(hash) == len(commands) else None
    
    for command in commands:
        if hashes.get_by_hashmap(command.name, mapper=hashmap, attrs=False, cls=True):
            return command
    return False
