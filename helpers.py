from json import load
from os import getenv
from pathlib import Path

from discord import Color, Embed

from variables import PRIMARY_COLOR


def generate_embed(
    title: str,
    description: str = None,
    color: Color = PRIMARY_COLOR,
    footer: str = None,
    image: str = None,
    thumbnail: str = None,
    url: str = None,
):
    embed = Embed(title=title, description=description, color=color, url=url)

    if footer != None:
        embed.set_footer(text=f"{footer} - Bot by bsoyka and others")
    else:
        embed.set_footer(text="Bot by bsoyka and others")

    if image != None:
        embed.set_image(url=image)

    if thumbnail != None:
        embed.set_thumbnail(url=image)

    return embed


def is_developer(ctx):
    return ctx.author.id in [466677474672246795]


def escape_text(text):
    return str(text).replace("_", "\\_").replace("*", "\\*")


async def update_owners(bot):
    server = bot.get_guild(int(getenv("BOT_GUILD_ID")))
    role = server.get_role(int(getenv("BOT_IN_SERVER_ROLE")))
    role_members = set([member.id for member in role.members])
    with open(Path(__file__).parent / "owner_overrides.json") as file:
        overrides = load(file)

    owner_list = set(
        [
            guild.owner.id
            for guild in bot.guilds
            if guild.owner in server.members
            if len([x for x in guild.members if not x.bot]) >= 3
        ]
    )

    for guild_id, owners in overrides.items():
        guild = bot.get_guild(int(guild_id))
        if len([x for x in guild.members if not x.bot]) >= 3:
            owner_list.update(owners)

    for owner in owner_list - role_members:
        await server.get_member(owner).add_roles(role)

    for member in role_members - owner_list:
        await server.get_member(member).remove_roles(role)
