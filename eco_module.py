from random import randint
from sqlite3 import connect

from discord import User
from discord.ext.commands import BucketType, Cog, command, cooldown

from database import get_balance, get_global_leaderboard, get_leaderboard, set_balance
from helpers import escape_text, generate_embed
from variables import DANGER_COLOR


class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = connect("economy.db")

    @command()
    @cooldown(3, 7, BucketType.user)
    async def bal(self, ctx, user: User = None):
        """
        Gets a user's balance
        """

        user = user if user else ctx.author

        await ctx.send(
            "",
            embed=generate_embed(
                title=f"Current balance for {user}", description=get_balance(user.id)
            ),
        )

    @command()
    @cooldown(1, 180, BucketType.user)
    async def work(self, ctx):
        """
        Works for a random amount of money
        """

        old_balance = get_balance(ctx.author.id)
        earnings = randint(25, 125)
        new_balance = old_balance + earnings

        set_balance(ctx.author.id, new_balance)

        embed = generate_embed(title=f"You've worked, {escape_text(ctx.author)}!")
        embed.add_field(name="Earned", value=earnings)

        await ctx.send("", embed=embed)

    @command()
    @cooldown(1, 60, BucketType.user)
    async def beg(self, ctx):
        """
        Begs for a random amount of money
        """

        old_balance = get_balance(ctx.author.id)

        if randint(0, 2):
            earnings = randint(5, 35)
            new_balance = old_balance + earnings

            set_balance(ctx.author.id, new_balance)

            embed = generate_embed(title=f"You've begged, {escape_text(ctx.author)}!")
            embed.add_field(name="Earned", value=earnings)
        else:
            embed = generate_embed(
                title=f"You failed, {escape_text(ctx.author)}.", color=DANGER_COLOR
            )

        await ctx.send("", embed=embed)

    @command(aliases=["lb", "top"])
    @cooldown(3, 15, BucketType.channel)
    async def leaderboard(self, ctx, mode: str = "server"):
        """
        Gets the economy leaderboard
        """
        server_options = ["server", "local", "s", "l"]
        global_options = ["global", "g"]
        all_options = server_options + global_options

        if mode.lower() not in all_options:
            await ctx.send(
                "",
                embed=generate_embed(
                    title="Invalid mode specified",
                    description='Must be "server" (default) or "global"',
                    color=DANGER_COLOR,
                ),
            )
        elif mode.lower() in server_options:
            leaderboard = get_leaderboard(ctx.guild.members)

            top_str = "\n".join(
                f"{index}. **{escape_text(self.bot.get_user(user_id))}**: {balance}"
                for index, (user_id, balance) in enumerate(leaderboard, start=1)
            )

            await ctx.send(
                "",
                embed=generate_embed(
                    title=f"{escape_text(ctx.guild.name)} leaderboard",
                    description=top_str,
                ),
            )
        elif mode.lower() in global_options:
            leaderboard = get_global_leaderboard()

            top_str = "\n".join(
                f"{index}. **{escape_text(self.bot.get_user(user_id))}**: {balance}"
                for index, (user_id, balance) in enumerate(leaderboard, start=1)
            )

            await ctx.send(
                "",
                embed=generate_embed(
                    title="Global leaderboard",
                    description=top_str.replace("**None**:", "***Unknown user***:"),
                ),
            )
