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

import pymongo
from .env import Enviroment
import asyncio
import types


class MongoDB:
    def __init__(self, uri: str = None, env_path: str = './.env',
                 loop: asyncio.AbstractEventLoop = asyncio.get_event_loop(),
                 env: Enviroment = None, **mongo_config) -> None:
        self.uri = uri

        if not self.uri:
            self.env = env or Enviroment(env_path)
            self.uri = self.env('MONGO_DB_URI')

        self.conn = pymongo.MongoClient(self.uri, **mongo_config)
        self.loop = loop or asyncio.new_event_loop()

    def ping(self):
        database = self.conn.get_database('Bot')
        ping = database.command('ping')
        return ping

    async def find_one(self, query: dict, table: str = 'Bot', column: str = 'Guilds', **kwargs):
        return await self.loop.run_in_executor(None, self.conn[table][column].find_one, query, **kwargs)

    async def update_one(self, query: dict, table: str = 'Bot', column: str = 'Guilds', **kwargs):
        return await self.loop.run_in_executor(None, self.conn[table][column].update_one, query, **kwargs)

    async def insert_one(self, query: dict, table: str = 'Bot', column: str = 'Guilds', **kwargs):
        self.conn['Guilds'].collection_names()
        return await self.loop.run_in_executor(None, self.conn[table][column].insert_one, query, **kwargs)

    async def delete_one(self, query: dict, table: str = 'Bot', column: str = 'Guilds', **kwargs):
        return await self.loop.run_in_executor(None, self.conn[table][column].delete_one, query, **kwargs)

    async def manual(self, func: types.FunctionType, **kwargs):
        return await self.loop.run_in_executor(None, func=func, **kwargs)

    async def __aiter__(self, query=None, table: str = 'Bot', column: str = 'Guilds'):
        if query is None:
            query = dict()
        col = self.conn[table][column]
        data = await self.loop.run_in_executor(None, col.find, query)
        for _ in data:
            yield data