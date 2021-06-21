from .config import BotModel
from .bot import MechaKaren
from discord.ext.commands import Cog
from abc import ABC

class KarenMixin(ABC):
    r"""
    Base Class for cogs - Holds some key functions and other stuff which wont need constant re-defining
    In in each cog
    """
    defaults: BotModel
    bot: MechaKaren

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.attrs = None

        super().__init__()

    def cog_unload(self):
        super().cog_unload()
        
    def attributes(self):
        values = dir(super())
        accepted = []
        for value in values:
            if not callable(getattr(super(), value)):
                ## If it the attr is callable we dont class it as an attribute
                accepted.append(value)
        self.attrs = accepted
        return accepted

class KarenMetaClass(type(Cog), type(ABC)):
    """
    This allows the metaclass used for proper type detection to
    coexist with discord.py's metaclass
    """
