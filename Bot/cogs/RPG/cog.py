import asyncio

import discord
from discord.ext import commands

from .DB import main, get_user
from .src.shop import shop


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop = shop

    @commands.command(name = "start")
    async def start(self, ctx):
        """
        Start an account for Karen's RPG game.

        -----

        Parameters:
            \\ ctx (Context)

        Usage:
            \\ start

        What does the command do:
            \\ Asks for a confirmation from the user if they really want to start an account or not.
            \\ Checks if the user already has an account or not.
            \\ If they don't then creates a new one.
        """
        confirmation1 = await ctx.send(
            embed = discord.Embed(
                description = f"Are you sure you want to start your career in this RPG game? This game contains explicit content.",
                color = discord.Colour.red()
            ).set_footer(icon_url = ctx.author.avatar_url, text = "This confirmation times out in 60 seconds.")
        )
        await confirmation1.add_reaction("✅")
        await confirmation1.add_reaction("❌")

        def check(m):
            return m.message_id == confirmation1.id and m.user_id == ctx.author.id and str(m.emoji) == "✅" or str(m.emoji) == "❌"
        try:
            __ = await self.bot.wait_for("on_raw_reaction_add", timeout = 60, check = check)
        except asyncio.TimeoutError:
            await ctx.send(
                embed = discord.Embed(
                    description = f"Alright, looks like we aren't setting up an account today!",
                    color = discord.Colour.red()
                )
            )
        else:
            if str(__.emoji) == "✅":
                data = main.find_one({"_id": ctx.author.id})
                if not data:
                    await get_user(ctx.author)
                    await ctx.send(
                        embed = discord.Embed(
                            description = "✅ Successfully created an account for you in Karen's RPG system.",
                            color = discord.Colour.green()
                        )
                    )
                else:
                    await ctx.send(
                        embed = discord.Embed(
                            description = f"❌ You already have an account registered!",
                            color = discord.Colour.red()
                        )
                    )
            elif str(__.emoji) == "❌":
                await ctx.send(
                embed = discord.Embed(
                    description = f"Alright, cancelling this process!",
                    color = discord.Colour.red()
                )
            )
