from os import getenv
from typing import Optional

from discord import Activity, ActivityType
from discord.ext.commands import Bot, Cog, when_mentioned_or
from discord.ext.commands.errors import (
    BadArgument,
    CheckFailure,
    CommandNotFound,
    CommandOnCooldown,
    MissingRequiredArgument,
)
from dotenv import load_dotenv
from psutil import cpu_percent, virtual_memory

from helpers import escape_text, generate_embed, update_owners
from variables import DANGER_COLOR, SUCCESS_COLOR

from dev_module import Development
from eco_module import Economy
from games_module import Games
from image_module import ImageManipulation
from random_module import Random
from status_module import StatusModule

load_dotenv()

bot = Bot(
    command_prefix=when_mentioned_or("&"), case_insensitive=True, description="Trence",
)

bot.remove_command("help")


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

    if getenv("STATUSPAGE_API_KEY"):
        bot.add_cog(StatusModule(bot))

    if getenv("BOT_IN_SERVER_ROLE"):
        await update_owners(bot)

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

    if getenv("BOT_IN_SERVER_ROLE"):
        await update_owners(bot)


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

    if getenv("BOT_IN_SERVER_ROLE"):
        await update_owners(bot)


@bot.event
async def on_member_join(member):
    if not member.guild == bot.get_guild(int(getenv("BOT_GUILD_ID"))):
        return

    if getenv("BOT_IN_SERVER_ROLE"):
        await update_owners(bot)


def command_exists(command: str):
    commands = bot.walk_commands()
    for x in commands:
        if x.name == command or command in x.aliases:
            return True
    return False


def get_command_brief(command: str):
    commands = bot.walk_commands()
    for x in commands:
        if (x.name == command or command in x.aliases) and x.brief:
            return f"`&{x.name}` - {x.brief}"
    return f"`&{command}`"


def get_command_usage(command: str):
    commands = bot.walk_commands()
    for x in commands:
        if (x.name == command or command in x.aliases) and x.usage:
            return f"`{x.usage}`"


def get_command_aliases(command: str):
    commands = bot.walk_commands()
    for x in commands:
        if (x.name == command or command in x.aliases) and x.aliases:
            return ", ".join([f"`{alias}`" for alias in sorted(x.aliases)])


def get_command_embed(command: str):
    if command_exists(command):
        title = get_command_brief(command)
        usage = get_command_usage(command)
        aliases = get_command_aliases(command)

        embed = generate_embed(title=title)

        if usage:
            embed.add_field(name="Usage", value=usage, inline=False)

        if aliases:
            embed.add_field(name="Aliases", value=aliases)
    else:
        embed = generate_embed(title="Command not found", color=DANGER_COLOR)

    return embed


@bot.command(
    name="help",
    brief="Show available commands",
    usage="&help",
    aliases=["?", "commands"],
)
async def help_(ctx, *, command: str = None):
    if command:
        await ctx.send("", embed=get_command_embed(command.lower()))
    else:
        embed = generate_embed(
            title="Trence Help",
            description="For more information on a command, use `&help <command>`",
        )
        embed.add_field(
            name="General",
            value="\n".join(
                [
                    get_command_brief(command)
                    for command in ["help", "info", "invite", "support", "code"]
                ]
            ),
            inline=False,
        )
        embed.add_field(
            name="Economy",
            value="\n".join(
                [
                    get_command_brief(command)
                    for command in ["bal", "top", "work", "beg"]
                ]
            ),
            inline=False,
        )
        embed.add_field(
            name="Games",
            value="\n".join([get_command_brief(command) for command in ["nhie"]]),
            inline=False,
        )
        embed.add_field(
            name="Random",
            value="\n".join(
                [
                    get_command_brief(command)
                    for command in [
                        "circle",
                        "8ball",
                        "clap",
                        "flip",
                        "green",
                        "random",
                    ]
                ]
            ),
            inline=False,
        )

        await ctx.send("", embed=embed)


@bot.command(
    brief="Invite the bot to your own server",
    usage="&invite",
    aliases=["addbot", "usebot", "inv"],
)
async def invite(ctx):
    invite_link = f"https://discord.com/api/oauth2/authorize?client_id={bot.user.id}&permissions=1077267520&scope=bot"

    await ctx.send(
        "", embed=generate_embed(title="Invite the bot to your server", url=invite_link)
    )


@bot.command(
    aliases=["server", "supportserver"],
    brief="Join the support server",
    usage="&support",
)
async def support(ctx):
    await ctx.send(
        "https://discord.gg/ebDzmnv",
        embed=generate_embed(
            title="Join the Trence support server with the link above"
        ),
    )


@bot.command(
    aliases=["source", "inspect", "github", "repo"],
    brief="View the source code",
    usage="&code",
)
async def code(ctx):
    await ctx.send(
        "",
        embed=generate_embed(
            title="View the bot's source code on GitHub",
            url="https://github.com/bsoyka/trence",
        ),
    )


@bot.command(
    aliases=["ping", "latency", "cpu", "memory", "servers", "members", "status"],
    brief="Show current information about the bot",
    usage="&info",
)
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
    embed.add_field(
        name="Status page",
        value="[trence.statuspage.io](https://trence.statuspage.io/)",
        inline=False,
    )

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
