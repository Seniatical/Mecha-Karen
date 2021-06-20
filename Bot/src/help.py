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

import discord
from discord.ext import commands
from .passive.handler import convert

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.AutoShardedBot = bot
        aliases = {command: command.aliases for command in self.bot.commands}
        self.aliases = {}

        for k, v in aliases.items():
            for alias in v:
                self.aliases.update({alias: k})

    @commands.group(name='Help', invoke_with_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def help(self, ctx, *, command: str = None):
        if not command:
            embed = discord.Embed(
                description='''\
[Command Documentation](https://docs.mechakaren.xyz/)
[Support Server](https://discord.gg/Q5mFhUM)
[Invite](https://mechakaren.xyz/invite/)
[API Documentation](https://api.mechakaren.xyz/)
                ''',
                colour=discord.Colour.green(),
            )
            embed.set_author(name=ctx.me.display_name, icon_url=ctx.me.avatar)
        else:
            prefix = self.bot.prefix_.cache[ctx.guild.id][-1]

            command = command.lower()

            _command = self.bot.get_command(command.split(' ')[0])
            if not _command:
                _command = self.aliases.get(command)

                if not _command:
                    return await ctx.send(embed=discord.Embed(
                        description='It seems that I cannot find this command!',
                        colour=discord.Colour.red()
                    ))

            embed = discord.Embed(
                title=command.title(),
                url='https://docs.mechakaren.xyz/search.html?q={}'.format(command.replace(' ', '+')),
                colour=discord.Colour.green()
            )

            if type(_command) == commands.Group and len(command.split(' ')) > 1:
                _command = _command.get_command(command.split(' ')[1])
                if not _command:
                    return await ctx.send(embed=discord.Embed(
                        description='The command {!r} does not have this sub command!',
                        colour=discord.Colour.red()
                    ))
                embed.add_field(name='Usage', value=f'''\
```
{prefix}{command.split(' ')[0]} {_command.name.lower()} {_command.signature}
```
''')
            else:
                embed.add_field(name='Usage', value=f'''\
```
{prefix}{command} {_command.signature}
```
''')
            embed.add_field(name='Cooldown', value=await convert(round(_command._buckets._cooldown.per)), inline=False)

            if _command.aliases:
                aliases = ' '.join(map(lambda word: '`' + word + '`', _command.aliases))
            else:
                aliases = 'There are no aliases for this command!'
            
            embed.add_field(name='Aliases', value=aliases, inline=False)

        await ctx.send(embed=embed)

    @commands.command(aliases=['link', 'links'])
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(embed_links=True)
    async def invite(self, ctx: commands.Context) -> discord.Embed:
        embed = discord.Embed(title='🔗 Links', colour=discord.Colour.red())
        embed.set_thumbnail(url=ctx.me.avatar)
        embed.add_field(name='Invite', value="If you wish to invite me, [Click Here](https://mechakaren.xyz/invite)")
        embed.add_field(name='Support Server', value="Need any help with the bot or spot a bug, [Click Me](https://discord.com/invite/Q5mFhUM)")
        embed.add_field(name='Others', value='''\
[Dashboard](https://mechakaren.xyz/login)
[API Homepage](https://api.mechakaren.xyz/)
[API Documentation](https://api.mechakaren.xyz/docs)
[Bot Documentation](https://docs.mechakaren.xyz/)
''', inline=False)
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Help(bot))
