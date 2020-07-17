from random import randint
from sqlite3 import connect

from discord import User
from discord.ext.commands import BucketType, Cog, command, cooldown

from database import get_balance, get_leaderboard, set_balance
from helpers import escape_text, generate_embed
from variables import DANGER_COLOR


class Economy(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.database = connect("economy.db")

    @command()
    @cooldown(1, 7, BucketType.user)
    async def bal(self, ctx, user: User = None):
        """
        Gets a user's balance
        """

        user = user if user else ctx.author

        await ctx.send(
            "",
            embed=generate_embed(
                title="Current balance", description=get_balance(ctx.author.id)
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
    @cooldown(2, 15, BucketType.channel)
    async def leaderboard(self, ctx):
        """
        Gets the server economy leaderboard
        """

        leaderboard = get_leaderboard(ctx.guild.members)

        top_str = "\n".join(
            f"{index}. **{escape_text(self.bot.get_user(user_id))}**: {balance}"
            for index, (user_id, balance) in enumerate(leaderboard, start=1)
        )

        await ctx.send(
            "",
            embed=generate_embed(
                title=f"{escape_text(ctx.guild.name)} leaderboard", description=top_str
            ),
        )
