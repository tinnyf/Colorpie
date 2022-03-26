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
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
import pickle


#Todo: store players as dehydrated values not as classinstances - get them from somewhere else
class PlayerHandler(commands.Cog):
    file_locations = {
        "Players": "src/data/players"
    }


    def __init__(self, bot):
        self.bot = bot
        self.players = self.read_pickle("Players")
        self.runes = ["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
        "Min", "Thark", "Set", "Ged", "Dorn", "Lae"]

    def create(self, user): #This currently takes a discord_user object.
        for player in self.players:
            if player.get_discord_reference() == user.id:
                for player in self.get_players():
                    print(player.get_name())
                return("You're already playing... stupid.")
        ID = len(self.players)
        self.players.append(Player(user.id, ID, user.name))
        self.save_pickle(self.players, "Players")
        for player in self.get_players():
            print(player.get_name())
        return("Thanks for playing! Enjoy your 50 free relics")


    def read_pickle(self, location):
        with open(location, "rb") as f:
            try:
                return pickle.load(f)
            except EOFError:
                return []

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)

    def get_player_id(self, discord_member): #This is sooo confusing
        for player in self.get_players():
            if player.get_discord_reference() == discord_member.id:
                return player.id
        return False

    def get_player(self, playerID):
        for player in self.players:
            if playerID == player.get_id():
                return player

    def get_players(self):
        print(f"{len(self.players)} are playing right now")
        return self.players

    def get_title(self, playerID):
        return self.get_player(playerID).get_title()

    def get_faction(self, playerID):
        return self.get_player(playerID).get_faction()

    def get_daily(self, playerID):
        return self.get_player(playerID).get_daily()

    def get_name(self, playerID):
        return self.get_player(playerID).get_name()

    def set_relics(self, playerID, relics):
        self.get_player(playerID).set_relics(relics)
        self.save_pickle(self.players, "Players")

    def get_relics(self, playerID):
        return self.get_player(playerID).get_relics()

    def set_daily(self, playerID, when):
        self.get_player(playerID).set_daily(when)
        self.save_pickle(self.players, "Players")

    def randomise_runes(self, playerID):
        self.get_player(playerID).set_random_rune_scores()
        self.save_pickle(self.players, "Players")

    def get_rune_scores(self, playerID):
        return self.get_player(playerID).get_rune_scores()

    def increase_rune(self, playerID, rune, amount):
        self.get_player(playerID).increase_rune(rune,amount)

    def daily_runes(self, playerID):
        message = None
        for rune, score in (self.get_player(playerID).get_rune_scores()).items():
            if random.randint(1, score) == score:
                self.increase_rune(playerID, rune, 1)
                if score == 19:
                    message = "It seems something has changed within. Something has shifted. Power builds within you, and you fear it may someday overspill."
        return message

    def merge(self, originalID, newID):
        self.get_player(newID).set_id(originalID)
        return "Those two players are now one!"
