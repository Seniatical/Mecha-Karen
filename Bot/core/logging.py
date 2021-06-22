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

import logging
import os
import typing

def setup_discord_logger():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)

    discord_handler = logging.FileHandler(filename='./storage/logs/discord.log', encoding='utf-8', mode='w')
    discord_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(discord_handler)

try:
    os.remove('./storage/logs/commands.log')
    os.remove('./storage/logs/discord.log')
    os.remove('./storage/logs/events.log')
except FileNotFoundError:
    print('Logging files dont exist, skipping deletion.')


class LoggingBase(object):
    def __init__(self, name: str, level,
                 *handlers: logging.Handler,
                 new_logger: bool = True, formatting: typing.Union[dict, logging.Formatter] = None,
                 ) -> None:
        self.name = name
        self.level = level
        self.handlers = handlers

        if new_logger:
            if type(level) == str:
                self.level = getattr(logging, level.upper())
                # Converts DEBUG to logging.DEBUG

            self.logger = logging.Logger(name, self.level)
        else:
            self.logger = logging.getLogger(name)

        if handlers:
            for handler in handlers:
                if formatting:
                    if type(formatting) == dict:
                        format_ = formatting.get(handler.__class__.__name__)
                    else:
                        format_ = formatting
                else:
                    format_ = None

                handler.setFormatter(format_)
                self.logger.addHandler(handler)

    def log(self, message: str, name: str = ...,
            level: typing.Union[str, int] = logging.DEBUG
            ):
        if type(level) == str:
            level = getattr(logging, level)
        name = 'N.A' if type(name) == Ellipsis else name

        message += f" *({name})"

        self.logger.log(level=level, message=message)

    def debug(self, message: str, name: str):
        message += f" *({name})"
        self.logger.debug(msg=message)

    def error(self, message: str, name: str):
        message += f" *({name})"
        self.logger.error(msg=message)

    def critical(self, message: str, name: str):
        message += f" *({name})"
        self.logger.critical(msg=message)

    def exception(self, message: str, name: str):
        message += f" *({name})"
        self.logger.exception(message)

    def warn(self, message: str, name: str):
        message += f" *({name})"
        self.logger.warning(msg=message)

    @property
    def warning(self):
        # self.warning(...)
        return self.warn


class CommandLogger(LoggingBase):
    def __init__(self) -> None:

        handler = logging.FileHandler(filename='./storage/logs/commands.log', encoding='utf-8', mode='w')
        formatting = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

        # Remove log files on boot-up to prevent huge log files piling up.
        super().__init__('CommandLogger', logging.DEBUG, handler, formatting=formatting)

class EventLogger(LoggingBase):
    def __init__(self) -> None:
        handler = logging.FileHandler(filename='./storage/logs/events.log', encoding='utf-8', mode='w')
        formatting = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

        super().__init__('EventLogger', logging.DEBUG, handler, formatting=formatting)
