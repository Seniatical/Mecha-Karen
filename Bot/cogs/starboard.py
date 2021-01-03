import discord
from discord.ext import commands
from Utils import db

'''
Version Release:
    Non - Configurable mode has been set
    Embed + Star changed once it has been reached
    Need to fix the DB storing the stars
    Unreliable
    
Version Release:
    Stars are grabbed straight from the message
        -> More reliable
        -> No need to write and read DB for them
    Fixed broken attachements:
        HTTPException:
            Gives message link and sets a footer
    If messaged edits it edits
        -> Soon to add (Edited) to the footer
        
    Some other bs check the update logs - Mark
    
Version Release:
    Configurable:
        Stars and Channel
        
    Fixed the UNIQUE CONSTRAINT issue
'''

def star(stars):
    if stars in range(0, 6):
        colour = 0xECFFA7
        star_ = '⭐'
    elif stars in range(5, 11):
        colour = 0xE1FF79
        star_ = '🌟'
    elif stars in range(10, 16):
        colour = 0xD4FF3E
        star_ = '💫'    ## Last resort
    else:
        colour = 0xC7FF00
        star_ = '☄️'
    return colour, star_

def create_embed(message: discord.Message, stars: int):
    colour, star_count = star(stars)
    embed = discord.Embed(colour=colour, description='[Original Message]({})'.format(message.jump_url))
    embed.set_author(icon_url=message.author.avatar_url, name=message.author)
    if message.content != None:
        embed.add_field(name='Message:', value=message.content)
    if len(message.attachments):
        if message.attachments[0].filename.split('.')[-1] not in ['png', 'jpg', 'gif', 'jpeg']:
            embed.add_field(name='Attachments:', value=message.attachments[0].url)
        else:
            embed.set_image(url=message.attachments[0].url)
    pre = 'Stars' if stars != 1 else 'Star'
    message_ = '{} **{} {}** {}'.format(star_count, stars, pre, message.channel.mention)
    return embed, message_

class starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        global count
        if payload.emoji.name == '⭐':
            channel = db.record(
                'SELECT star_channel FROM guild WHERE GuildID = ?', payload.guild_id) or (None,)
            if not channel[0]:
                return
            message = await self.bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
            if payload.member.id == message.author.id or message.author.bot or channel[0] == payload.channel_id:
                return await message.remove_reaction(payload.emoji, payload.member)
            star_message = db.record(
                'SELECT StarMessage FROM starboard WHERE RootMessage = ?', message.id) or (None,)
            star_limit = db.record(
                'SELECT star_count FROM guild WHERE GuildID = ?', payload.guild_id) or (0,)
            for reaction in message.reactions:
                if reaction.emoji == '⭐':
                    count = reaction.count
                    break
                else:
                    count = 0
            if count == 0:
                db.execute(
                    'DELETE FROM starboard WHERE RootMessage = ?', message.id)
                return db.commit()
            star_limit = 0 if not star_limit[0] else star_limit[0]
            if count < star_limit:
                return
            star_channel = self.bot.get_channel(channel[0])
            embed, mes = create_embed(message, count)
            if not star_message[0]:
                try:
                    star_mes = await star_channel.send(content=mes, embed=embed)
                except discord.errors.HTTPException:
                    embed = discord.Embed(description='[Original Message]({})'.format(message.jump_url), colour=discord.Colour.red()).set_author(icon_url=message.author.avatar_url, name=message.author)
                    embed.set_footer(text='Missing Field, Cannot Load Original Message!', icon_url=self.bot.user.avatar_url)
                    star_mes = await star_channel.send(embed=embed, content=mes)
                db.execute(
                    'INSERT INTO starboard (RootMessage, StarMessage) VALUES (?, ?)', message.id, star_mes.id)
                db.commit()
            else:
                star_message = await star_channel.fetch_message(star_message[0])
                try:
                    await star_message.edit(content=mes, embed=embed)
                except discord.errors.HTTPException:
                    embed = discord.Embed(description='[Original Message]({})'.format(message.jump_url), colour=discord.Colour.red()).set_author(icon_url=message.author.avatar_url, name=message.author)
                    embed.set_footer(text='Missing Field, Cannot Load Original Message!', icon_url=self.bot.user.avatar_url)
                    await star_message.edit(embed=embed, content=mes)

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def setboard(self, ctx, channel: discord.TextChannel = None):
        if not channel:
            ctx.command.reset_command(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Please mention a channel, If you wish to remove your starboard mention that channel! You can view your configs by using command `-Starboard`',
                colour=discord.Colour.red()
            ))
        channel_ = db.record(
            'SELECT star_channel FROM guild WHERE GuildID = ?', ctx.guild.id) or (None,)
        if channel_[0] == channel.id:
            db.execute(
                'UPDATE guild SET star_channel = ? WHERE GuildID = ?', None, ctx.guild.id)
            db.commit()
            return await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> Removed starboard from this server!',
                colour=discord.Colour.green()
            ))
        db.execute(
            'UPDATE guild SET star_channel = ? WHERE GuildID = ?', channel.id, ctx.guild.id)
        db.commit()
        await ctx.send(embed=discord.Embed(
            description='<a:Passed:757652583392215201> New Starboard has been set for {}'.format(channel.mention),
            colour=discord.Colour.green()
        ))

    @commands.command()
    @commands.has_guild_permissions(manage_guild=True)
    @commands.cooldown(1, 60, commands.BucketType.guild)
    async def setstarlimit(self, ctx, count_='1'):
        try:
            count_ = int(count_)
        except ValueError:
            ctx.command.reset_command(ctx)
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Star limit must be a number not letters!',
                colour=discord.Colour.red()
            ))
        if count_ < 0:
            return await ctx.send(embed=discord.Embed(
                description=''
            ))
        board = db.record(
            'SELECT star_channel FROM guild WHERE GuildID = ?', ctx.guild.id) or (None,)
        if not board[0]:
            return await ctx.send(embed=discord.Embed(
                description='<a:nope:787764352387776523> Please setup a starboard using command `-Setboard` before using this command!',
                colour=discord.Colour.red()
            ))
        else:
            db.execute(
                'UPDATE guild SET star_count = ? WHERE GuildID = ?', count_, ctx.guild.id)
            db.commit()
            await ctx.send(embed=discord.Embed(
                description='<a:Passed:757652583392215201> New Starboard limit is {}.'.format(count_),
                colour=discord.Colour.green()
            ))

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def starboard(self, ctx):
        channel = db.record(
            'SELECT star_channel FROM guild WHERE GuildID = ?', ctx.guild.id) or ('Not Set',)
        star_lim = db.record(
            'SELECT star_count FROM guild WHERE GuildID = ?', ctx.guild.id) or (1,)
        if isinstance(channel[0], int):
            channel_ = self.bot.get_channel(channel[0])
        else:
            channel_ = 'Not Set'
        status = 'Status: Active <:4941_online:787764205256310825>' if channel_ != 'Not Set' else 'Status: Inactive <:offline:787764149706031104>'
        colour = discord.Colour.green() if channel_ != 'Not Set' else discord.Colour.red()
        embed = discord.Embed(
            title=status,
            colour=colour,
            timestamp=ctx.message.created_at).set_footer(text='Prompted by {}'.format(ctx.author), icon_url=ctx.author.avatar_url)
        embed.add_field(name='Channel:', value=channel_.mention if channel_ != 'Not Set' else channel_)
        embed.add_field(name='Star Limit:', value='**{}**'.format('1' if not star_lim[0] else star_lim[0]), inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(starboard(bot))
