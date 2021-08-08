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

import json

class Cache:
    def __init__(self, cache = None):
        self.cache = cache or {}  ## Load pre-exising cache if you like
        
    async def base_template(self, user_id: int) -> dict:
        if user_id in self.cache:
            return False
        self.cache.update({user_id: {
            "images": [],
            "messages": [],
        }})
        
        # REMOVE: user looping - cache grows very large
        return True
        
    def to_json(self, path, container):   ## Usually i will have 2 but fish
        ## My Method is to use try and finally to do this :>
        ## not async cus it only used when the bot = dead
        data = self.get_cache(container)
        with open(path, 'w') as f:
            json.dump(f, data, indent=4)
        
    async def update_cache(self, key, value, num) -> dict:
        if key in self.cache:
            self.cache[key][num] = value
        else:
            self.cache.update({key: value})
        return self.cache
    
    async def remove_key(self, **values):
        if 'key' in values:
            value = values['key']
        else:
            value = values['value']
            
        temp = {v: k for k, v in self.cache.items()} if 'value' in values else self.cache
        if temp != self.cache:
            ## keys and values are reversed
            value = temp[value]
        self.cache.pop(value)
        return self.cache

    async def get_value(self, key):
        return self.cache.get(key)
    
    async def get_key_by_value(self, value):
        temp = {v: k for k, v in self.cache.items()}
        return temp.get(value)
    
    async def add_new_container(self, name, cache = None, *, as_var: bool = False) -> dict:
        cache = cache or {}
        
        if as_var:
            setattr(self, name, cache)
        else:
            self.cache['name'] = cache
        
        return cache
    
    def get_cache(self, name, *, as_var: bool = False):
        if as_var:
            return getattr(self, name, None)
        return self.cache.get(name)
    
    ## Some methods
    
    def __len__(self):
        return len(self.cache)
    
