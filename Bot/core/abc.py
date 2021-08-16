# !/usr/bin/python

"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0
A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.
FULL LICENSE CAN BE FOUND AT:
    https://www.apache.org/licenses/LICENSE-2.0.html
Any violation to the license, will result in moderate action
You are legally required to mention (original author, license, source and any changes made)
"""

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
        
        self.attrs = []
        self.methods = []

        super().__init__()
        self._sort()

    def cog_unload(self):
        super().cog_unload()

    def _sort(self):
        values = dir(super())
        attrs, methods = ([], [])
        for value in values:
            if not callable(getattr(super(), value)):
                ## If it the attr is callable we dont class it as an attribute
                attrs.append(value)
            else:
                methods.append(value)
                
        self.attrs = attrs
        self.methods = methods
        
        return True


class KarenMetaClass(type(Cog), type(ABC)):
    pass
