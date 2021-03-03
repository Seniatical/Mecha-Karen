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

import os
import shutil
from Utils import __logging__
from Utils import setup
from Utils.sensitive import env_reader
import bot
import threading

class Error(Exception):
    pass

def _stop(__cls):
    __cls = __logging__.clog(__cls)
    __cls.destroy(
        Trees = True
        reason = f'[{__cls.created_at.date}] | [Subprocess Destroyed] -> Killed via __main__.py',
        cause = __logging__.BUG ## Usual cause so ye
    )
    return __cls.process_id == None
    
if not __name__ == '__main__':
    raise Error('Not __main__.py file being ran!')
  
current_dir = os.getcwd()

if not current_dir.endswith('Bot'):
    raise Error('Move __main__.py into the Bot folder')
    
data = env_reader(get='*')
    
start = __logging__.BOOT(
    username = data['USERNAME']
    password = data['PASSWORD']
    host = 'https://127.0.0.1:9785',
    is_local = True
    server = data['SERVER_INFO']['ADDRESS']
    raise_on_warnings = True
    return_traceback = True
    lint = '*'
    time = __logging__.last_triggered_at
    )
    
if not start:
    raise Error('Failed to start up __logging__\n\n%s' % __logging__.dumps('ERROR')[0])
    
start.start(
    setup.setup()
)

start.rename_e = 'Mecha Karen'
mother = start.ROOT = 'MOTHER'  ## Default was set to `%root%`
mother.BRANCHES = __logging__.base_map('BRANCHES',
                                       ['INTERNAL HELPERS', __logging__.SWARM_BRANCH(None)]
                                      )

self = bot.Mecha_Karen()
_thread = threading.Thread(target=self.run)
_thread.run()

while _thread.is_alive():
    exp = __logging__.monitor(_thread)
    if 'error' in exp:
        __logging__.log('../logs/errors.log', type='error', format='[{date}] [{time}] -> {error.shortened} | {error.line}')

try:
    _stop(_thread)
except Exception as e:
    raise e
finally:
    os.kill(os.getpid(), 9)
