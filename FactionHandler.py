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
from Player import Player
from Faction import Faction
import pickle


class FactionHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.file_locations = {
            "Factions": "src/data/factions",
            "Lore": "src/data/lore",
            "Daily": "src/data/daily"
        }
        try:
            self.factions = self.read_pickle("Factions")
        except EOFError:
            self.factions = []
        self.lore = self.read_pickle("Lore")

    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)

    def get_factions(self):
        return self.factions

    def get_role_id(self, faction_id):
        return self.get_faction_from_id(faction_id).get_role_id()

    def add_member(self, member_id, faction_id):
        self.get_faction_from_id(faction_id).add_member(member_id)

    def found(self, name, role_id):
        self.factions.append(Faction(name, role_id))
        self.save_pickle(self.factions, "Factions")
        return f"Created a new faction with name: {name}"

    def get_permissions(self, title, faction_id):
        return self.get_faction_from_id(faction_id).get_permissions(title)

    def get_faction_from_id(self, faction_id):
        return self.factions[faction_id]

    def add_shop_item(self, faction_id, item, values):
        self.get_faction_from_id(faction_id).add_shop_item(item, values)
        self.save_pickle(self.factions, "Factions")

    def add_perk(self, faction_id, perk):
        self.get_faction_from_id(faction_id).add_perk(perk)
        self.save_pickle(self.factions, "Factions")

    def add_member(self, faction_id, player_id):
        self.get_faction_from_id(faction_id).add_member(player_id)
        self.save_pickle(self.factions, "Factions")

    def remove_perk(self, faction_id, perk):
        self.get_faction_from_id(faction_id).remove_perk(perk)
        self.save_pickle(self.factions, "Factions")

    def set_emoji(self, emoji_id):
        self.get_faction_from_id(faction_id).set_emoji(emoji_id)
        self.save_pickle(self.factions, "Factions")

    def set_name(self, name):
        self.get_faction_from_id(faction_id).set_name(name)
        self.save_pickle(self.factions, "Factions")

    def register(self, word, text):
        try:
            self.lore[word.lower()] = text
            self.save_pickle(self.lore, "Lore")
        except AttributeError as e:
            lore = {}
            lore[word.lower()] = text
            print(text)
            self.save_pickle(lore,"Lore")

    def discover(self, word):
        return self.lore[word.lower()]



















## test for functionality of ctx.invoked_with
##   @commands.command(aliases = ["ping"])
##   async def pong(self, ctx):
##      await ctx.send(ctx.invoked_with)
