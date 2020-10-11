import discord
from discord.ext import commands
from discord.ext.commands import BucketType
import json
import os

os.chdir('C:\\Users\\isa1b.DESKTOP-GMQ5DPV.000.001\\PycharmProjects\\Discord Bot')

class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cp'])
    @commands.is_owner()
    async def change_prefix(self, ctx, *, prefix=None):
        if prefix == None:
            await ctx.send('You cannot set the prefix as nothing!')
        elif len(list(prefix)) > 20:
            await ctx.send("The server's prefix cannot be bigger than `5` Letters!")
        else:
            with open('JSON/prefixes.json', 'r') as f:
                prefixes = json.load(f)

            prefixes[str(ctx.guild.id)] = prefix

            with open('JSON/prefixes.json', 'w') as f:
                json.dump(prefixes, f, indent=4)
            await ctx.send('The new prefix for Mecha Karen is **`{}`**'.format(prefix))

    @commands.command()
    async def prefix(self, ctx):
        with open('JSON/prefixes.json', 'r') as f:
            prefixes = json.load(f)
        prefix = prefixes[str(ctx.guild.id)]
        await ctx.send('The prefix for the server **`{}`** is **`{}`**'.format(ctx.guild.name, prefix))

    @commands.command(aliases=['sw', 'set_wel', 'set_w'])
    async def set_welcome(self, ctx, channel : discord.TextChannel=None):
        if channel == None:
            await ctx.send('You havent provided a valid channel!')
        else:
            with open('JSON/welcome.json', 'r') as f:
                welcome_id = json.load(f)
            welcome_id[str(ctx.guild.id)] = f'{channel.id}'
            with open('JSON/welcome.json', 'w') as f:
                json.dump(welcome_id, f, indent=4)
            await ctx.send(f'The welcomes channel has been set as `{channel.name}`.')

    @commands.command(aliases=['rw', 'remove_w', 'r_welcome'])
    async def remove_welcome(self, ctx):
        with open('JSON/welcome.json', 'r') as f:
            welcome_id = json.load(f)
        welcome_id[str(ctx.guild.id)] = f'Not Set'
        with open('JSON/welcome.json', 'w') as f:
            json.dump(welcome_id, f, indent=4)
        await ctx.send(f'You have removed the welcome messages!')

    @commands.command(aliases=['cog'])
    async def cogs(self, ctx):
        cog = []
        index = 0
        for filename1 in os.listdir('./cogs'):
            if filename1.endswith('.py'):
                cog.append(filename1[:-3])
        if 'loadup' in cog:
            x = cog.index('loadup', 0, -1)
            cog.pop(x)
        if 'Error Handling' in cog:
            x = cog.index('Error Handling', 0, -1)
            cog.pop(x)
        if 'HelpCommands' in cog:
             x = cog.index('HelpCommands', 0, -1)
             cog.pop(x)
        if 'HelpCommands' in cog:
            x = cog.index('HelpCommands', 0, -1)
            cog.pop(x)
        if 'Management' in cog:
            x = cog.index('Management', 0, -1)
            cog.pop(x)
        if 'Reports and Suggestions' in cog:
            x = cog.index('Reports and Suggestions', 0, -1)
            cog.pop(x)
        if 'Events' in cog:
            x = cog.index('Events', 0, -1)
            cog.pop(x)
        for element in cog:
            cog.insert(index, f'{index + 1}.\t' + cog[index] + '\n')
            cog.pop(index + 1)
            index += 1
        x = ''.join(map(str, cog))
        embed = discord.Embed(
            title=f'Mecha Karen currently has {index} cogs!',
            color=discord.Color.red(),
            description=x
        )
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 50000, BucketType.user)
    async def suggest(self, ctx, *args):
        if ctx.author.id == 300074149878038539:
            await ctx.send('You have been banned from sending requests!')
        elif ctx.author.id == 708548079196045363:
            await ctx.send('You have been banned from sending requests!')
        else:
            channel = self.bot.get_channel(753704717254918214)
            x = ' '.join(map(str, args))
            embed = discord.Embed(
                title=f"{ctx.author}'s Suggestion!",
                color=discord.Color.red(),
                description=f'The user **`{ctx.author}`** is from **`{ctx.guild}`**.'
            )
            embed.add_field(name=f'Description!', value=f'{x}')
            embed.set_footer(text=f'User ID: {ctx.author.id}\nGuild ID: {ctx.guild.id}')
            msg = await channel.send(embed=embed)
            await msg.add_reaction('👍')
            await msg.add_reaction('👎')
            await ctx.send('You suggestion has been sent')

    @commands.command()
    @commands.cooldown(1, 50000, BucketType.user)
    async def report(self, ctx, *args):
        counter = random.randint(1, 1000)
        channel = self.bot.get_channel(754048733481795596)
        x = ' '.join(map(str, args))
        if x == None:
            await ctx.send('You going to report nothing?')
        else:
            embed = discord.Embed(
                title=f'Report #{counter}',
                color=discord.Color.red(),
                description=f'The user `{ctx.author}` from the guild `{ctx.guild}` has sent a report on Mecha Karen!'
            )
            embed.add_field(name='Query?', value=f'{x}')
            embed.set_footer(text=f'User ID: {ctx.author.id}\nGuild ID: {ctx.guild.id}')
            await channel.send(embed=embed)
            await ctx.send(f'Your report has successfully been sent!')

def setup(bot):
    bot.add_cog(Management(bot))
