import discord
from discord.ext import commands
import asyncio
import json
import datetime

class JoinLeave(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cache = bot.cache

        if not self.cache.cache.get('jl'):
            print('Created new cache instance - Join/Leave channels')
            self.cache.cache.update({'jl': {}})

        if not getattr(self.bot, 'task_log', None):
            self.bot.task_log = {}

        if not self.bot.task_log.get('JL'):
            _task = self.bot.loop.create_task(self.cache_log())
            self.bot.task_log.update({'JL': _task})

    async def cache_log(self):
        while True:
            client = self.bot.client
            table = client['Bot']
            column = table['JL']

            self.cache.cache.update({'jl': {}})

            for collection in column.find():
                self.cache.cache['jl'].update({collection['_id']: {
                    'join_c': collection['wchannel'],
                    'join_m': collection['wmessage'],
                    'leave_c': collection['lchannel'],
                    'leave_m': collection['lmessage']
                }})
            await asyncio.sleep(30)  ## Refresh the cache every 20 seconds to prevent massive delays...

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        cls_c = self.cache.cache

        if member.guild.id in cls_c['jl']:
            _data = cls_c['jl'][member.guild.id]
            _channel = self.bot.get_channel(_data['join_c'])

            if not _channel:
                return

            message = _data['join_m']
            if not message or message == 'Not Set.':
                return
            message = message.replace('\\n', '\n')
            try:
                _message = message.replace('\'', '"')
                _embed = json.loads(_message)
            except Exception:
                _embed = False

            try:
                if not _embed:
                    parsed_message = message.format(member=member, user=member, guild=member.guild, server=member.guild)
                    await _channel.send(parsed_message)
                else:
                    embed = discord.Embed()
                    keys = {k.lower(): k for k in _embed.keys()}

                    if 'title' in keys:
                        _key = keys['title']
                        embed.title = _embed[_key].format(member=member, user=member, server=member.guild,
                                                          guild=member.guild)

                    if 'description' in keys or 'desc' in keys:
                        _key = keys['description' if 'description' in keys else 'desc']
                        embed.description = _embed[_key].format(member=member, user=member, server=member.guild,
                                                                guild=member.guild)

                    if 'colour' in keys or 'color' in keys:
                        _colour = keys['colour' if 'colour' in keys else 'color']
                        try:
                            _colour = _embed[_colour].replace('#', '0x')
                            _colour = int(_colour, 16)
                        except Exception:
                            _colour = discord.Colour.default()
                        embed.colour = _colour

                    if 'timestamp' in keys or 'time' in keys:
                        _key = keys['timestamp' if 'timestamp' in keys else 'time']
                        if _key:
                            embed.timestamp = datetime.datetime.utcnow()

                    if 'thumbnail' in keys or 'thumb' in keys:
                        _url = keys['thumbnail' if 'thumbnail' in keys else 'thumb']
                        try:
                            embed.set_thumbnail(url=_url)
                        except Exception:
                            pass

                    if 'image' in keys or 'img' in keys:
                        _url = keys['image' if 'image' in keys else 'img']
                        try:
                            embed.set_image(url=_url)
                        except Exception:
                            pass

                    if 'footer' in keys:
                        _mini = keys['footer']
                        _temp = {k.lower(): k for k in _mini.keys()}
                        if 'text' not in _temp or not ('image' in _temp or 'icon_url' in _temp):
                            pass
                        elif ('icon_url' in _temp or 'image' in _temp) and 'text' not in _temp:
                            embed.set_footer(icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']])

                        elif not ('icon_url' in _temp or 'image' in _temp) and 'text' in _temp:
                            embed.set_footer(
                                text=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                                 guild=member.guild))

                        elif 'icon_url' in _temp and ('icon_url' in _temp or 'image' in _temp):
                            embed.set_footer(
                                icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']],
                                text=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                                 guild=member.guild)
                            )
                        else:
                            pass

                    if 'author' in keys:
                        _mini = keys['author']
                        _temp = {k.lower(): k for k in _mini.keys()}
                        if 'text' not in _temp or not ('image' in _temp or 'icon_url' in _temp):
                            pass
                        elif ('icon_url' in _temp or 'image' in _temp) and 'text' not in _temp:
                            embed.set_author(icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']])

                        elif not ('icon_url' in _temp or 'image' in _temp) and 'text' in _temp:
                            embed.set_author(
                                name=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                                 guild=member.guild))

                        elif 'icon_url' in _temp and ('icon_url' in _temp or 'image' in _temp):
                            embed.set_author(
                                icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']],
                                name=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                                 guild=member.guild)
                            )
                        else:
                            pass

                    fields = []
                    for key in _embed.keys():
                        try:
                            fields.append(int(key))
                        except ValueError:
                            continue
                    for field in fields:
                        try:
                            name = _embed[field]['name'].format(member=member, user=member, server=member.guild,
                                                                guild=member.guild)
                            value = _embed[field]['value'].format(member=member, user=member, server=member.guild,
                                                                  guild=member.guild)
                        except KeyError:
                            continue
                        if 'inline' in _embed[field]:
                            if not _embed[field]['inline']:
                                inline = False
                            else:
                                inline = True
                        else:
                            inline = True
                        embed.add_field(name=name, value=value, inline=inline)

                    await _channel.send(embed=embed)

            except Exception:
                return

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        cls_c = self.cache.cache

        if member.guild.id not in cls_c['jl']:
            return

        _data = cls_c['jl'][member.guild.id]
        _channel = self.bot.get_channel(_data['leave_c'])

        if not _channel:
            return

        message = _data['leave_m']
        if not message or message == 'Not Set.':
            return
        try:
            _message = message.replace('\'', '"')
            _embed = json.loads(_message)
        except Exception:
            _embed = False

        try:
            if not _embed:
                parsed_message = message.format(member=member, user=member, guild=member.guild, server=member.guild)
                await _channel.send(parsed_message)
            else:
                embed = discord.Embed()
                keys = {k.lower(): k for k in _embed.keys()}

                if 'title' in keys:
                    _key = keys['title']
                    print(_key)
                    embed.title = _embed[_key].format(member=member, user=member, server=member.guild,
                                                      guild=member.guild)

                if 'description' in keys or 'desc' in keys:
                    _key = keys['description' if 'description' in keys else 'desc']
                    embed.description = _embed[_key].format(member=member, user=member, server=member.guild,
                                                            guild=member.guild)

                if 'colour' in keys or 'color' in keys:
                    _colour = keys['colour' if 'colour' in keys else 'color']
                    try:
                        _colour = _embed[_colour].replace('#', '0x')
                        _colour = int(_colour, 16)
                    except Exception:
                        _colour = discord.Colour.default()
                    embed.colour = _colour

                if 'timestamp' in keys or 'time' in keys:
                    _key = keys['timestamp' if 'timestamp' in keys else 'time']
                    if _key:
                        embed.timestamp = datetime.datetime.utcnow()

                if 'thumbnail' in keys or 'thumb' in keys:
                    _url = keys['thumbnail' if 'thumbnail' in keys else 'thumb']
                    try:
                        embed.set_thumbnail(url=_url)
                    except Exception:
                        pass

                if 'image' in keys or 'img' in keys:
                    _url = keys['image' if 'image' in keys else 'img']
                    try:
                        embed.set_image(url=_url)
                    except Exception:
                        pass

                if 'footer' in keys:
                    _mini = keys['footer']
                    _temp = {k.lower(): k for k in _mini.keys()}
                    if 'text' not in _temp or not ('image' in _temp or 'icon_url' in _temp):
                        pass
                    elif ('icon_url' in _temp or 'image' in _temp) and 'text' not in _temp:
                        embed.set_footer(icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']])

                    elif not ('icon_url' in _temp or 'image' in _temp) and 'text' in _temp:
                        embed.set_footer(
                            text=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                             guild=member.guild))

                    elif 'icon_url' in _temp and ('icon_url' in _temp or 'image' in _temp):
                        embed.set_footer(
                            icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']],
                            text=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                             guild=member.guild)
                        )
                    else:
                        pass

                if 'author' in keys:
                    _mini = keys['author']
                    _temp = {k.lower(): k for k in _mini.keys()}
                    if 'text' not in _temp or not ('image' in _temp or 'icon_url' in _temp):
                        pass
                    elif ('icon_url' in _temp or 'image' in _temp) and 'text' not in _temp:
                        embed.set_author(icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']])

                    elif not ('icon_url' in _temp or 'image' in _temp) and 'text' in _temp:
                        embed.set_author(
                            name=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                             guild=member.guild))

                    elif 'icon_url' in _temp and ('icon_url' in _temp or 'image' in _temp):
                        embed.set_author(
                            icon_url=_mini[_temp['icon_url' if 'icon_url' in _temp else 'image']],
                            name=_mini[_temp['text']].format(member=member, user=member, server=member.guild,
                                                             guild=member.guild)
                        )
                    else:
                        pass

                fields = []
                for key in _embed.keys():
                    try:
                        fields.append(int(key))
                    except ValueError:
                        continue
                for field in fields:
                    try:
                        name = _embed[field]['name'].format(member=member, user=member, server=member.guild,
                                                            guild=member.guild)
                        value = _embed[field]['value'].format(member=member, user=member, server=member.guild,
                                                              guild=member.guild)
                    except KeyError:
                        continue
                    if 'inline' in _embed[field]:
                        if not _embed[field]['inline']:
                            inline = False
                        else:
                            inline = True
                    else:
                        inline = True
                    embed.add_field(name=name, value=value, inline=inline)

                await _channel.send(embed=embed)

        except Exception:
            return

def setup(bot):
    bot.add_cog(JoinLeave(bot))
