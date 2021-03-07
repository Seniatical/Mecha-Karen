class Cache:
    def __init__(self, cache = None):
        self.cache = cache or {}  ## Load pre-exising cache if you like
        
    async def update_cache(self, key, value) -> dict:
        if key in self.cache:
            self.cache[key] = value
        else:
            self.cache.update({key: value})
        return self.cache
    
    async def remove_key(self, **values):
        if 'key' in values:
            value = values['key']
        else:
            value = values['value']
            
        temp = {v: k for k, v in self.cache.items()} if 'key' in values else self.cache
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
    
    async def add_new_container(self, name, cache = None):
        global temp
        cache = cache or {}
        exec('''self.{} = {}'''.format(name, cache))
        exec('''global temp
temp = self.{}
        '''.format(name))
        return temp
    
    async def whole_cache(self, name):
        global temp
        exec('''global temp
temp = self.{}
        '''.format(name))
        return temp
