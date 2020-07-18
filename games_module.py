import discord
from discord.utils import get
from discord.ext.commands import Cog, command, cooldown, BucketType
from random import choice

from settings import get_env
from helpers import generate_embed

class Games(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(aliases=["neverhaveIever"])
    @cooldown(1, 2.5, BucketType.user)
    async def nhie(self, ctx, *, question="random"):
        """
        Never Have I Ever
        """
        custom_question = True if question != "random" else False
        if not custom_question:
            with open("never_have_I_ever.txt", "r", encoding="utf-8") as file:
                question = choice(file.readlines()).replace("Never have I ever ", "")

        reactions = self.bot.get_guild(int(get_env("BOT_GUILD_ID"))).emojis
        i_have_reaction = get(reactions, id=int(get_env("I_HAVE_REACTION_ID")))
        i_have_not_reaction = get(reactions, id=int(get_env("I_HAVE_NOT_REACTION_ID")))

        message = await ctx.send(
            "",
            embed=generate_embed(
                title="Never have I ever... {}".format(" (Custom Question)" if custom_question else ""), description=question,
                footer=f"Requested by {ctx.author}"
            ),
        )

        await message.add_reaction(i_have_reaction)
        await message.add_reaction(i_have_not_reaction)
