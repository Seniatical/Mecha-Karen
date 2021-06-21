import json
from pydantic import BaseModel

r"""

    EXAMPLE CONFIG DATA
 
{
    "default_prefix": "-",
    "intents": [
        "guilds",
        "members",
        "bans",
        "emojis",
        "voice_states",
        "presences",
        "messages",
        "guild_messages",
        "reactions",
    ],
    "guild_logs": "Channel to log all guild joins",
    "error_logs": "Channel to log all errors from commands",
    
    "case_sensitive": false,
    "description": "I am Mecha Karen, An Open Sourced Bot Inspiring Others!"
}
"""

try:
    with open('./storage/storage/config.json', 'r') as f:
        data = json.load(f)
except FileNotFoundError as error:
    raise FileNotFoundError('Cannot locate config.json file!')
except json.JSONDecodeError as error:
    raise Exception('Failed to read your .json file') from error


class BotModel(BaseModel):
    default_prefix: str
    guild_logs: int
    error_logs: int
    intents: tuple
