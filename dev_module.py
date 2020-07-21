import pathlib
from json import dump, load
from os import getenv, system
from sys import executable

from discord import Message, TextChannel, User
from discord.errors import Forbidden
from discord.ext.commands import Cog, Greedy, check, group

from database import get_balance, set_balance
from helpers import generate_embed, is_developer, update_owners
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
            name=guild.get_role(734948102204817571),
            inline=False,
            value="Users who manage a server with at least 3 human members and <@733335759175811073> (Message <@575252669443211264> if you've added the bot to a server you don't own)",
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
        embed.add_field(
            name=guild.get_role(734192906512105483),
            value="Ping role for giveaways (React with :gift: to get this)",
        )
        embed.add_field(
            name=guild.get_role(735011074725773334),
            value="Ping role for polls (React with :thumbsup: to get this)",
        )
        embed.add_field(
            name=guild.get_role(735161809375330417),
            value="Ping role for when <#733521503001509959> is just too quiet (React with :speech_balloon: to get this)",
        )

        await message.edit(embed=embed)

        await ctx.send(
            "", embed=generate_embed(title="Updated message with new role info")
        )

    @dev.group(name="owner")
    async def dev_owner(self, ctx, user: User):
        guild_list = [
            f"{guild.name} ({len([x for x in guild.members if not x.bot])})"
            for guild in self.bot.guilds
            if guild.owner == user
        ]

        await ctx.send(
            "",
            embed=generate_embed(
                title=f"Guilds I'm in owned by {user}",
                description="\n".join(guild_list),
            ),
        )

    @dev.group(name="eval")
    async def dev_eval(self, ctx, *, expression: str):
        result = str(eval(expression)).replace(getenv("BOT_TOKEN"), "DISCORD BOT KEY")
        await ctx.send(
            "",
            embed=generate_embed(
                title="Eval Result", description=f"```\n{result}\n```"
            ),
        )

    @dev.group(name="dm")
    async def dev_dm(self, ctx, user: User, *, message: str):
        await user.send(
            "", embed=generate_embed(title="New message", description=message)
        )

        await ctx.send("", embed=generate_embed(title="Message sent"))

    @dev.group(name="dq")
    async def dev_dq(
        self,
        ctx,
        users: Greedy[User],
        giveaway_channel: TextChannel,
        giveaway_message: int,
    ):
        for user in users:
            giveaway_msg = await giveaway_channel.fetch_message(giveaway_message)
            status = await ctx.send(
                "", embed=generate_embed(title=f"Disqualifying user {user}")
            )

            await giveaway_msg.remove_reaction("🎉", user)

            await status.edit(
                embed=generate_embed(title=f"Removed reaction from user {user}")
            )

            try:
                await user.send(
                    "",
                    embed=generate_embed(
                        title="Disqualified from giveaway",
                        description="You've been disqualified from a giveaway in the [Trence Support server](https://discord.gg/ebDzmnv). Please reach out by messaging <@575252669443211264> if you have any questions.",
                    ),
                )
            except Forbidden:
                await status.edit(
                    embed=generate_embed(
                        title=f"Could not message user {user}", color=DANGER_COLOR
                    )
                )
                continue

            await status.edit(embed=generate_embed(title="Message sent"))

    @dev.group(name="updateowners")
    async def dev_updateowners(self, ctx):
        status = await ctx.send(
            "", embed=generate_embed(title="Updating server owners")
        )
        await update_owners(self.bot)
        await status.edit(embed=generate_embed(title="All done!"))

    @dev.group(name="override")
    async def dev_override(self, ctx, server_id: str, user: User):
        with open(pathlib.Path(__file__).parent / "owner_overrides.json") as file:
            overrides = load(file)

        if server_id in overrides.keys():
            overrides[server_id].append(user.id)
        else:
            overrides[server_id] = [user.id]

        with open(pathlib.Path(__file__).parent / "owner_overrides.json", "w") as file:
            dump(overrides, file)

        await ctx.send(
            "", embed=generate_embed(title="Override added! Updating server owners")
        )

        await update_owners(self.bot)

    @dev.group(name="slowmode", aliases=["slow"])
    async def dev_slowmode(self, ctx, channel: TextChannel, delay: int = 1):
        await channel.edit(slowmode_delay=delay)
        await ctx.send("", embed=generate_embed(title="Slowmode updated"))

    @dev.group(name="check")
    async def dev_check(self, ctx, server_id: int, user: User):
        guild = self.bot.get_guild(server_id)
        member = guild.get_member(user.id)

        if member.guild_permissions.manage_guild:
            await ctx.send(
                "",
                embed=generate_embed(
                    title=f"{user} has Manage Server permissions in {guild.name}"
                ),
            )
        else:
            await ctx.send(
                "",
                embed=generate_embed(
                    title=f"{user} does not have Manage Server permissions in {guild.name}",
                    color=DANGER_COLOR,
                ),
            )
