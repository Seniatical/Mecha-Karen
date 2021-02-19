try:
    import bs4
    import aiohttp
    import html5lib
    import datetime
    import json
except ModuleNotFoundError as import_error:
    raise ModuleNotFoundError(import_error)


class useful:
    def __init__(self):
        self.maximum = 100
        self.minimum = 10
        self.months = [datetime.date(2020, i, 1).strftime('%B') for i in range(1, 13)]
        self.opts = ['date', 'author', 'rating', 'example', 'meaning']


def is_homepage(query: str = None):
    if not query:
        return 'No link was specifed'
    query = query.lower()
    if query == 'https://www.urbandictionary.com/':
        return True
    return False


def is_urban(query: str = None):
    query = query.lower()
    if not query:
        return 'No link was specifed'
    if not 'https://www.urbandictionary.com/' in query:
        return False
    return True


async def is_valid_word(name: str = None):
    if not name:
        return 'No word was specifed'
    async with aiohttp.ClientSession() as session:
        async with session.get('https://www.urbandictionary.com/define.php?term={}'.format(name)) as r:
            r = await r.text()
            code = bs4.BeautifulSoup(r, 'html5lib')
            valid = code.find("div", attrs={'class': 'meaning'})
            if not valid:
                return False
            return True


def recieve(word):
    returner = {}
    x = useful().opts
    for i in range(0, 5):
        if i == 0:
            res = search(word).date
            returner[x[i]] = res
        if i == 1:
            res = search(word).author
            returner[x[i]] = res
        if i == 2:
            res = search(word).rating
            returner[x[i]] = res
        if i == 3:
            res = search(word).example
            returner[x[i]] = res
        if i == 4:
            res = search(word).meaning
            returner[x[i]] = res
    return returner


class search:
    def __init__(self, query: str = None):
        try:
            if query.lower() == 'homepage':
                self.query = 'https://www.urbandictionary.com/'
            else:
                self.query = 'https://www.urbandictionary.com/' if not query else 'https://www.urbandictionary.com/define.php?term={}'.format(
                    query.title())
        except AttributeError:
            self.query = 'https://www.urbandictionary.com/'
        self.word_ = query

    async def meaning(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                homepage = is_homepage(self.query)
                if homepage:
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    return soup.find('div', attrs={'class': 'meaning'}).text
                else:
                    valid = await is_valid_word(self.word_)
                    if not valid:
                        return {'Error 404': 'Word not found'}
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    return soup.find('div', attrs={'class': 'meaning'}).text

    async def example(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                homepage = is_homepage(self.query)
                if homepage:
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    return soup.find('div', attrs={'class': 'example'}).text
                else:
                    valid = await is_valid_word(self.word_)
                    if not valid:
                        return {'Error 404': 'Word not found'}
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    return soup.find('div', attrs={'class': 'example'}).text

    async def author(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                homepage = is_homepage(self.query)
                if homepage:
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    full_author = soup.find('div', attrs={'class': 'contributor'}).text
                    for i in useful().months:
                        if i in full_author:
                            ind = full_author.index(i, 0)
                            new_author = full_author[2:ind]
                    return {'full': full_author, 'name': new_author.strip()}
                else:
                    valid = is_valid_word(self.word_)
                    if not valid:
                        return {'Error 404': 'Word not found'}
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    full_author = soup.find('div', attrs={'class': 'contributor'}).text
                    for i in useful().months:
                        if i in full_author:
                            ind = full_author.index(i, 0, -1)
                            new_author = full_author[2:ind]
                    return {'full': full_author, 'name': new_author.strip()}

    async def rating(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                homepage = is_homepage(self.query)
                if homepage:
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    downvotes = soup.find('a', attrs={'class': 'down'})
                    upvotes = soup.find('a', attrs={'class': 'up'})
                    return {'likes': upvotes.text, 'dislikes': downvotes.text}
                else:
                    valid = is_valid_word(self.word_)
                    if not valid:
                        return {'Error 404': 'Word not found'}
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    downvotes = soup.find('a', attrs={'class': 'down'})
                    upvotes = soup.find('a', attrs={'class': 'up'})
                    return {'likes': upvotes.text, 'dislikes': downvotes.text}

    async def created_at(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                home = is_homepage(self.query)
                if home == True or is_valid_word(self.word_) == True:
                    data = {}
                    soup = bs4.BeautifulSoup(await data.text(), 'html5lib')
                    full_str = soup.find('div', attrs={'class': 'contributor'}).text
                    for i in useful().months:
                        if i in full_str:
                            data['month'] = i
                            data['year'] = full_str[len(full_str) - 4:].strip()
                            data['day'] = full_str[len(full_str) - 8:len(full_str) - 6]
                            data['date'] = '%s-%s-%s' % (full_str[len(full_str) - 4:].strip(), useful().months.index(i, 0) + 1,
                                                         full_str[len(full_str) - 8:len(full_str) - 6])
                    return data
                else:
                    return {'Error 404': 'Word not found'}

    def all(self):
        holder = {}
        x = recieve(self.word_)
        holder.update({self.word_: x})
        return holder

    async def chosen_word(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                if self.word_:
                    soup = bs4.BeautifulSoup(data.content, 'html5lib')
                    return soup.find('a', attrs={'class': 'word'}).text
                return self.word_

    async def view(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.query) as data:
                x = is_valid_word(self.word_)
                if x == False:
                    holder = {}
                    holder.update({"Error 404": "Word not found"})
                else:
                    holder = {}
                    x = recieve(self.word_)
                    word = bs4.BeautifulSoup(await data.text(), 'html5lib').find('a', attrs={
                        'class': 'word'}).text if not self.word_ else self.word_.title()
                    holder.update({word: x})
                x = json.dumps(holder, indent=4)
                return x

    created_at, date = property(created_at), property(created_at)
    author = property(author)
    rating = property(rating)
    example = property(example)
    meaning = property(meaning)
    all, everything = property(all), property(all)
    view, format_data = property(view), property(view)
    the_word = property(chosen_word)
    print('\nReady to Locate your Word.')


