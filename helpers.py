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
        embed.set_footer(text=f"{footer} - Bot by bsoyka")
    else:
        embed.set_footer(text="Bot by bsoyka")

    if image != None:
        embed.set_image(url=image)

    if thumbnail != None:
        embed.set_thumbnail(url=image)

    return embed


def is_developer(ctx):
    return ctx.author.id in [466677474672246795]


def escape_text(text):
    return str(text).replace("_", "\\_")
