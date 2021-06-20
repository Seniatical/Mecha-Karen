import discord
from discord.ext import commands, ipc
import datetime
import time as tme
from utility import abbrev_denary

class Constructor:
    pass

class Dashboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.bot.ipc.update_endpoints()

        self.last_logged = {
            'joins': {},
            }

    @ipc.server.route()
    async def leave_guild(self, data):
        guild_id = data.guild_id
        guild = self.bot.get_guild(int(guild_id))
        if not guild:
            return {'error': 404, 'message': 'Mecha Karen is not in this server'}
        await guild.leave()
        return {'status': 200, 'u': 'OK'}
        
    @ipc.server.route()
    async def get_guild_info(self, data):
        guild = self.bot.get_guild(int(data.guild_id))
        if not guild:
            return {'error': 404, 'message': 'Cannot find this guild'}
        
        return {
            'members': guild.member_count,
            'owner': {
                'id': guild.owner.id,
                'name': str(guild.owner),
                'avatar': str(guild.owner.avatar)
                },
            'created_at': guild.created_at.strftime("%a, %#d %b %Y, %I:%M %p"),
            'channels': {
                'total': len(guild.channels),
                'text': len(guild.text_channels),
                'voice': len(guild.voice_channels),
                'category': len(guild.categories)
                },
            'boosts': guild.premium_subscription_count,
            }

    @ipc.server.route()
    async def has_access(self, data):
        guild = self.bot.get_guild(int(data.guild_id))
        if not guild:
            return {'error': 404, 'message': 'Cannot find this guild'}
        member = guild.get_member(int(data.user_id))

        if not member:
            return {'error': 404, 'message': 'Cannot find this member'}
        
        return {'has_access': member.guild_permissions.manage_guild}

    @ipc.server.route()
    async def get_name(self, data):
        guild_id = int(data.guild_id)

        return {'name': self.bot.get_guild(guild_id).name}

    @ipc.server.route()
    async def get_member_joins(self, data):
        guild_id = int(data.guild_id)
        guild = self.bot.get_guild(guild_id)

        logged = self.last_logged['joins'].get(guild_id)
        if logged and guild.members == logged['guild'].members:
            return logged['data']
        
        joins = []
        for i in range(30):
            try:
                delta = datetime.date(day=(i + 1), month=datetime.datetime.utcnow().month, year=datetime.datetime.utcnow().year)
            except ValueError:
                break
            
            joined = sum(datetime.date(day=m.joined_at.day, month=m.joined_at.month, year=m.joined_at.year) == delta for m in guild.members if m.joined_at is not None)

            joins.append(joined)

        self.last_logged['joins'].update({
            'guild': guild,
            'data': {'join': joins}
            }
            )
            
        return {'join': joins}

    @ipc.server.route()
    async def get_prefixes(self, data):
        guild_id = int(data.guild_id)
        guild = self.bot.get_guild(guild_id)
        
        message = Constructor()
        message.guild = Constructor()
        message.guild.id = int(guild.id)
        
        prefixes = await self.bot.prefix(self.bot, message)

        voice = guild.me.voice
        if voice:
            channel = {
                'name': voice.channel.name,
                'users': len(voice.channel.members),
                'region': str(voice.channel.rtc_region) if str(voice.channel.rtc_region) != 'None' else 'Automatic',
                'bitrate': abbrev_denary(voice.channel.bitrate),
                'category': getattr(voice.channel.category, 'name', None) or 'N/A'
                }
        else:
            channel = None
        
        return {
                'prefixes': list(prefixes),
                'joined_at': guild.me.joined_at.strftime("%a, %#d %b %Y, %I:%M %p"),
                'premium': False,
                'nickname': guild.me.nick,
                'voice': channel,
                'mention': prefixes.mention,
            }

    @ipc.server.route()
    async def update_prefix(self, data):
        method = data.action
        prefix = data.prefix
        guild_id = int(data.guild_id)
        guild = self.bot.get_guild(guild_id)

        if not self.bot.get_guild(guild_id):
            return {'error': 'CANNOT FIND SPECIFED GUILD'}

        if method == 'REMOVE':
            message = Constructor()
            message.guild = Constructor()
            message.guild.id = guild_id
                
            prefixes = await self.bot.prefix(self.bot, message)

            if prefixes.mention:
                prefixes = list(prefixes)[2:]
            else:
                prefixes = list(prefixes)

            try:
                prefixes.pop(prefixes.index(prefix, 0))
            except IndexError:
                return {'prefixes': prefixes}
                
            await self.bot.loop.run_in_executor(
                None, self.bot.client['Bot']['Guilds'].update_one,
                {'_id': guild_id}, {'$set': {'prefix': prefixes}}
                )
            self.bot.prefix.cache.pop(guild.id)

            return {'prefixes': prefixes}

        if method == 'ADD':
            message = Constructor()
            message.guild = Constructor()
            message.guild.id = guild_id
                
            prefixes = await self.bot.prefix(self.bot, message)

            if prefixes.mention:
                prefixes = list(prefixes)[2:]
            else:
                prefixes = list(prefixes)

            if len(prefixes) + 1 > 5:
                return {'error': 'MAX LIMIT REACHED'}

            if len(prefix) > 10:
                return {'error': 'PREFIX TOO LARGE'}
            
            prefixes.append(prefix)

            await self.bot.loop.run_in_executor(
                None, self.bot.client['Bot']['Guilds'].update_one,
                {'_id': guild_id}, {'$set': {'prefix': prefixes}}
                )
            self.bot.prefix.cache.pop(guild.id)

            return {'prefixes': prefixes}

        if method == 'MENTION':
            message = Constructor()
            message.guild = Constructor()
            message.guild.id = guild_id
                
            if prefix == 'true':
                await self.bot.loop.run_in_executor(
                    None, self.bot.client['Bot']['Guilds'].update_one,
                    {'_id': guild_id}, {'$set': {'mention': True}}
                    )
            else:
                await self.bot.loop.run_in_executor(
                    None, self.bot.client['Bot']['Guilds'].update_one,
                    {'_id': guild_id}, {'$set': {'mention': False}}
                    )

            try:
                self.bot.prefix.cache.pop(guild.id)
            except KeyError:
                pass

            return {'mention': True if prefix == 'true' else False}

        return {'error': 'UNKNOWN METHOD'}

    @ipc.server.route()
    async def get_channels(self, data):
        guild_id = int(data.guild_id)
        guild = self.bot.get_guild(guild_id)

        channels = {'text': [], 'voice': []}
        for channel in guild.text_channels:
            channels['text'].append({'name': channel.name, 'id': channel.id, 'category': getattr(channel.category, 'name', '')})
        for channel in guild.voice_channels:
            channels['voice'].append({'name': channel.name, 'id': channel.id, 'category': getattr(channel.category, 'name', '')})

        channel = await self.bot.loop.run_in_executor(
            None, self.bot.client['Bot']['Logging'].find_one, {'_id': guild_id}
            )
        if not channel:
            channels['logging'] = None
        else:
            channel = self.bot.get_channel(channel['channel'])
            if not channel:
                channels['logging'] = '#Deleted-Channel'
            else:
                channels['logging'] = channel.name

        channel = await self.bot.loop.run_in_executor(
            None, self.bot.client['Bot']['Guilds'].find_one, {'_id': guild_id}
            )
        count = channel['StarCount']
        channel = channel['StarChannel']

        if not channel:
            channels['starboard'] = None
        else:
            channel = self.bot.get_channel(channel['channel'])
            if not channel:
                channels['starboard'] = '#Deleted-Channel'
            else:
                channels['starboard'] = channel.name
        channels['starboard-stars'] = count

        return channels
        
def setup(bot):
    bot.add_cog(Dashboard(bot))
