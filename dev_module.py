import pathlib
from os import system
from sys import executable

from discord import TextChannel, User
from discord.ext.commands import Cog, check, group

from database import get_balance, set_balance
from helpers import generate_embed, is_developer


class Development(Cog, name="Development"):
    def __init__(self, bot):
        self.bot = bot

    @group(hidden=True)
    @check(is_developer)
    async def dev(self, ctx):
        """
        Development commands
        """

        if ctx.invoked_subcommand is None:
            await ctx.send(
                "",
                embed=generate_embed(
                    title="Development",
                    description="You are authorised to use this command, but input an invalid subcommand.",
                ),
            )

    @dev.group(name="restart")
    async def dev_restart(self, ctx):
        """
        Restarts the bot
        """

        await ctx.send("", embed=generate_embed(title="Restarting bot"))
        await self.bot.close()
        system(f"{executable} {pathlib.Path(__file__).parent.absolute()}/main.py")

    @dev.group(name="stop")
    async def dev_stop(self, ctx):
        """
        Stops the bot
        """

        await ctx.send("", embed=generate_embed(title="Shutting down bot"))
        await self.bot.close()

    @dev.group(name="say")
    async def dev_say(self, ctx, channel: TextChannel, *, text: str):
        """
        Says whatever you want as the bot
        """

        await ctx.message.delete()
        await channel.send(text)

    @dev.group(name="setbal")
    async def dev_setbal(self, ctx, user: User, new_balance: int):
        old_balance = get_balance(user.id)

        set_balance(user.id, new_balance)

        embed = generate_embed(title=f"Updated balance for {user}")
        embed.add_field(name="Old balance", value=old_balance)
        embed.add_field(name="New balance", value=new_balance)

        await ctx.send("", embed=embed)

    @dev.group(name="addbal")
    async def dev_addbal(self, ctx, user: User, change: int):
        old_balance = get_balance(user.id)
        new_balance = old_balance + change

        set_balance(user.id, new_balance)

        embed = generate_embed(title=f"Updated balance for {user}")
        embed.add_field(name="Old balance", value=old_balance)
        embed.add_field(name="New balance", value=new_balance)

        await ctx.send("", embed=embed)
