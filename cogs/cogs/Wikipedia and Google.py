import discord
from discord.ext import commands
import wikipedia, os
from chatbot import Chat, register_call
from bs4 import *

template_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"chatbotTemplate","chatbottemplate.template")
chat = Chat(template_file_path)

class Searches(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @register_call("whoIs")
    def who_is(query, session_id="general"):
        try:
            return wikipedia.summary(query)
        except Exception:
            for new_query in wikipedia.search(query):
                try:
                    return wikipedia.summary(new_query)
                except Exception:
                    pass
        return "I don't know about "+query

    @commands.command(pass_context = True)
    @commands.cooldown(1, 300, commands.BucketType.member)
    async def search(self, ctx,*,message):
        result = chat.respond(message)
        if(len(result)<=2048):
            embed=discord.Embed(title=f"Search results for {message}", description = result, color = (0xF48D1))
            await ctx.send(embed=embed)
        else:
            embedList = []
            n=2048
            embedList = [result[i:i+n] for i in range(0, len(result), n)]
            for num, item in enumerate(embedList, start = 1):
                if(num == 1):
                    embed = discord.Embed(title=f"Search results for {message}", description = item, color = (0xF48D1))
                    embed.set_footer(text="Page {}".format(num))
                    await ctx.send(embed = embed)
                else:
                    embed = discord.Embed(description = item, color = (0xF48D1))
                    embed.set_footer(text = "Page {}".format(num))
                    await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Searches(bot))
