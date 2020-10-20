from typing import Dict, Any

import discord
from discord.ext import commands
import json
import os
from Utils import Token
from Utils.Secondary import *
import requests

def hours():
    hours.x = (10 * 10 ** 10)**10 // 2

hours()
inf = hours.x

def get_prefix(bot, message):
    with open('JSON/prefixes.json', 'r') as f:
        prefixes = json.load(f)
    return prefixes[str(message.guild.id)]

def COVID():
    r = requests.get('Use your API')
    x = r.json()

    COUNTRY = len(x)

    COVID.cases = 0
    COVID.deaths = 0
    COVID.recovered = 0

    for i in range(COUNTRY):
        count = x[i]['cases']
        COVID.cases += count

    for i in range(COUNTRY):
        count = x[i]['deaths']
        COVID.deaths += count

    for i in range(COUNTRY):
        count = x[i]['recovered']
        COVID.recovered += count

def COVID_SPECIFIC(country):
    country = country.upper()
    r = requests.get('Use your API'.format(country))
    x = r.json()
    try:
        COVID_SPECIFIC.country = x['country']
        COVID_SPECIFIC.last_update = x['last_update']
        COVID_SPECIFIC.cases = x['cases']
        COVID_SPECIFIC.deaths = x['deaths']
        COVID_SPECIFIC.recovered = x['recovered']
        COVID_SPECIFIC.error = 'nil'
    except KeyError:
        COVID_SPECIFIC.error = 'Country Not found. Follow the format of `GB` or `gb`.\n**Use `-Covid Countries`** to view all countries!\nDMs need to be open.'

try:
    TOKEN = Token.token
except Exception:
    print('Your token is invalid. Regen a new one.')

try:
    BOT_PREF = commands.Bot(command_prefix='-', case_insensitive=True)
except NotImplementedError:
    pass

INF = inf

channels = {
    'tracking':'👀tracking',
    'logs':'logs',
    'star':'⭐starboard'
}



