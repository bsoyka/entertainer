from os import getenv
from time import time

from discord.ext.commands import Cog
from discord.ext.tasks import loop
from requests import post


class StatusModule(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sender.start()

    def cog_unload(self):
        self.sender.cancel()

    @loop(minutes=2.5)
    async def sender(self):
        post(
            url="https://api.statuspage.io/v1/pages/vbwjhz2x7vtk/metrics/6yqxfpwq0209/data",
            params={"data[timestamp]": int(time()), "data[value]": self.bot.latency * 1000},
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "OAuth " + getenv("STATUSPAGE_API_KEY"),
            },
        )
