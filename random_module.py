from random import choice, getrandbits, randint

from discord.ext.commands import BucketType, Cog, command, cooldown

from helpers import generate_embed
from variables import MAGIC_8_ANSWERS


class Random(Cog, name="Random entertainment"):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["coin", "coinflip"], brief="Flip a coin", usage="&flip")
    @cooldown(5, 10, BucketType.user)
    async def flip(self, ctx):
        if getrandbits(1):
            await ctx.send(
                "", embed=generate_embed(title="Coin flip", description="Heads")
            )
        else:
            await ctx.send(
                "", embed=generate_embed(title="Coin flip", description="Tails")
            )

    @command(aliases=["rand", "randint"], brief="Pick a random number", usage="&random <start> <end>")
    @cooldown(5, 10, BucketType.user)
    async def random(self, ctx, start: int, end: int):
        await ctx.send(
            "",
            embed=generate_embed(
                title="Random number", description=randint(start, end)
            ),
        )

    @command(aliases=["sass"], brief="Say something with sass", usage="&clap <text>")
    @cooldown(5, 10, BucketType.user)
    async def clap(self, ctx, *, text: str):
        await ctx.send(
            "",
            embed=generate_embed(
                title="Text with sass:",
                description=text.replace("  ", " ").replace(" ", " :clap: "),
                footer=f"Requested by {ctx.author}",
            ),
        )

    @command(name="8ball", aliases=["magic8", "m8"], brief="Ask the magic 8 ball a question", usage="&8ball <question>")
    @cooldown(5, 10, BucketType.user)
    async def magic8ball(self, ctx, *, question: str):
        await ctx.send(
            "",
            embed=generate_embed(
                title="Magic 8 Ball says...", description=choice(MAGIC_8_ANSWERS)
            ),
        )

    @command(aliases=["greentext"], brief="Say something but in green", usage="&green <text>")
    @cooldown(5, 10, BucketType.user)
    async def green(self, ctx, *, text: str):
        await ctx.send(
            "",
            embed=generate_embed(
                title="Green text:",
                description=f"```css\n{text}\n```",
                footer=f"Requested by {ctx.author}",
            ),
        )
