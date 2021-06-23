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

from core import bot, meta
import os
import tracemalloc
import argparse

parse = argparse.ArgumentParser(description='Optional CLI for running Mecha Karen')
parse.add_argument('--meta', type=None, help='Run the meta version of Mecha Karen')
parse.add_argument('--main', type=None, help='[Default] Run the main bot!')

if __name__ == '__main__':
    args = vars(parse.parse_args())

    tracemalloc.start()

    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    
    if 'meta' in args:
        karen = meta.MechaKaren()
    elif 'main' in args:
        ## Well theres only 1 command other then help
        karen = bot.MechaKaren()
    else:
        exit()
    ipc = karen.ipc

    print('Websocket running on: ', (ipc.host, ipc.port, ipc.multicast_port))

    karen.run()

else:
    raise RuntimeError('Make sure your running `main.py`!')

tracemalloc.stop()
