from os import getenv

from discord import Activity, ActivityType
from discord.ext.commands import Bot
from discord.ext.commands.errors import (BadArgument, CheckFailure,
                                         CommandNotFound, CommandOnCooldown,
                                         MissingRequiredArgument)
from dotenv import load_dotenv

from dev_module import Development
from eco_module import Economy
from helpers import generate_embed
from image_module import ImageManipulation
from random_module import Random
from games_module import Games
from variables import DANGER_COLOR

load_dotenv()

bot = Bot(command_prefix="&", case_insensitive=True, description="Trence",)


@bot.event
async def on_ready():
    print("Ready")
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name=f"in {len(bot.guilds)} servers"
        )
    )


@bot.event
async def on_guild_join(guild):
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name=f"in {len(bot.guilds)} servers"
        )
    )


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name=f"in {len(bot.guilds)} servers"
        )
    )


@bot.command()
async def invite(ctx):
    invite_link = f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=1077267520&scope=bot"

    await ctx.send(
        "", embed=generate_embed(title="Invite the bot to your server", url=invite_link)
    )


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, BadArgument):
        await ctx.send(
            "",
            embed=generate_embed(
                title="Bad argument given", description=str(error), color=DANGER_COLOR
            ),
        )

        return
    elif isinstance(error, CheckFailure):
        await ctx.send(
            "",
            embed=generate_embed(
                title="Check failure",
                description="You alren't allowed to use that command here",
                color=DANGER_COLOR,
            ),
        )

        return
    elif isinstance(error, CommandNotFound):
        return
    elif isinstance(error, CommandOnCooldown):
        await ctx.send(
            "",
            embed=generate_embed(
                title="This command is on cooldown",
                description=f"Try again in {error.retry_after:.1f} seconds",
                color=DANGER_COLOR,
            ),
        )

        return
    elif isinstance(error, MissingRequiredArgument):
        await ctx.send(
            "",
            embed=generate_embed(
                title=f"Missing a required argument: {error.param.name}", color=DANGER_COLOR,
            ),
        )

        return

    raise error


bot.add_cog(Development(bot))
bot.add_cog(ImageManipulation(bot))
bot.add_cog(Random(bot))
bot.add_cog(Economy(bot))
bot.add_cog(Games(bot))

bot.run(getenv("BOT_TOKEN"))
