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

import typing
from PIL import Image
import discord
import io

def save_image(image: typing.Union[list, Image.Image], filename: str, **kwargs) -> discord.File:
    if type(image) == list:
        with io.BytesIO() as buffer:
            duration = kwargs.get('duration')
            loop = kwargs.get('loop')

            if duration:
                image[0].save(
                    buffer, 'GIF',
                    duration=duration,
                    loop=0, save_all=True,
                    append_images=image[1:]
                )
            else:
                image[0].save(
                    buffer, 'GIF',
                    loop=loop, save_all=True,
                    append_images=image[1:]
                )
            buffer.seek(0)

            return discord.File(fp=buffer, filename=filename)

    with io.BytesIO() as buffer:
        image.save(buffer, kwargs.get('type') or 'PNG')
        buffer.seek(0)

        return discord.File(fp=buffer, filename=filename)

def sort_size(*size) -> tuple:
    if size:
        if len(size) > 1:
            x, y = tuple(map(int, size[:2]))
        else:
            x, y = size[0], 300
    else:
        x, y = (300, 300)
    try:
        size = tuple(map(int, (x, y)))
    except ValueError:
        size = (300, 300)

    if any(i for i in size if i > 900):
        size = (300, 300)

    return size
