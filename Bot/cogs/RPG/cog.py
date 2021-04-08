import asyncio

import discord
from discord.ext import commands

from .DB import get_user, main, reset_progress
from .src.shop import shop


class Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.shop = shop

    @commands.command(name = "start")
    async def start(self, ctx):
        """
        Description:
            \\ Start an account for Karen's RPG game.

        -----

        Parameters:
            \\ ctx (Context)

        -----

        Usage:
            \\ start

        -----

        What does the command do:
            \\ Checks if the user already has an account or not.
            \\ Asks for a confirmation from the user if they really want to start an account or not. (reaction based)
            \\ If they accept, then creates a new account.
        """

        data = main.find_one({"_id": ctx.author.id})
        if not data:
            confirmation = await ctx.send(
                embed = discord.Embed(
                    description = f"Are you sure you want to start your career in this RPG game? This game contains explicit content.",
                    color = discord.Colour.red()
                ).set_footer(icon_url = ctx.author.avatar_url, text = "This confirmation times out in 60 seconds.")
            )
            await confirmation.add_reaction("✅")
            await confirmation.add_reaction("❌")

            def check(m):
                return m.message_id == confirmation.id and m.user_id == ctx.author.id and str(m.emoji) == "✅" or str(m.emoji) == "❌"
            try:
                reaction = await self.bot.wait_for("on_raw_reaction_add", timeout = 60, check = check)
            except asyncio.TimeoutError:
                await ctx.send(
                    embed = discord.Embed(
                        description = f"Alright, looks like we aren't setting up an account today!",
                        color = discord.Colour.red()
                    )
                )
            else:
                if str(reaction.emoji) == "✅":
                    await get_user(ctx.author)
                    await ctx.send(
                        embed = discord.Embed(
                            description = "✅ Successfully created an account for you in Karen's RPG system.",
                            color = discord.Colour.green()
                        )
                    )
                elif str(reaction.emoji) == "❌":
                    await ctx.send(
                    embed = discord.Embed(
                        description = f"Alright, cancelling this process!",
                        color = discord.Colour.red()
                    )
                )
        else:
            await ctx.send(
                embed = discord.Embed(
                    description = f"❌ You already have an account registered!",
                    color = discord.Colour.red()
                )
            )

    @commands.command(name = "reset")
    async def reset(self, ctx):
        """
        Description:
            \\ Reset your account.

        -----

        Parameters:
            \\ ctx (Context)

        -----

        Usage:
            \\ reset

        -----

        What does the command do:
            \\ Checks if the user already has an account or not.
            \\ Asks for a confirmation from the user if they really want to reset their account or not. (reaction based)
            \\ Asks for a final confirmation from the user (message based)
            \\ If they agree on resetting, then resets the progress.
        """

        data = main.find_one({"_id": ctx.author.id})
        if data:
            confirmation1 = await ctx.send(
                embed = discord.Embed(
                    description = f"Are you sure you want to reset your career in this RPG game? This will erase all your data in the game!",
                    color = discord.Colour.red()
                ).set_footer(icon_url = ctx.author.avatar_url, text = "This confirmation times out in 60 seconds.")
            )
            await confirmation1.add_reaction("✅")
            await confirmation1.add_reaction("❌")

            def check(m):
                return m.message_id == confirmation1.id and m.user_id == ctx.author.id and str(m.emoji) == "✅" or str(m.emoji) == "❌"
            try:
                reaction = await self.bot.wait_for("on_raw_reaction_add", timeout = 60, check = check)
            except asyncio.TimeoutError:
                await ctx.send(
                    embed = discord.Embed(
                        description = f"Alright, looks like we aren't resetting your account today!",
                        color = discord.Colour.red()
                    )
                )
            else:
                if str(reaction.emoji) == "✅":
                    await get_user(ctx.author)
                    confirmation2 = await ctx.send(
                        embed = discord.Embed(
                            description = f"Are you really sure about resetting your progress? **This procceess can't be undone!** `(y/n)`",
                            color = discord.Colour.red()
                        ).set_footer(icon_url = ctx.author.avatar_url, text = "This confirmation times out in 60 seconds.")
                    )
                    def check_(m):
                        return m.channel == ctx.channel and m.author == ctx.author
                    try:
                        msg = await self.bot.wait_for("on_message", timeout = 60, check = check)
                    except asyncio.TimeoutError:
                        await ctx.send(
                            embed = discord.Embed(
                                description = f"Alright, looks like we aren't resetting your account today!",
                                color = discord.Colour.red()
                            )
                        )
                    else:
                        if msg.content.lower() == "y" or msg.content.lower() == "yes":
                            await reset_progress(ctx.author)
                            await ctx.send(
                                embed = discord.Embed(
                                    description = "✅ Successfully reset your account in Karen's RPG system. Your data in this game has been erased.",
                                    color = discord.Colour.green()
                                )
                            )
                        elif msg.content.lower() == "n" or msg.content.lower() == "no":
                            await ctx.send(
                                embed = discord.Embed(
                                    description = f"Alright, cancelling this process!",
                                    color = discord.Colour.red()
                                )
                            )                            
                elif str(reaction.emoji) == "❌":
                    await ctx.send(
                        embed = discord.Embed(
                            description = f"Alright, cancelling this process!",
                            color = discord.Colour.red()
                        )
                    )
        else:
            await ctx.send(
                embed = discord.Embed(
                    description = f"❌ You don't have an account registered!",
                    color = discord.Colour.red()
                )
            )
