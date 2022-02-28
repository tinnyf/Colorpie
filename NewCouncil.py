import discord
import discord.ext
from discord.ext import commands, tasks
import random
import json
import typing
import asyncio
import cp_converters
from cp_converters import SmartMember
import datetime
from datetime import date, time, datetime
from discord.ext.commands import bot
from FactionClasses import FactionMember
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

master_role = 776142246008455188
guild_id = 695401740761301056

class cp_NewCouncil(commands.Cog):
    file_locations =  {
        "Factions": 'src/data/faction.json',
    }

    def __init__(self,bot):
        self.bot = bot
        self.faction_dict = self.read_json("Factions")

    def read_json(self, location):
        with open(self.file_locations[location], "r" ) as json_file_r0:
            try:
                return json.load(json_file_r0)
            except json.decoder.JSONDecodeError:
                return {}

    def get_role_from_id(self, role_id):
        return (self.bot.get_guild(695401740761301056)).get_role(role_id)

    def save_json_dict(self, dict, location):
        with open(self.file_locations[location], 'w') as json_file:
            json.dump(dict,json_file)

    async def faction_select(self, ctx):
        subcomponents = []
        for faction, contents in self.faction_dict.items():
            subcomponent = SelectOption(
                label = contents["Name"] , emoji = self.bot.get_emoji(947539895071670302), description = contents["Description"], value = faction
            )
            if contents["Emoji"]:
                subcomponent.emoji=self.bot.get_emoji(contents["Emoji"])
            subcomponents.append(subcomponent)
        await ctx.send(
            "Choose a faction!",
            components = [
                Select(options = subcomponents, max_values = 1, id = "faction_selector")
            ]
        )

        return await self.bot.wait_for("select_option")

    @commands.command()
    async def found(self, ctx, name):
        dict_contents = {}
        self.faction_dict[name] = {"Members": {}, "Emoji": False, "Name": name, "Titles": {}, "Description" : "Description would go here", "perks": []}
        self.save_json_dict(self.faction_dict, "Factions") #Is it worth binding faction_dict with the key "Factions" somewhere?
        await ctx.send(f"Created a new faction with name: {name}")

    @commands.command()
    async def invite(self, ctx, invited:SmartMember):
        if FactionMember.has_permission(self.faction_dict, ctx.author, "Send Invites"):
            await self.invite_process(invited, FactionMember.get_faction) #Is it preferred to create a variable, then check if false, then use as arg?
        elif self.get_role_from_id(master_role) in ctx.author.roles:
            await self.faction_select(ctx)
        else:
            await ctx.send("You're not in a faction, so you can't invite anyone to one")

## test for functionality of ctx.invoked_with
##   @commands.command(aliases = ["ping"])
##   async def pong(self, ctx):
##      await ctx.send(ctx.invoked_with)
