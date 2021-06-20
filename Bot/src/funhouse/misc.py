import discord
from discord.ext import commands
import pyfiglet
import requests
import shutil
import bs4
import random
from PIL import Image
import disputils
import aiohttp
import hashlib
from requests.utils import requote_uri
from utility import checks

async def most_frequent(list_):
    return max(set(list_), key=list_.count)

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.holder = {}

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        try:
            attach = await message.attachments[0].to_file()
        except IndexError:
            attach = None
        content = message.content
        time = message.created_at
        user = message.author
        self.holder[message.channel.id] = [content, attach, time, user]

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    async def snipe(self, ctx):
        if not ctx.channel.id in self.holder:
            return await ctx.send('Nothing to snipe.')
        data = self.holder[ctx.channel.id]
        embed=discord.Embed(colour=data[-1].colour, timestamp=data[2])
        embed.set_author(name=data[-1].display_name, icon_url=data[-1].avatar)
        if data[0]:
            embed.description = data[0]
        if data[1]:
            await ctx.send(file=data[1])
        embed.set_footer(text='Sniped ')
        del self.holder[ctx.channel.id]
        await ctx.send(embed=embed)

    @commands.command()
    @commands.bot_has_guild_permissions(send_messages=True, embed_links=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ascii(self, ctx, *, text: str = None):
        if text == None:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('Provide me with some text.')
        asc = pyfiglet.figlet_format(text=text)
        try:
            await ctx.send('Ascii Text ->\n```\n' + asc + '\n```')
        except discord.errors.HTTPException:
            ctx.command.reset_cooldown(ctx)
            return await ctx.send('The text was too large!')

    @commands.command(aliases=['W'])
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def weather(self, ctx, *, location: str = None):
        if location == None:
            ctx.command.reset_cooldown(ctx)
            await ctx.send('You haven\'t provided a location!')
        else:
            try:
                x = location
                x = x.lower()
                r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID=49466a8c290796e687e2490621bac0b3'.format(x))
                x = r.json()
                country = x['sys']['country']
                city = x['name']
                cord1 = x['coord']['lon']
                cord2 = x['coord']['lat']
                main = x['weather'][0]['main']
                desc = x['weather'][0]['description']
                speed = x['wind']['speed']
                humid = x['main']['humidity']
                pressure = x['main']['pressure']
                clouds = x['clouds']['all']
                temp = x['main']['temp']
                temp_f = x['main']['feels_like']
                zone = x['timezone']
                embed = discord.Embed(
                    title=f'{city} ({country})',
                    colour=discord.Color.blue(),
                    description=f'Longitude : {cord1} | Latitude : {cord2}'
                )
                embed.add_field(name='Wind', value=f'{speed} MPH')
                embed.add_field(name='Humidity', value=f'{humid}%')
                embed.add_field(name='Weather', value=f'{main} ({desc})')
                embed.add_field(name='Pressure', value=f'{pressure}')
                embed.add_field(name='Clouds', value=f'{clouds}')
                embed.add_field(name='Temperature', value=f'{round(temp - 273.15)} °C')
                embed.add_field(name='Feels Like', value=f'{round(temp_f - 273.15)} °C')
                embed.add_field(name=f'Time Zone', value=f'{zone}')
                embed.add_field(name=f'Min Temp', value=str(round(x['main']['temp_min'] - 273.15)) + ' °C')
                embed.add_field(name=f'Max Temp', value=str(round(x['main']['temp_max'] - 273.15)) + ' °C')
                await ctx.send(embed=embed)
            except KeyError:
                ctx.command.reset_cooldown(ctx)
                await ctx.send('Location was invalid.')

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def github(self, ctx):
        channel = self.bot.get_channel(753311458171027547)
        async for message in channel.history(limit=1):
            last_message = message
        embed = last_message.embeds[0]
        embed.timestamp = last_message.created_at
        embed.set_footer(icon_url=self.bot.user.avatar)
        await ctx.send(embed=embed)

    @commands.command(help = "Check to see if your password has been pwned before.")
    async def pwned(self, ctx, *, password: str) -> discord.Embed:
        password = hashlib.sha1(password.encode('utf-8')).hexdigest()
        search = password.upper()[:5]  # Search up first 5 hashes
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://api.pwnedpasswords.com/range/{search}") as response:
                passwords = await response.text()
                for item in passwords.splitlines():
                    if password.upper()[5:] == item[0:35]:  # If password has been pwned before
                        embed = discord.Embed(title="Password Results: ", color=discord.Colour.red())
                        embed.add_field(name="Better change your password: ", value=f"Your password has been pwned: {item[36:]} times")
                        return await ctx.send(embed=embed)
                #  If it has not been pwned before
                embed = discord.Embed(title="Password Results: ", color=discord.Colour.green())
                embed.add_field(name="Congratulations: ", value="Your password has never been pwned before!")
                return await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def element(self, ctx, *, element_name: str):
        msg = await ctx.send('Fetching your element from the database...')
        compound = element_name.lower()
        IMAGE = requote_uri(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound}/PNG')
        URL = requote_uri(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound}/json')
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as r:
                data = await r.json()
        try:
            data['Fault']
            return await msg.edit(content=None, embed=discord.Embed(
                description='<a:nope:787764352387776523> Compound named **{}** Cannot be found!'.format(element_name),
                colour=discord.Colour.red()
                ))
        except KeyError:
            embed = discord.Embed(colour=random.randint(0x000000, 0xFFFFFF)).set_thumbnail(url=IMAGE)
        names = []
        identifers = []
        weight = []
        counts = []
        for item in data["PC_Compounds"]:
            for urn in item['props']:
                if urn['urn']['label'] == 'Molecular Formula':
                    embed.set_author(icon_url=IMAGE, name=urn['value']['sval'])

                if urn['urn']['label'] == 'IUPAC Name':
                    names.append(urn['value']['sval'])

                if urn['urn']['label'] == 'SMILES':
                    identifers.append(f'''{urn['urn']['name']}: {urn['value']['sval']}''')
                if urn['urn']['label'] == 'Weight':
                    weight.append(f'''{urn['urn']['name']} ({urn['urn']['release'].replace('.', '/')}): {urn['value'].get('fval') or '?'}''')

            for key in item['count']:
                counts.append(f'''{key}: {item['count'][key]}''')

        identifers.append('CID: {}'.format(data["PC_Compounds"][0]['id']['id']['cid']))

        embed.add_field(name='Favourite IUPAC Name:', value=(await most_frequent(names),)[0].title(), inline=False)
        embed.add_field(name='Identifers:', value='```yaml\n{}\n```'.format('\n'.join(identifers)))
        embed.add_field(name='Weights:', value='```yaml\n{}\n```'.format('\n'.join(weight)), inline=False)
        embed.add_field(name='Counts:', value='```yaml\n{}\n```'.format('\n'.join(counts)), inline=False)

        await msg.edit(embed=embed, content=None)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def element_search(self, ctx, *, element: str):
        msg = await ctx.send('Fetching your element from the database...')
        compound = element.lower()
        IMAGE = f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{compound}/PNG'
        URL = f'https://pubchem.ncbi.nlm.nih.gov/rest/autocomplete/compound/{element.lower()}/json?limit=25'
        async with aiohttp.ClientSession() as session:
            async with session.get(URL) as r:
                data = await r.json()
        try:
            data['Fault']
            return await msg.edit(content=None, embed=discord.Embed(
                description='<a:nope:787764352387776523> Compound named **{}** Cannot be found!'.format(element_name),
                colour=discord.Colour.red()
                ))
        except KeyError:
            embed = discord.Embed(colour=random.randint(0x000000, 0xFFFFFF)).set_thumbnail(url=IMAGE)
        items = data['dictionary_terms']['compound']
        embed.description='```yaml\n{}\n```'.format('\n'.join(items))
        await msg.edit(cotent=None, embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def structure(self, ctx, *, element: str):
        async with aiohttp.ClientSession() as session:
            async with session.get(requote_uri(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{element.lower()}/PNG')) as r:
                if r.content_type == 'text/plain':
                    return await ctx.send('Element cannot be found!')
        embed = discord.Embed(title=element.title(), colour=random.randint(0x000000, 0xFFFFFF))
        embed.set_image(url=requote_uri(f'https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/name/{element.lower()}/PNG'))
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))
