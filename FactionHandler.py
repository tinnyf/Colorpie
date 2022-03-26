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
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
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
        try:
            self.daily = self.read_pickle(self.file_locations["Daily"])
        except EOFError:
            self.daily = []

    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)

    def get_factions(self):
        return self.factions

    def found(self, name):
        self.factions.append(Faction(name))
        self.save_pickle(self.factions, "Factions")
        return f"Created a new faction with name: {name}"

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

    def get_permissions(self, title, faction_id):
        return get_faction_from_id(faction_id).get_permissions(title)

    def get_faction_from_id(self, faction_id):
        for faction in factions:
            if faction_id == faction.get_id():
                return faction

    def daily_data(self):
         print(len(self.daily))
         amount, text = random.choice(list(self.daily))
         return amount, text

    def get_dailys(self):
        return(self.daily)

    def daily_create(self, lst):
        try:
            self.daily.append(lst)
            self.save_pickle(self.daily, self.file_locations["Daily"])
        except AttributeError as e:
            daily = []
            daily.append(lst)
            print(text)
            self.save_pickle(self.daily, self.file_locations["Daily"])

    def daily_remove(self, lst):
        self.daily.remove(lst)
        self.save_pickle(self.daily, self.file_locations["Daily"])

    def print_daily(self):
        print(self.daily)


## test for functionality of ctx.invoked_with
##   @commands.command(aliases = ["ping"])
##   async def pong(self, ctx):
##      await ctx.send(ctx.invoked_with)
