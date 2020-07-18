from os import getenv

from discord import Activity, ActivityType
from discord.ext.commands import Bot, when_mentioned_or
from discord.ext.commands.errors import (BadArgument, CheckFailure,
                                         CommandNotFound, CommandOnCooldown,
                                         MissingRequiredArgument)
from dotenv import load_dotenv
from psutil import cpu_percent, virtual_memory

from helpers import escape_text, generate_embed
from variables import DANGER_COLOR, SUCCESS_COLOR

from dev_module import Development
from eco_module import Economy
from games_module import Games
from image_module import ImageManipulation
from random_module import Random

load_dotenv()

bot = Bot(
    command_prefix=when_mentioned_or("&"), case_insensitive=True, description="Trence",
)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name=f"in {len(bot.guilds)} servers | &help"
        )
    )

    status_channel = await bot.fetch_channel(getenv("BOT_STATUS_CHANNEL"))
    await status_channel.send(
        "", embed=generate_embed(title="Bot is ready", color=SUCCESS_COLOR)
    )

    print("Bot is ready")


@bot.event
async def on_guild_join(guild):
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name=f"in {len(bot.guilds)} servers | &help"
        )
    )

    status_channel = await bot.fetch_channel(getenv("BOT_STATUS_CHANNEL"))
    embed = generate_embed(
        title="Joined server",
        description=f"**{escape_text(guild.name)}**",
        color=SUCCESS_COLOR,
    )
    embed.add_field(name="ID", value=str(guild.id))
    embed.add_field(name="Owner", value=str(guild.owner))
    embed.add_field(name="Members", value=str(len(guild.members)))
    await status_channel.send("", embed=embed)


@bot.event
async def on_guild_remove(guild):
    await bot.change_presence(
        activity=Activity(
            type=ActivityType.playing, name=f"in {len(bot.guilds)} servers | &help"
        )
    )

    status_channel = await bot.fetch_channel(getenv("BOT_STATUS_CHANNEL"))
    embed = generate_embed(
        title="Left or removed from server",
        description=f"**{escape_text(guild.name)}**",
        color=DANGER_COLOR,
    )
    embed.add_field(name="ID", value=str(guild.id))
    embed.add_field(name="Owner", value=str(guild.owner))
    embed.add_field(name="Members", value=str(len(guild.members)))
    await status_channel.send("", embed=embed)


@bot.command()
async def invite(ctx):
    invite_link = f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=1077267520&scope=bot"

    await ctx.send(
        "", embed=generate_embed(title="Invite the bot to your server", url=invite_link)
    )


@bot.command(aliases=["server"])
async def support(ctx):
    await ctx.send(
        "https://discord.gg/CcRr9Su",
        embed=generate_embed(
            title="Join the Trence support server with the link above"
        ),
    )


@bot.command(aliases=["ping"])
async def info(ctx):
    embed = generate_embed(
        title="Information",
        description="Find a list of commands with the `&help` command",
    )
    embed.add_field(name="Latency", value=f"{round(bot.latency * 1000)}ms")
    embed.add_field(name="Server count", value=str(len(bot.guilds)))
    embed.add_field(name="Unique members", value=str(len(set(bot.get_all_members()))))
    embed.add_field(name="CPU usage", value=f"{cpu_percent()}%")
    embed.add_field(name="Memory usage", value=f"{virtual_memory().percent}%")

    await ctx.send("", embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    elif isinstance(error, BadArgument):
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
                title=f"Missing a required argument: {error.param.name}",
                color=DANGER_COLOR,
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
