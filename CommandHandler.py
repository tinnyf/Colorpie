import discord
import discord.ext
from discord.ext import commands, tasks
import typing
import asyncio
from discord.ext.commands import bot
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from CpUser import CpUser
from FactionHandler import FactionHandler
import cp_converters
from cp_converters import SmartMember

class CommandHandler(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.faction_handler = FactionHandler(bot)

    @commands.command()
    async def found(self, ctx, name):
        await ctx.send(self.faction_handler.found(name))

    @commands.command()
    async def invite(self, ctx, invited:SmartMember):
        print (invited.nick)
        await ctx.send(await self.faction_handler.invite(ctx, invited))

    async def faction_select(self, ctx):
        subcomponents = []
        for faction, contents in self.factions.items():
            subcomponent = SelectOption(
                label = contents["Name"],
                emoji = self.bot.get_emoji(master_role),
                description = contents["Description"],
                value = faction
            )
            if contents["Emoji"]:
                subcomponent.emoji = self.bot.get_emoji(contents["Emoji"])
            subcomponents.append(subcomponent)
        await ctx.send(
            "Choose a faction!",
            components = [
                Select(
                    options = subcomponents,
                    max_values = 1,
                    id = "faction_selector"
                )
            ]
        )

        return await self.bot.wait_for("select_option")
