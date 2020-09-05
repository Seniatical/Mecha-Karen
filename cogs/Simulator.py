import discord
from discord.ext import commands
from PIL import Image
import random

class Simulate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('Simulate Cog is ready')

    @commands.command()
    async def Simulate(self, ctx, Animal=None ,member : discord.Member=None):
        if member == None:
            member = ctx.author
        if Animal == None:
            await ctx.send('What animal do you want to be!')
        else:
            await ctx.send(f'{member} will now become a {Animal}.')
        if member == None:
            avatar = ctx.author.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')
        else:
            avatar = member.avatar_url_as(format=None,static_format='jpg',size=1024)
            await avatar.save('./Images/Avatar.jpg')

        if Animal == 'bird':
            im1 = Image.open(f'./Images/{Animal}.jpg')

            img_path = './Images/Avatar.jpg'
            img = Image.open(img_path)

            width, height = img.size
            asp_rat = width/height

            new_width = 180

            new_height = 184

            new_rat = new_width/new_height

            if (new_rat == asp_rat):
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            else:
                new_height = round(new_width / asp_rat)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save("./Images/outputname.jpg", quality=95)

            back_im = im1.copy()
            mrl = Image.open('./Images/outputname.jpg')
            back_im.paste(mrl, (650, 20))
            back_im.save('./Images/bird2.jpg', quality=95)
            await ctx.send(file=discord.File('./Images/bird2.jpg'))
        elif Animal == 'ant':
            im1 = Image.open(f'./Images/{Animal}.jpg')

            img_path = './Images/Avatar.jpg'
            img = Image.open(img_path)

            width, height = img.size
            asp_rat = width/height

            new_width = 120

            new_height = 124

            new_rat = new_width/new_height

            if (new_rat == asp_rat):
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            else:
                new_height = round(new_width / asp_rat)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save("./Images/outputname.jpg", quality=95)

            back_im = im1.copy()
            mrl = Image.open('./Images/outputname.jpg')
            back_im.paste(mrl, (382, 180))
            back_im.save('./Images/ant2.jpg', quality=95)
            await ctx.send(file=discord.File('./Images/ant2.jpg'))
        elif Animal == 'beetle':
            im1 = Image.open(f'./Images/{Animal}.jpg')

            img_path = './Images/Avatar.jpg'
            img = Image.open(img_path)

            width, height = img.size
            asp_rat = width/height

            new_width = 130

            new_height = 134

            new_rat = new_width/new_height

            if (new_rat == asp_rat):
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            else:
                new_height = round(new_width / asp_rat)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save("./Images/outputname.jpg", quality=95)

            back_im = im1.copy()
            mrl = Image.open('./Images/outputname.jpg')
            back_im.paste(mrl, (365, 160))
            back_im.save('./Images/beetle2.jpg', quality=95)
            await ctx.send(file=discord.File('./Images/beetle2.jpg'))
        elif Animal == 'fly':
            im1 = Image.open(f'./Images/{Animal}.jpg')

            img_path = './Images/Avatar.jpg'
            img = Image.open(img_path)

            width, height = img.size
            asp_rat = width/height

            new_width = 110

            new_height = 114

            new_rat = new_width/new_height

            if (new_rat == asp_rat):
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            else:
                new_height = round(new_width / asp_rat)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save("./Images/outputname.jpg", quality=95)

            back_im = im1.copy()
            mrl = Image.open('./Images/outputname.jpg')
            back_im.paste(mrl, (215, 113))
            back_im.save('./Images/fly2.jpg', quality=95)
            await ctx.send(file=discord.File('./Images/fly2.jpg'))
        elif Animal == 'beetle':
            im1 = Image.open(f'./Images/{Animal}.jpg')

            img_path = './Images/Avatar.jpg'
            img = Image.open(img_path)

            width, height = img.size
            asp_rat = width/height

            new_width = 110

            new_height = 114

            new_rat = new_width/new_height

            if (new_rat == asp_rat):
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            else:
                new_height = round(new_width / asp_rat)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save("./Images/outputname.jpg", quality=95)

            back_im = im1.copy()
            mrl = Image.open('./Images/outputname.jpg')
            back_im.paste(mrl, (365, 160))
            back_im.save('./Images/beetle2.jpg', quality=95)
            await ctx.send(file=discord.File('./Images/beetle2.jpg'))
        elif Animal == 'ladybird':
            im1 = Image.open(f'./Images/{Animal}.jpg')

            img_path = './Images/Avatar.jpg'
            img = Image.open(img_path)

            width, height = img.size
            asp_rat = width/height

            new_width = 250

            new_height = 254

            new_rat = new_width/new_height

            if (new_rat == asp_rat):
                img = img.resize((new_width, new_height), Image.ANTIALIAS)

            else:
                new_height = round(new_width / asp_rat)
                img = img.resize((new_width, new_height), Image.ANTIALIAS)
            img.save("./Images/outputname.jpg", quality=95)

            back_im = im1.copy()
            mrl = Image.open('./Images/outputname.jpg')
            back_im.paste(mrl, (750, 300))
            back_im.save('./Images/ladybird2.jpg', quality=95)
            await ctx.send(file=discord.File('./Images/ladybird2.jpg'))

        else:
            if Animal == None:
                pass
            else:
                await ctx.channel.purge(limit=1)
                await ctx.send('That animal doesnt exist! View animals using `Animals`')
                lists = ['', '', '', '', '', '', 'The animal part is case sensitive!']
                await ctx.send(random.choice(lists))


def setup(bot):
    bot.add_cog(Simulate(bot))
