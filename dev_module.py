import pathlib
from os import getenv, system
from sys import executable

from discord import Message, TextChannel, User
from discord.ext.commands import Cog, check, group

from database import get_balance, set_balance
from helpers import generate_embed, is_developer
from variables import DANGER_COLOR, SUCCESS_COLOR


class Development(Cog, name="Development"):
    def __init__(self, bot):
        self.bot = bot

    @group(hidden=True)
    @check(is_developer)
    async def dev(self, ctx):
        """
        Development commands
        """

        if ctx.invoked_subcommand is None:
            await ctx.send(
                "",
                embed=generate_embed(
                    title="Development",
                    description="You are authorised to use this command, but input an invalid subcommand.",
                ),
            )

    @dev.group(name="restart")
    async def dev_restart(self, ctx):
        """
        Restarts the bot
        """

        await ctx.send("", embed=generate_embed(title="Restarting bot"))

        status_channel = await self.bot.fetch_channel(getenv("BOT_STATUS_CHANNEL"))
        embed = generate_embed(title="Restarting bot")
        embed.add_field(name="Triggered by", value=str(ctx.author), inline=False)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        embed.add_field(name="Message", value=f"[Click here]({ctx.message.jump_url})")
        await status_channel.send("", embed=embed)

        await self.bot.close()
        system(f"{executable} {pathlib.Path(__file__).parent.absolute()}/main.py")

    @dev.group(name="stop")
    async def dev_stop(self, ctx):
        """
        Stops the bot
        """

        await ctx.send(
            "", embed=generate_embed(title="Shutting down bot", color=DANGER_COLOR)
        )

        status_channel = await self.bot.fetch_channel(getenv("BOT_STATUS_CHANNEL"))
        embed = generate_embed(title="Shutting down bot", color=DANGER_COLOR)
        embed.add_field(name="Triggered by", value=str(ctx.author), inline=False)
        embed.add_field(name="Channel", value=ctx.channel.mention)
        embed.add_field(name="Message", value=f"[Click here]({ctx.message.jump_url})")
        await status_channel.send("", embed=embed)

        await self.bot.close()

    @dev.group(name="say")
    async def dev_say(self, ctx, channel: TextChannel, *, text: str):
        """
        Says whatever you want as the bot
        """

        try:
            await ctx.message.delete()
        except:
            pass
        finally:
            await channel.send(text)

    @dev.group(name="setbal")
    async def dev_setbal(self, ctx, user: User, new_balance: int):
        old_balance = get_balance(user.id)

        set_balance(user.id, new_balance)

        embed = generate_embed(title=f"Updated balance for {user}")
        embed.add_field(name="Old balance", value=old_balance)
        embed.add_field(name="New balance", value=new_balance)

        await ctx.send("", embed=embed)

    @dev.group(name="addbal")
    async def dev_addbal(self, ctx, user: User, change: int):
        old_balance = get_balance(user.id)
        new_balance = old_balance + change

        set_balance(user.id, new_balance)

        embed = generate_embed(title=f"Updated balance for {user}")
        embed.add_field(name="Old balance", value=old_balance)
        embed.add_field(name="New balance", value=new_balance)

        await ctx.send("", embed=embed)

    @dev.group(name="invite")
    async def dev_invite(self, ctx, channel: TextChannel):
        invite = await channel.create_invite()

        await ctx.send(
            "",
            embed=generate_embed(title="Invite URL generated", description=str(invite)),
        )

    @dev.group(name="roleinfo")
    async def dev_roleinfo(self, ctx, channel: TextChannel, message: int):
        message = await channel.fetch_message(message)
        guild = message.guild

        embed = generate_embed(title="Server role information")
        embed.add_field(
            name=guild.get_role(733520526500429944),
            inline=False,
            value="Completely trusted users with full administrator permissions",
        )
        embed.add_field(
            name=guild.get_role(733451355397685349),
            value="Developers who've contributed a ton, with permissions to use development commands on the bot",
        )
        embed.add_field(
            name=guild.get_role(733532438612934686),
            value="Those who've contributed to the development of the bot (coding)",
        )
        embed.add_field(
            name=guild.get_role(733531221962784820),
            inline=False,
            value="Server boosters here on Discord! (Includes 25% boost with <@437808476106784770> leveling, attach files, video, and priority speaker permissions)",
        )
        embed.add_field(
            name=guild.get_role(733543787099586660),
            value="Partners of this server or <@733335759175811073> (<#733539039516295268>, Includes attach files and video permissions)",
        )
        embed.add_field(
            name=guild.get_role(733703623988740129),
            value="Those who've invited 5 others to this server (Includes attach files and video permissions)",
        )
        embed.add_field(
            name=guild.get_role(733745042111594607),
            inline=False,
            value="The user with the highest rank on <@437808476106784770> (Includes attach files, video, and priority speaker permissions)",
        )
        embed.add_field(
            name=guild.get_role(733745165298302976),
            inline=False,
            value="Those who've reached level 10 on <@437808476106784770> (Includes attach files and video permissions)",
        )
        embed.add_field(
            name=guild.get_role(733735394448769044),
            value="Ping role for news about the bot, including downtime, new features, and more (React with :robot: to get this)",
        )
        embed.add_field(
            name=guild.get_role(733767816494317679),
            value="Ping role for news about this server (React with :mega: to get this)",
        )
        embed.add_field(
            name=guild.get_role(733786000530210857),
            value="Access to channels with various GitHub webhooks (React with :computer: to get this)",
        )

        await message.edit(embed=embed)

        await ctx.send(
            "", embed=generate_embed(title="Updated message with new role info")
        )
