from random import choice, getrandbits, randint

from discord.ext.commands import BucketType, Cog, command, cooldown

from helpers import generate_embed
from variables import MAGIC_8_ANSWERS


class Random(Cog, name="Random entertainment"):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["coin", "coinflip"])
    @cooldown(5, 10)
    async def flip(self, ctx):
        """
        Flips a coin
        """

        if getrandbits(1):
            await ctx.send(
                "", embed=generate_embed(title="Coin flip", description="Heads")
            )
        else:
            await ctx.send(
                "", embed=generate_embed(title="Coin flip", description="Tails")
            )

    @command(aliases=["rand"])
    @cooldown(5, 10)
    async def random(self, ctx, start: int, end: int):
        """
        Picks a random number
        """

        await ctx.send(
            "",
            embed=generate_embed(
                title="Random number", description=randint(start, end)
            ),
        )

    @command(aliases=["sass"])
    @cooldown(5, 10)
    async def clap(self, ctx, *, text: str):
        """
        Says whatever you want with sass
        """

        await ctx.send("", embed=generate_embed(title=text.replace(" ", " :clap: ")))

    @command(name="8ball", aliases=["magic8"])
    @cooldown(5, 10)
    async def magic8ball(self, ctx, *, question: str):
        """
        Responds with a magic 8 ball response
        """

        await ctx.send(
            "",
            embed=generate_embed(
                title="Magic 8 Ball says...", description=choice(MAGIC_8_ANSWERS)
            ),
        )

    @command(aliases=["green"])
    @cooldown(5, 10)
    async def greentext(self, ctx, *, text: str):
        """
        Says whatever you want, but green
        """

        await ctx.send(f"```css\n{text}\n```")
