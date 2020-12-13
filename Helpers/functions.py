import discord, datetime
import os
import sys
import time
import socket
import random
import getpass
from os.path import isfile
from subprocess import call
from urllib.request import urlopen
from time import strftime,localtime

async def is_guild_owner(ctx):
    if ctx.author != ctx.guild.owner:
        return False
    return True

async def is_member(ctx):
    if ctx.author.bot:
        return False
    return True

async def is_voice(ctx, channel_name):
    for i in ctx.guild.channels:
        if i.name.lower() == channel_name:
            if isinstance(i, discord.VoiceChannel):
                return True
    return False

async def is_updates(ctx, channel_name):
    for i in ctx.guild.channel:
        if i.name.lower() == channel_name:
            if i.is_news():
                return True
    return False

async def time():
    return datetime.datetime.now().strftime('%j')

def interface_check(_iface=None):
	_i = os.popen('ip link | grep \"state\" | awk {\'print $2 $9\'}').read()
	ifaces = _i.split('\n')
	_l = len(ifaces)
	ifaces.pop(_l-1)

	_list  = {}
	for i in ifaces:
		item = i.split(':')
		_list[item[0]] = item[1]
		keys = _list.keys()
		for key in keys:
			stat = _list[key]
			if stat == "UP":
				_iface = key
			else:
				pass
	if _iface == None:
		sys.exit(log
				(
					'Check the connection retard.',err=True,end=True
				)
			)
	else:
		return _iface
