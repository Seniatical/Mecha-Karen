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

import io
import typing
from PIL import Image, ImageEnhance, ImageOps
from ._ import save_image, sort_size, discord
from glitch_this import ImageGlitcher
from io import BytesIO
import cv2 as opencv
import numpy as np

glitcher = ImageGlitcher()

file = discord.File
MAX_FRAMES = 30

def exceeded_frames(self, image: Image, ignore: str):
    if getattr(image, 'is_animated', False) and ignore.lower() in [
        '--true', '--ignore-frames', '--reduce',
        '--filter'
    ]:
        if ignore.lower() in ['--reduce', '--filter']:
            pass
        else:
            return image.n_frames > 30
    return False

def IMAGEOPS(effect, stream: io.BytesIO, animate: str, *size) -> Image:
    image: Image = Image.open(stream)

    try:
        if type(size[-1]) == dict:
            kwargs = size[-1]
            size = size[:-1]
        else:
            kwargs = {}
    except IndexError:
        kwargs = {}

    if not size and not getattr(stream, 'discord', False):
        size = image.size
    else:
        size = sort_size(*size)

    if getattr(image, 'is_animated', False) and animate.lower() == '--true':
        duration = image.info.get('duration')
        loops = image.info.get('loop')

        frames = []
        frames_ = image.n_frames if image.n_frames <= MAX_FRAMES else MAX_FRAMES
        for _ in range(frames_):
            frames.append(effect.__call__(image=image.convert('RGB').resize(size), **kwargs))
            image.seek(_)
        return save_image(image=frames, filename='{}.gif'.format(effect.__class__.__name__), duration=duration, loop=loops)

    else:
        inverted: Image = effect.__call__(image=image.convert('RGB').resize(size))
        return save_image(image=inverted, filename='{}.png'.format(effect.__class__.__name__))

def COLOUR_MAP(func, stream: io.BytesIO, animate: str, *size) -> Image:
    try:
        if type(size[-1]) == dict:
            kwargs = size[-1]
            size = size[:-1]
        else:
            kwargs = {}
    except IndexError:
        kwargs = {}

    try:
        if type(size[-1]) == list:
            args = size[-1]
            size = size[:-1]
        else:
            args = []
    except KeyError:
        args = []

    file_bytes = np.asarray(bytearray(stream.read()), dtype=np.uint8)
    image = opencv.imdecode(file_bytes, opencv.IMREAD_COLOR)
    opencv.waitKey(1)

def glitch_(stream, level, animate, size):
    image = Image.open(stream)

    if not size and not getattr(stream, 'discord', False):
        size = image.size
    else:
        size = sort_size(*size)
    data = {}

    if animate.lower() == '--true' and getattr(image, "is_animated", False):
        glitched = []

        frames_ = image.n_frames if image.n_frames <= MAX_FRAMES else 100
        for frame in range(frames_):
            try:
                image.seek(frame)
            except EOFError:
                continue

            glitch = glitcher.glitch_image(image.convert('RGB').resize(size), level, color_offset=True)
            glitched.append(glitch)
        data['duration'] = image.info.get('duration') or 150
    else:
        data['duration'] = 150
        glitched = glitcher.glitch_image(image.convert('RGB').resize(size), level, color_offset=True,
                                         gif=True)

    return save_image(image=glitched, filename='glitched.gif', **data)


def spin_(image: typing.BinaryIO, animate: str) -> save_image:
    image = Image.open(image)

    frames = []

    if getattr(image, 'is_animated', False) and animate.lower() == '--true':
        frames_to_use: float = 360 / image.n_frames
        if int(frames_to_use) - frames_to_use != 0:
            frames_to_use += 1
        frames_to_use = int(frames_to_use)

        frames_to_use = frames_to_use if frames_to_use <= MAX_FRAMES else MAX_FRAMES

        degrees: list[int] = list(range(0, 361, frames_to_use))
        for _ in range(image.n_frames):
            try:
                frames.append(image.convert('RGBA').rotate(-degrees[_]).convert('RGBA'))
            except Exception:
                continue
            image.seek(_)

    else:

        for i in range(0, 361, 15):
            frames.append(image.convert('RGBA').rotate(-i).convert('RGBA'))

    with BytesIO() as buffer:
        frames[0].save(
            buffer,
            format='GIF',
            append_images=frames[1:],
            save_all=True,
            optimize=False,
            loop=0,
            duration=5
        )
        buffer.seek(0)
        return file(fp=buffer, filename='spin.gif')

def gayify_(stream: BytesIO, animate, *size):
    image = Image.open(stream)

    if not size and not getattr(stream, 'discord', False):
        size = image.size
    else:
        size = sort_size(*size)

    with Image.open('./storage/images/gay.png') as _:
        gay_filter = _.resize(size)

    image = image.resize(size)
    image.paste(gay_filter, (0, 0), gay_filter)

    return save_image(image, 'gay.png')
