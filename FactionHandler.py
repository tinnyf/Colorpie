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
from CpUser import CpUser
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption

master_role = 776142246008455188
guild_id = 695401740761301056

class FactionHandler(commands.Cog):
    file_locations = {
        "Factions": "src/data/faction.json",
    }

    def __init__(self, bot):
        self.bot = bot
        self.factions = self.read_json("Factions") #Possibly the issue is that this is static?

    def read_json(self, location):
        with open(self.file_locations[location], "r") as json_file_r0:
            try:
                return json.load(json_file_r0)
            except json.decoder.JSONDecodeError:
                return {}

    def get_role_from_id(self, role_id):
        return (self.bot.get_guild(guild_id)).get_role(role_id)

    def save_json_dict(self, dict, location):
        with open(self.file_locations[location], "w") as json_file:
            json.dump(dict, json_file)

    def interaction_check(interaction):
        return interaction.user == ctx.author and i.message.id == sent_message.id

    async def invite_process(self, invitee, faction):
        await invitee.create_dm()
        await invitee.dm_channel.send(f"You've recieved an invite to faction: {faction}",
        components = [
            Button(Label = "Accept", style = 3, id = "AcceptButton"),
            Button(Label = "Refuse", style = 4, id = "RefuseButton")
        ])
        interaction = self.bot.wait_for("button_click", check = interaction_check(i))
        if interaction.custom_id == "AcceptButton":
            #DoAcceptStuff
            await ctx.send("You accepted this invite!")
        if interaction.custom_id == "RefuseButton":
            #DoRefuseStuff
            await ctx.send("You rejected this invite!")




    def found(self, name):
        dict_contents = {}
        self.factions[name] = {
            "Members": {},
            "Emoji": False,
            "Name": name,
            "Titles": {},
            "Description": "Description would go here",
            "perks": [],
        }
        self.save_json_dict(self.factions, "Factions")
        return f"Created a new faction with name: {name}"

    async def invite(self, ctx, invited):
        if CpUser.has_permission(self.factions, ctx.author, "Send Invites"): #Currently factions doesn't exist in the right space
            await self.invite_process(invited, CpUser.get_faction)
        elif self.get_role_from_id(master_role) in ctx.author.roles:
            await self.faction_select(ctx)
        else:
            return "You don't have permission to invite someone to your faction."

## test for functionality of ctx.invoked_with
##   @commands.command(aliases = ["ping"])
##   async def pong(self, ctx):
##      await ctx.send(ctx.invoked_with)
