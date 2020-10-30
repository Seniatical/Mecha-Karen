import discord
from discord.ext import commands
import os
import json
from PIL import *

class events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        with open('JSON/welcome.json', 'r') as f:
            channel = json.load(f)
        if channel[str(member.guild.id)] == 'Not Set':
            return
        else:
            channel = int(channel[str(member.guild.id)])
            channel = self.bot.get_channel(int(channel))
            if channel.name not in member.guild.channels and member not in channel.guild.members:
                pass
            else:
                avatar = member.avatar_url_as(format=None,static_format='png',size=1024)
                await avatar.save('./Images/Avatar.png')
                im = Image.open(r'./Images/Avatar.png').convert('RGB')
                im = im.resize((120, 120));
                bigsize = (im.size[0] * 3, im.size[1] * 3)
                mask = Image.new('L', bigsize, 0)
                draw = ImageDraw.Draw(mask)
                draw.ellipse((0, 0) + bigsize, fill=255)
                mask = mask.resize(im.size, Image.ANTIALIAS)
                im.putalpha(mask)

            output = ImageOps.fit(im, mask.size, centering=(10, 10))
            output.putalpha(mask)
            output.save('./Images/output.png')

            background = Image.open('./Images/welcome.png').convert('RGB')
            background.paste(im, (149, 12), im)
            background.save('./Images/overlap.png')
            await channel.send(file=discord.File('./Images/overlap.png'))
            a = list(str(len(member.guild.members)))
            if '1' in a[-1]:
                ending = 'ˢᵗ'
            elif '2' in a[-1]:
                ending = 'ⁿᵈ'
            elif '3' in a[-1]:
                ending = 'ʳᵈ'
            else:
                ending = 'ᵗʰ'
            await channel.send('Welcome {} to {}. You are our {}{} member!'.format(member.mention, member.guild.name, len(member.guild.members), ending))
        if member.guild.id == 740523643980873789:
            role = discord.utils.get(member.guild.roles, name="Supporters")
            await member.add_roles(role)
        elif member.guild.id == 650556537387089921:
            role = discord.utils.get(member.guild.roles, name='Sosa')
            await member.add_roles(role)
        else:
            pass

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = self.bot.get_channel(740941457841586219)
        if channel not in member.guild.channels:
            pass
            return
        await channel.send(f'{member} has left {member.guild}!')

def setup(bot):
    bot.add_cog(events(bot))
