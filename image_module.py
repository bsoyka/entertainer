from functools import partial
from io import BytesIO
from os import getenv
from typing import Union

import requests
from discord import Color, File, Member, User
from discord.ext.commands import Cog, command, cooldown
from PIL import Image, ImageDraw

from helpers import generate_embed


class ImageManipulation(Cog, name="Image manipulation"):
    def __init__(self, bot):
        self.bot = bot

    async def get_avatar(self, user: Union[User, Member]) -> bytes:
        url = user.avatar_url_as(format="png")
        return await url.read()

    @staticmethod
    def processing(avatar_bytes: bytes, colour: tuple) -> BytesIO:
        with Image.open(BytesIO(avatar_bytes)) as im:
            with Image.new("RGB", im.size, colour) as background:
                rgb_avatar = im.convert("RGB")

                with Image.new("L", im.size, 0) as mask:
                    mask_draw = ImageDraw.Draw(mask)

                    mask_draw.ellipse([(0, 0), im.size], fill=255)

                    background.paste(rgb_avatar, (0, 0), mask=mask)

                final_buffer = BytesIO()

                background.save(final_buffer, "png")

        final_buffer.seek(0)

        return final_buffer

    @command()
    @cooldown(3, 15)
    async def circle(self, ctx, *, member: Member = None):
        """
        Displays the user's avatar on their color
        """

        member = member or ctx.author

        async with ctx.typing():
            if isinstance(member, Member):
                member_colour = member.colour.to_rgb()
            else:
                member_colour = (0, 0, 0)

            avatar_bytes = await self.get_avatar(member)

            fn = partial(self.processing, avatar_bytes, member_colour)

            final_buffer = await self.bot.loop.run_in_executor(None, fn)

            response = requests.post(
                "https://api.imgur.com/3/upload",
                files={"image": final_buffer},
                headers={"Authorization": f"Client-ID {getenv('IMGUR_CLIENT_ID')}"},
            )
            response.raise_for_status()
            file_url = response.json()["data"]["link"]

            await ctx.send(
                "",
                embed=generate_embed(
                    title=f"{member}'s circle avatar",
                    image=file_url,
                    color=Color.from_rgb(*member_colour),
                ),
            )
