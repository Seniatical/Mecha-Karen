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

import random
from discord import Embed, Colour
import datetime
from .facts import facts

## DM EMBEDS
async def get_dm_embed(bot, message):
    dm_embed = Embed(
        title='Hello {}!'.format(message.author),
        colour=Colour(random.randint(0x000000, 0xFFFFFF)),
        timestamp=datetime.datetime.utcnow(),
        description='I see you are interested! \👀'
    )
    dm_embed.add_field(name='Support Server?', value='**[My Support Server!](https://discord.gg/Q5mFhUM)**')
    dm_embed.add_field(name='Bot Invite?',
                    value='**[My Very Own Invite!](https://discord.com/api/oauth2/authorize?client_id=740514706858442792&permissions=8&scope=bot)**',
                    inline=False)
    dm_embed.add_field(name='Source Code?',
                    value='**[My Source Code!](https://github.com/Seniatical/Mecha-Karen-Source-Code)**', inline=False)
    dm_embed.add_field(name='Fun Fact!', value=random.choice(facts))
    dm_embed.set_thumbnail(url=bot.user.avatar_url)
    dm_embed.set_footer(
        text='Bot created by _-*™#7519',
        icon_url='https://i.imgur.com/jSzSeva.jpeg'
    )
    return dm_embed
## DM EMBEDS

