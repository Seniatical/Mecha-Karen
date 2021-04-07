from .cog import Cog  ## MAIN COG FOR THE RPG
from .gangs import Gangs  ## HELP COMMANDS / TUTORIALS
from .use import Use ## Commands to use special items and stuff
from .owner import EcoOwner ## Owner commands
from .DB import *
from .src.shop import shop as Shop

__all__ = (
    'Cog', 'Support', 'Use', 'EcoOwner',
    'connection', 'root_db', 'main',
    'blacklists', 'get_user', 'can_prestige',
    'reset_progress', 'prestige'
)

cogs = ['Cog', 'Gangs', 'Use', 'EcoOwner']
paths = [
    'cogs.RPG.cog',
    'cogs.RPG.gangs',
    'cogs.RPG.use',
    'cogs.RPG.owner'
]

def setup(bot):
    for cog in cogs:
        if not bot.get_cog(cog):
            bot.load_extension(paths[cogs.index(cog, 0)])
        else:
            bot.reload_extension(paths[cogs.index(cog, 0)])
    print('Added/Reloaded RPG Sector')
