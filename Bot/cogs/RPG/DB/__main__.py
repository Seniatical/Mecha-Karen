import pymongo
from typing import Union
from discord import Member
import datetime

connection = pymongo.MongoClient('mongodb+srv://Seniatical:NFenqAE9RBlSPFwB@cluster0.rgnis.mongodb.net/RPG?retryWrites=true&w=majority')

root_db = connection['RPG']
blacklists = root_db['Blacklists']
main = root_db['Data']

prestige_base = 1000000
## Need 1mil pounds to prestige

__base__ = {
    "_id": None,
    "gang": None,
    "pouch": 300,
    "stash": 0,
    "cylons": 500,
    "inv": {},
    "boosts": {},
    "prestige": 0,
}

async def get_user(user: Union[Member, str, int]) -> dict:
    updated_base = None

    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})
    if not user_data:
        updated_base = __base__
        updated_base['_id'] = user

        main.insert_one(updated_base)

    ## It will always be one or the other
    ## Never both or none
    return user_data or updated_base

async def can_prestige(user) -> bool:
    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False
    ## Logically if they don't have an account how do they prestige

    return ((user_data['prestige'] + 1.5) * prestige_base) <= user_data['pouch']

async def reset_progress(user: Union[Member, str, int]) -> dict:
    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False

    main.delete_one({'_id': user})

    return await get_user(user)

async def prestige(user: Union[Member, str, int]) -> dict:
    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False

    check = await prestige(user)

    if not check:
        return False

    ## Prestige gives a perm boost
    base = __base__
    base['prestige'] = (user_data['prestige'] + 1)
    base['cylons'] = user_data['cylons']

    main.update_one({'_id': user.id}, {'$set': base}, {'upsert': True})
    return base
