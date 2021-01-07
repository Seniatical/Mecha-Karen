# !/usr/bin/python

import os

class NotMainFile(Exception):
    pass
    
class IncorrectDirectory(Exception):
    pass

if not __name__ == '__main__':
    raise NotMainFile('File ran must be __main__.py from the MASTER folder.')

current_path = os.path.dirname(os.path.realpath(__file__))

try:
    os.chdir(current_path + '\\' + 'Bot')
except FileNotFoundError:
    raise IncorrectDirectory('Run __main__.py in the FOLDER outside of the Bot folder')

from Bot import bot
''' 
Imported here to prevent a circular loop, Just in case i accidently run the bot.py file instead of this.
And also to actually set the directory up there before importing
'''

print('Starting Up Karen...')
bot.Mecha_Karen()
