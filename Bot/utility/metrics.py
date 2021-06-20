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

import math

def abbrev_denary(number):
    if number == 0:
        return "0"
    size_name = ("", "K", "M", "B", "T", "Qd", "Qn", "Sx", "Sp")
    i = int(math.floor(math.log(number, 1000)))
    p = math.pow(1000, i)
    s = round(number / p, 2) if len(str(p)) > 4 else int(round(number / p, 2))
    return "%s %s" % (s, size_name[i])
