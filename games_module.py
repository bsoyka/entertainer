import discord
from discord.ext.commands import Cog, command, cooldown

class Games(Cog):
    def __init__(self, bot):
        self.bot = bot
