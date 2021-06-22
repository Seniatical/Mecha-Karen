from .bot import MechaKaren
from discord.ext.commands import Cog
from abc import ABC
from pydantic import BaseModel


class Bot(BaseModel):
    default_prefix: str = ""
    intents: tuple = ('guilds', 'members', 'bans', 'emojis', 'voice_states',
                      'presences', 'messages', 'guild_messages', 'reactions',
                      'integrations'
                      )
    # FALSE - Disabled
    logging: bool = True
    guild_logging: bool = True
    error_logging: bool = True
    running: bool = None


class KarenMixin(ABC):
    r"""
    Base Class for cogs - Holds some key functions and other stuff which wont need constant re-defining
    In in each cog
    """
    Bot.running = True

    defaults: Bot
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
    pass
