import os
import traceback

path = './src/'
dirs = []
cogs = []

""" PATH FINDING """
## Searches through dirs

for file in os.listdir(path):
    path_ = path + file
    if os.path.isdir(path_) and file != '__pycache__':
        dirs.append(path_)
    ## NOT ADDING COGS OUT OF FOLDERS!

for _dir in dirs:
    for file in os.listdir(_dir):
        path_ = _dir + '/' + file
        if not os.path.isdir(path_) and file != '__pycache__':
            cogs.append(path_)

def load_cogs(bot):
    for cog in cogs:
        try:
            ## COG IS THE RELATIVE PATH
            ## NEED TO CHANGE IT TO AN IMPORT
            ## CONVERTS ./path/to/cog.py - path.to.cog

            bot.load_extension(cog[2:].replace('/', '.')[:-3])
        except Exception as error:
            traceback.print_exception(type(error), error, error.__traceback__)
    bot.load_extension('src.help')

    return True
