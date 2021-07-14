import discord
from discord.ext import commands
from binascii import hexlify
import os
import datetime
import random
import aiofiles
from io import BytesIO
import json

class Owner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.client = bot.client
        bot.token_handler = client

    @commands.Cog.listener()
    async def on_ready(self):
        for user in self.bot.blacklistedusers.find():
            self.bot.blacklist_cache['users'].update({user['_id']: True})
        for guild in self.bot.blacklistedguilds.find():
            self.bot.blacklist_cache['guilds'].update({guild['_id']: True})

    @commands.command(aliases=['bl'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.is_owner()
    async def blacklist(self, ctx, mode: str, _id: int):
        if mode.lower() in ['guilds', 'guild', 'g']:
            _check = self.bot.blacklistedguilds.find_one({'_id': _id})
            if not _check:
                self.bot.blacklistedguilds.insert_one({'_id': _id})
                self.bot.blacklist_cache['guilds'].update({ctx.guild.id: True})
                if _id in [i.id for i in self.bot.guilds]:
                    _temp = self.bot.get_guild(_id)
                    await _temp.leave()
                    return await ctx.send(f'Successfully blacklisted guild **{_temp.name}**, and left there server.')
                return await ctx.send(f'Blacklisted guild with the ID **{_id}** from using Mecha Karen.')
            await ctx.send('Guild with this ID has already been blacklisted!')

        elif mode.lower() in ['user', 'u', 'users']:
            _check = self.bot.blacklistedusers.find_one({'_id': _id})
            if not _check:
                self.bot.blacklistedusers.insert_one({'_id': _id})
                self.bot.blacklist_cache['users'].update({ctx.author.id: True})
                if _id in [i.id for i in self.bot.users]:
                    _temp = self.bot.get_user(_id)
                    return await ctx.send(f'Blacklisted user {_temp.mention} from using Mecha Karen.')
                return await ctx.send(f'Blacklisted user with the ID **{_id}** from using Mecha Karen.')
            await ctx.send('User with this ID has already been blacklisted!')

        else:
            await ctx.send('Invalid option given!')

    @commands.command(aliases=['ubl'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.is_owner()
    async def unblacklist(self, ctx, mode: str, _id: int):
        if mode.lower() in ['guilds', 'guild', 'g']:
            _check = self.bot.blacklistedguilds.find_one({'_id': _id})
            if _check:
                self.bot.blacklistedguilds.delete_one({'_id': _id})
                return await ctx.send(f'Guild with the ID, **{_id}** can now use, Mecha Karen.')
            await ctx.send('Guild with this ID isn\'t blacklisted.')

        elif mode.lower() in ['user', 'u', 'users']:
            _check = self.bot.blacklistedusers.find_one({'_id': _id})
            if _check:
                self.bot.blacklistedusers.delete_one({'_id': _id})
                if _id in [i.id for i in self.bot.users]:
                    _temp = self.bot.get_user(_id)
                    return await ctx.send(f'User {_temp.mention}, can now re-use Mecha Karen.')
                return await ctx.send(f'User with ID **{_id}**, can now re-use Mecha Karen.')
            await ctx.send('User with this ID isn\'t blacklisted.')

        else:
            await ctx.send('Invalid option given!')

    @commands.command(aliases=['bls'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.is_owner()
    async def blacklists(self, ctx, mode: str, page: int = 1):
        _end = page * 10
        if mode.lower() in ['user', 'u', 'users']:
            totals = []
            for collection in self.bot.blacklistedusers.find():
                _temp = self.bot.get_user(collection['_id'])
                if not _temp:
                    totals.append(collection['_id'])
                else:
                    totals.append(_temp.mention + f' ({_temp.id})')

            totals = list(map(str, totals))[_end-10:_end]
            embed = discord.Embed(title='10 Of Each Blacklisted User', color=discord.Colour.red())
            embed.description = '\n'.join(totals)
            await ctx.send(embed=embed)

        elif mode.lower() in ['guilds', 'g', 'guild']:
            totals = []
            for collection in self.bot.blacklistedguilds.find():
                totals.append(collection['_id'])

            totals = list(map(str, totals))[_end-10:_end]
            embed = discord.Embed(title='10 Of Each Blacklisted Guild', color=discord.Colour.red())
            embed.description = '\n'.join(totals)
            await ctx.send(embed=embed)

        else:
            await ctx.send('Invalid option provided.')
        
    @commands.group(invoke_without_command=True)
    @commands.is_owner()
    async def config(self, ctx):
        loaded_cogs = [((i.split('.')[1]) + '.py') for i in self.bot.extensions.keys()]
        unloaded = []
        cogs = 0
        for file in os.listdir('./src'):
            if file != '__pycache__':
                cogs += 1
                if file not in loaded_cogs:     unloaded.append(file)
        embed = discord.Embed(title='Loaded Cogs & Commands:', colour=discord.Colour.red())
        embed.add_field(name='Cogs:', value='**Total:** `{}`\n**Loaded:** `{}`\n**Unloaded:** `{}`\n**Unloaded:** {}'.format(cogs, len(loaded_cogs), len(unloaded), (', '.join(unloaded) or 'None!')))
        loaded, unloaded, _commands = 0, 0, []
        for cmd in self.bot.commands:
            if not cmd.enabled:    unloaded += 1; _commands.append(cmd.name)
            else:   loaded += 1
        embed.add_field(name='Commands:', value='**Total:** `{}`\n**Loaded:** `{}`\n**Unloaded:** `{}`\n**Unloaded:** {}'.format(len(self.bot.commands), loaded, unloaded, (''.join(_commands) or 'None!')), inline=False)

        await ctx.send(embed=embed)

    @config.command()
    @commands.is_owner()
    async def help(self, ctx):
        return await ctx.send("""\
```
About: Developer commands that help speed the development of the bot.

Default: -Config
[ + ] Displays the total amount of commands / cogs which the bot is using
      - Shows how many are available for use and how many are down
      - Shows which ones are down. If applicable
      
Cogs: -Config Cog <STOP|RUN|RELOAD|SLEEP> <COG-NAME>
[ + ] Execute a command on a certain cog
	  - RUN -> Loads an unloaded cog to the bot
      - STOP -> Unloads a loaded cog from the bot
      - RELOAD -> Reloads a loaded cog from the bot
      - SLEEP -> Shuts down a cog for a certain duration
      	$SLEEP-FORMAT = -Config Cog Sleep owner, <SECONDS>

Commands: -Config Command <UPDATE|REMOVE|DISABLE|ENABLE>
[ + ] Execute a command on a bot command
	  - UPDATE -> Replace the command source code with the new code provided
      - REMOVE -> Deletes the command from the bot
      - DISABLE -> Stops the command from being ran (GLOBAL)
      - ENABLE -> Allows a disabled command to be ran again (GLOBAL)
      - RELOAD -> Reloads the command, replacing the old source code with the newer source code
      - SLEEP -> Stops a command from being ran for a duration; format same as cog
        ```""")
    
    @config.command()
    @commands.is_owner()
    async def cog(self, ctx, action: str, *, cog: str):
        actions = ['stop', 'run', 'reload', 'sleep']

        if action.lower() not in actions:
            return await ctx.send('Invalid action provided. Use one of the following options:\n`{}`'.format(' | '.join(actions)))

        if action.lower() == 'sleep':
            check = cog.split(',')[0]
        else:
            check = cog

        if action.lower() == 'stop':

            try:
                self.bot.unload_extension('src.%s' % cog)
            except Exception:
                return await ctx.send('This cog hasn\'t been loaded.')

            await ctx.send('Action was a success. Cog **%s** has stopped running.' % cog)

        elif action.lower() == 'run':

            try:
                self.bot.load_extension('src.%s' % cog)
            except Exception as error:
                with BytesIO() as file:
                    trace = __import__('traceback').format_exception(etype=type(error), value=error, tb=error.__traceback__)
                    file.write(bytes(''.join(trace).encode('ascii')))
                    file.seek(0)
                    
                    error_file = discord.File(fp=file, filename='error.log')
                    
                return await ctx.send('This cog is already running or has an error located in it. The error file is attached below.', file=error_file)

            await ctx.send('Action was a success. Cog **%s** is now running.' % cog)

        elif action.lower() == 'reload':

            try:
                self.bot.reload_extension('src.%s' % cog)
            except Exception as error:
                with BytesIO() as file:
                    trace = __import__('traceback').format_exception(etype=type(error), value=error, tb=error.__traceback__)
                    file.write(bytes(''.join(trace).encode('ascii')))
                    file.seek(0)
                    
                    error_file = discord.File(fp=file, filename='error.log')
                    
                return await ctx.send('This cog isn\'t running or has an error located in it. The error file is attached below.', file=error_file)

            await ctx.send('Action was a success. Cog **%s** has been reloaded.' % cog)

        else:

            try:
                self.bot.unload_extension('cogs.%s' % cog.split(',')[0])
            except Exception:
                return await ctx.send('This cog hasn\'t been loaded.')

            message = await ctx.send('Preparing to de-activate this cog for **%s** Seconds.' % cog.split(',')[-1])

            try:
                await asyncio.sleep(int(cog.split(',')[-1].strip()))
            except ValueError:
                return await message.edit(content='Time to sleep must be a number.')

            self.bot.load_extension('cogs.%s' % cog.split(',')[0])

            await message.edit(content='%s. Cog %s has exited the state of "SLEEPING". It can now be re-used.' % (ctx.author.mention, cog.split(',')[0]))
    
    @config.command()
    @commands.is_owner()
    async def command(self, ctx, action: str, *, command: str):
        bot_commands = {cmd.name.lower(): cmd for cmd in self.bot.commands}
        command = bot_commands.get(command.lower())
        if not command:
            return await ctx.send('This command doesn\'t exist.')
        actions = ['remove', 'disable', 'enable', 'reload', 'update', 'sleep']
        
        if not action.lower() in actions: 
            return await ctx.send('Invalid action provided, choose from: `{}`'.format(' | '.join(actions)))
        
        if action.lower() == 'remove':
            self.bot.remove_command(command.name)
            return await ctx.send('This command has been removed from the bot.')
        
        elif action.lower() == 'disable':
            if not command.enabled:
                return await ctx.send('This command is already disabled.')
            command.enabled = False
            return await ctx.send('This command has been disabled and can no be used until enabled.')
        
        elif action.lower() == 'enable':
            if command.enabled:
                return await ctx.send('This command is already enabled.')
            command.enabled = True
            return await ctx.send('This command has been enabled and can be used again.')
            
    @commands.command()
    async def version(self, ctx, new: str = None):
        if not new:
            file = await aiofiles.open('./core/version.py', 'r')
            contents = await file.read()
            await file.close()
            await ctx.send('Mecha Karen is currently running off of version `{}`'.format(contents.split('=')[-1].split("\"")[1]))
            
        if not ctx.author.id == self.bot.owner_id:
            return await ctx.send('You do not own this bot!')
        if not new:
            return
        
        async with aiofiles.open('./core/version.py', 'w') as file:
            await file.write('__version__ = "%s"' % new)
        return await ctx.send('New version has been set to **%s**.' % new)

    @commands.command()
    @commands.is_owner()
    @commands.bot_has_guild_permissions(send_messages=True)
    async def view(ctx, error_code: str):
        with open('./storage/storage/errors.json', 'r') as f:
            data = json.load(f)
        try:
            code = data.pop(error_code)
            with open('./storage/storage/errors.json', 'w') as f:
                json.dump(data, f, indent=4)

            embed = discord.Embed(title='Command: ' + code['Command'], colour=discord.Colour.red())
            embed.add_field(name='Exception Type:', value=code['Error Type'])
            embed.add_field(name='Description:', value=code['Shortened Error'], inline=False)
            await ctx.send(embed=embed)

        except KeyError:
            return await ctx.send('That error code doesn\'t exist')
    
def setup(bot):
    bot.add_cog(Owner(bot))
