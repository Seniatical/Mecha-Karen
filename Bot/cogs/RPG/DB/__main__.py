import pymongo
from typing import Union
from discord import Member
from discord.ext.commands import check
from .errors import VerficationError

import datetime

connection = pymongo.MongoClient('')

root_db = connection['RPG']
blacklists = root_db['Blacklists']
main = root_db['Data']

prestige_base = 1000000
## Need 1mil pounds to prestige

user = {
    "_id": None,
    "gang": None,
    "pouch": 300,
    "stash": 0,
    "limit": 1000,
    "cylons": 500,
    "inv": {},
    "boosts": {},
    "prestige": 0,
    "extra": {}     ## Useful if I get any more ideas
}

gang = {
    "_id": None,        ## GANG NAME
    "owner": None,      ## OWNER ID
    "roles": [],        ## MAX OF 5 ROLES ORDERED LIKE 0 = HIGHEST, 5 = LOWEST
    "points": 0,        ## ACHIEVED IN WARS
    "allies": [],       ## ALLY WITH OTHER GANGS || MAX 5
    "members": [],      ## MAXIMUM OF 50 MEMBERS
    "invite": False,    ## IS IT INVITE ONLY - False: Anyone can join, True: Invite only, None: Closed
    "extra": {},        ## If i get any extra ideas
}

def has_verified():
    async def predicate(ctx):
        if not main.find_one({'_id': ctx.author.id}):
            raise VerficationError('User has not verified their account')
        return True
    return check(predicate)

async def get_user(user: Union[Member, str, int]) -> dict:
    updated_base = None

    if type(user) == Member:
        user = user.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})
    if not user_data:
        updated_base = user
        updated_base['_id'] = user

        main.insert_one(updated_base)
        
        updated_base['is_new'] = True

    ## It will always be one or the other
    ## Never both or none
    return user_data or updated_base

async def can_prestige(user) -> bool:
    if type(user) == Member:
        user = user.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False
    ## Logically if they don't have an account how do they prestige

    return ((user_data['prestige'] + 1.5) * prestige_base) <= user_data['pouch']

async def reset_progress(user: Union[Member, str, int]) -> dict:
    if type(user) == Member:
        user = user.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False

    main.delete_one({'_id': user})

    return await get_user(user)

async def prestige(user: Union[Member, str, int]) -> dict:
    if type(user) == Member:
        user = user.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False

    check = await prestige(user)

    if not check:
        return False

    ## Prestige gives a perm boost
    base = user
    base['prestige'] = (user_data['prestige'] + 1)
    base['cylons'] = user_data['cylons']

    main.update_one({'_id': user.id}, {'$set': base}, {'upsert': True})
    return base
