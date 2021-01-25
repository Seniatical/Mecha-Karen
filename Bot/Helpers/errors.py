# !/usr/bin/python

"""
Copyright ©️: 2020 Seniatical / _-*™#7519
License: Apache 2.0

A permissive license whose main conditions require preservation of copyright and license notices.
Contributors provide an express grant of patent rights.
Licensed works, modifications, and larger works may be distributed under different terms and without source code.

FULL LISENCE CAN BE FOUND:
    https://www.apache.org/licenses/LICENSE-2.0.html

Any voilations to the lisence, will result in moderate action
"""

class BASE(Exception):
    pass

class NotGuildOwner(BASE):
    pass
    
class NotInVoice(BASE):
    pass
    
class NotUpdates(BASE):
    pass
    
class NotBot(BASE):
    pass
    
class ThreadingError(BASE):
    pass

class ConnectionError(BASE):
    pass

class BaseRAW(BASE):
    pass
