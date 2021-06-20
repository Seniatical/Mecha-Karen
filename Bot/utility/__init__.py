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

from . import *

from .facts import (facts, bot_facts)
from .genders import genders
from .jokes import jokes as _jokes
from .cache import Cache
from .hangman import boards
from .env import Enviroment
from .min import get_rep
from .premium import wrap_cooldown
from .handler import MongoDB
from .embeds import get_dm_embed
from .prefix import Prefix
from ._resp import (roasts, deaths)
from .metrics import abbrev_denary
