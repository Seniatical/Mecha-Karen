import pymongo
from typing import Union
from discord import Member
import datetime

connection = pymongo.MongoClient('')

root_db = connection['RPG']
blacklists = root_db['Blacklists']
main = root_db['Data']

prestige_base = 1000000
## Need 1mil radianites to prestige BASE

__base__ = {
    "_id": None,
    "resources": {
        "radianites": 0,
        "crystals": 0,
        "wood": 0,
        "steel": 0,
        "polymer": 0,
        "Fuel": 0,
    },
    "stats": {
        "level": 0,
        "cc": 0,
        "power": 0,
        "protection": None,
        "prestige": 0,
    },
    "troops": {},
    "buildings": {},
    "research": {},
    "boosts": {},
    }

def get_user(user: Union[Member, str, int]) -> dict:
    updated_base = None

    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})
    if not user_data:
        updated_base = __base__
        updated_base['_id'] = user

        ## 5 day protection for newer users
        now = datetime.datetime.utcnow()
        in_5_days = (now + 432000)
        as_iso = in_5_days.isoformat()
        updated_base['stats']['protection'] = as_iso

        main.insert_one(updated_base)

    ## It will always be one or the other
    ## Never both or none
    return user_data or updated_base

def can_prestige(user: Union[Member, str, int]) -> dict:
    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False
    ## Logically if they dont have an account how do they prestige

    return ((user_data['stats']['prestige'] + 1) * prestige_base) <= user_data['resources']['radianites']

def reset_progress(user: Union[Member, str, int]) -> dict:
    if type(user) == Member:
        user = member.id
    else:
        user = int(user)

    user_data = main.find_one({'_id': user})

    if not user_data:
        return False

    main.delete_one({'_id': user})

    return get_user(user)
