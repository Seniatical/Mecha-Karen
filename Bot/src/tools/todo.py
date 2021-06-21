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

import datetime
import typing
import asyncio
import discord
from discord.ext import commands
from durations import Duration

class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.tasks = bot.client['todo']['tasks']
        self.member = commands.MemberConverter()

    async def convert(self, seconds: int) -> str:
        hours = seconds // (60 * 60)
        seconds %= (60 * 60)
        minutes = seconds // 60
        if hours != 0 and seconds != 0 and minutes != 0:
            return f'{hours} Hour(s), {minutes} Minute(s) and {seconds} Second(s)'
        if hours != 0 and minutes != 0:
            return f'{hours} Hour(s) and {minutes} Minute(s)'
        if minutes != 0 and seconds != 0:
            return f'{minutes} Minute(s) and {seconds} Second(s)'
        if minutes != 0:
            return f'{minutes} Minute(s)'
        return f'{seconds} Second(s)'
    
    @commands.group(invoke_without_command=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def todo(self, ctx, number: str = None, user: discord.Member = None):
        user = user or ctx.author
        
        try:
            number = int(number)
        except (ValueError, TypeError):
            try:
                user = await self.member.convert(ctx, number)
            except Exception:
                number = None
            number = None

        uncleansed = self.tasks.find_one({'_id': user.id})
        if not uncleansed:
            return await ctx.send('```There are currently no tasks on {}\'s todo list \U0001f973```'.format(user.display_name))
        iter_data = uncleansed['tasks']

        if number:
            index = number
            if len(str(index)) < 3:
                num = '0' * (3 - len(str(index)))
                num += str(index)
            else:
                num = str(index)
            
            try:
                return await ctx.send('{}\'s todo List:```'.format(user.display_name) + f'{num} | {iter_data[(index - 1)]}\n```')
            except IndexError:
                return await ctx.send('This task number doesn\'t exist.')
            
        for iter in iter_data:
            index = iter_data.index(iter, 0)
            if len(str(index)) < 3:
                num = '0' * (3 - len(str(index + 1)))
                num += str(index + 1)
            else:
                num = str(index + 1)

            iter_data[index] = '%s | ' % num + iter

        new = '\n'.join(iter_data)
        await ctx.send('{}\'s todo List:```\n'.format(user.display_name) + '\n' + new + '\n```')

    @todo.command(aliases=['+'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def add(self, ctx, *, new_todo):
        if len(new_todo) > 100:
            await ctx.send('Warning: Your todo task was larger than 100 characters. We have scaled it down automatically.')
            new_todo = new_todo[:100]
        
        current_todos = self.tasks.find_one({'_id': ctx.author.id})
        if not current_todos:
            query = {'_id': ctx.author.id, 'tasks': [new_todo]}
        else:
            if len(current_todos['tasks']) == 15:
                return await ctx.send('You have reached the limit of todo\'s on your list. If you would like to have more consider purchasing premium.')
            query = current_todos
            for todo in query['tasks']:
                if todo.lower().strip() == new_todo.lower().strip():
                    return await ctx.send('This todo is already on your list. Task number #%d' % (query['tasks'].index(todo) + 1))
            
            query['tasks'].append(new_todo)

        if not current_todos:
            self.tasks.insert_one(query)
        else:
            self.tasks.update_one({'_id': ctx.author.id}, {'$set': {'tasks': query['tasks']}})

        await ctx.send('Added this to your todo list. Task #%s.' % len(query['tasks']))

    @todo.command(aliases=['modify'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def edit(self, ctx, task_number: str, *, new_todo):
        try:
            number = int(task_number)
        except (ValueError, TypeError):
            return await ctx.send('Make sure the task number is actually a number.')

        todos = self.tasks.find_one({'_id': ctx.author.id})
        if not todos:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')
        
        if len(new_todo) > 100:
            await ctx.send('Warning: Your todo task was larger than 100 characters. We have scaled it down automatically.')
            new_todo = new_todo[:100]
        
        iter_data = todos['tasks']
        index = number
        if len(str(index)) < 3:
            num = '0' * (3 - len(str(index)))
            num += str(index)
        else:
            num = str(index)

        try:
            selected_todo = iter_data[(index - 1)]
            for todo in iter_data:
                if todo.lower().strip() == new_todo.lower().strip():
                    return await ctx.send('This todo is already on your list. Task number #%d' % (iter_data.index(selected_todo) + 1))
            
            iter_data[(index - 1)] = new_todo
        except IndexError:
            return await ctx.send('This task number doesn\'t exist.')

        self.tasks.update_one({'_id': ctx.author.id}, {'$set': {'tasks': iter_data}})

        await ctx.send('```Updated todo task #%s\n\nBefore:\n%s\n\n+After:\n%s```' % (num, selected_todo, new_todo))

    @todo.command(aliases=['remove', 'check', '-'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def done(self, ctx, task_number: str):
        try:
            number = int(task_number)
        except (ValueError, TypeError):
            return await ctx.send('Make sure the task number is actually a number.')

        uncleansed = self.tasks.find_one({'_id': ctx.author.id})
        if not uncleansed:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')
        iter_data = uncleansed['tasks']
        
        index = number
        if len(str(index)) < 3:
            num = '0' * (3 - len(str(index)))
            num += str(index)
        else:
            num = str(index)

        try:
            checked = iter_data.pop((index - 1))
        except IndexError:
            return await ctx.send('This task number doesn\'t exist.')
            
        self.tasks.update_one({'_id': ctx.author.id}, {'$set': {'tasks': iter_data}})
        
        return await ctx.send('This todo has been checked off\n```\n' + f'{num} | {checked}\n```')
    
    @todo.command(aliases=['+='])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def append(self, ctx, task_number: str, *, add_on):
        try:
            number = int(task_number)
        except (ValueError, AttributeError):
            return await ctx.send('The task number must actually be a number.')
        
        todos = self.tasks.find_one({'_id': ctx.author.id})
        
        if not todos:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')
        
        todos = todos['tasks']
        
        index = number
        if len(str(index)) < 3:
            num = '0' * (3 - len(str(index)))
            num += str(index)
        else:
            num = str(index)

        try:
            current_todo = todos[(index - 1)]
        except IndexError:
            return await ctx.send('This task number doesn\'t exist.')
        
        if (len(add_on) + len(current_todo)) > 100:
            await ctx.send('Warning: Your todo task was larger than 100 characters. We have scaled it down automatically.')
            add_on = add_on[:(100 - len(current_todo))]
        todos[(index - 1)] = (current_todo + add_on)
        
        self.tasks.update_one({'_id': ctx.author.id}, {'$set': {'tasks': todos}})
        
        await ctx.send('Added text to todo task #%s```Before:\n%s\n\n+After:\n%s```' % (num, current_todo, (current_todo + add_on)))

    @todo.command(aliases=['clear', 'delete'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def reset(self, ctx):
        todos = self.tasks.find_one({'_id': ctx.author.id})

        if not todos:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')

        msg = await ctx.send('Are you sure you would like to clear your todo list. (**%s** tasks)' % len(todos['tasks']))

        try:
            check = await self.bot.wait_for('message', check=lambda m: m.author.id == ctx.author.id and m.channel.id == ctx.channel.id and m.content.lower() in ['y', 'n', 'yes', 'no'], timeout=30.0)
        except Exception:
            return await msg.edit(content='Failed to recieve a response, Cancelling request.')

        if check.content.lower() in ['n', 'no']:
            return await msg.edit(content='Cancelling request.\n> **Reason:** User cancelled operation.')

        else:
            self.tasks.delete_one({'_id': ctx.author.id})

        return await msg.edit(content='Successfully cleared all todos from your list! (**%s** tasks)' % len(todos['tasks']))
    
    @todo.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def highlight(self, ctx, task_number: str):
        todos = self.tasks.find_one({'_id': ctx.author.id})

        if not todos:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')
        
        try:
            task_number = int(task_number)
        except (ValueError, AttributeError):
            return await ctx.send('The task number must actually be a number.')
        
        todos = todos['tasks']
        try:
            todo = todos[(task_number - 1)]
        except IndexError:
            return await ctx.send('Task number not found!')
        
        if todo.endswith(' [HIGHLIGHTED]'):
            todo = todo[:-len(' [HIGHLIGHTED]')]
            message = 'I have removed the highlight tag from your todo.'
        else:
            todo += ' [HIGHLIGHTED]'
            message = 'I have added the highlight tag to your todo.'
        
        todos[(task_number - 1)] = todo
        
        self.tasks.update_one({'_id': ctx.author.id}, {'$set': {'tasks': todos}})
        return await ctx.send(message)
    
    @todo.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def move(self, ctx, move_from, move_to):
        todos = self.tasks.find_one({'_id': ctx.author.id})

        if not todos:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')
        
        try:
            move_from, move_to = int(move_from), int(move_to)
        except (ValueError, AttributeError):
            return await ctx.send('Move to/from must be the task numbers.')
        
        if move_to <= 0:
            return await ctx.send('Cannot move to task to or below 0. Perhaps you ment 1.')
        
        if move_to > len(todos['tasks']):
            return await ctx.send('Cannot move a task to a number which doesn\'t exist.')
        
        todos = todos['tasks']
        
        try:
            movefromvalue = todos[(move_from - 1)]
        except IndexError:
            return await ctx.send('The task number to move cannot be found.')
        movetovalue = todos[(move_to - 1)]
        
        todos.pop((move_from - 1))
        todos.insert((move_to - 1), movefromvalue)
        
        self.tasks.update_one({'_id': ctx.author.id}, {'$set': {'tasks': todos}})
        
        return await ctx.send('```\nMoved task #{} to #{}.```'.format(move_from, move_to))
    
    @todo.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def deadline(self, ctx, task_number: str, *, duration: str):
        todos = self.tasks.find_one({'_id': ctx.author.id})

        if not todos:
            return await ctx.send('```There are currently no tasks on your todo list \U0001f973```')
        
        try:
            task_index = int(task_number)
        except ValueError:
            return await ctx.send('The task number must actually be a number.')
        
        try:
            task = todos['tasks'][task_index - 1]
        except IndexError:
            return await ctx.send('This task doesn\'t exist!')
        
        try:
            dur = Duration(duration)
        except Exception:
            return await ctx.send('Failed to parse the duration for the deadline.')
        time_to_rest = dur.to_seconds()
        message = await ctx.send('I will remind you after %s' % await self.convert(time_to_rest))
        await asyncio.sleep(time_to_rest)
        await message.edit(content='%s, Looks like your deadline for task **%s** is over!\n```%s```' % (ctx.author.mention, task_index, task))
    
def setup(bot):
    bot.add_cog(Todo(bot))
