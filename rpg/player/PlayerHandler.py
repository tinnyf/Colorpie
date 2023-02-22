import pickle
from discord.ext import commands, tasks
import random

from rpg.player.Player import Player

import pandas


class PlayerHandler(commands.Cog):

    def __init__(self, bot):
        self.file_locations = {
            "Players": "src/data/players"
        }
        self.bot = bot
        self.players = []
        try:
            self.player_repo = self.read_csv("Players")
            print(self.player_repo)
            print(f"length of player_repo is {len(self.player_repo)}")
            try:
                for player in self.player_repo:
                    print(player["name"])
                    print(len(player.values()))
                    self.players.append(Player(**player))
            except Exception as e:
                print(e)
        except FileNotFoundError as e:
            print(f"Error in Playhandler: {e}")
            self.players = self.read_pickle("Players")

        self.runes = ["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
                      "Min", "Thark", "Set", "Ged", "Dorn", "Lae"]

    def create(self, user):  # This currently takes a discord_user object.
        for player in self.players:
            if player.get_discord_reference() == user.id:
                for player in self.get_players():
                    print(player.get_name())
                return ("You're already playing... stupid.")
        ID = len(self.players)
        self.players.append(Player(id=ID, name=user.name, discord_reference=user.id))
        self.save_pickle(self.players, "Players")
        for player in self.get_players():
            print(player.get_name())
        return ("Thanks for playing! Enjoy your 50 free relics")

    def read_csv(self, location):
        data_base = []
        df = pandas.read_csv(self.file_locations[location], index_col=0)
        for index, row in df.iterrows():
            data_base.append(row.to_dict())
        return data_base

    def save_csv(self, data, location):
        if not isinstance(data[1], dict):
            data = self.objects_to_dict(data)
        dataframe = pandas.DataFrame(data)
        csv = dataframe.to_csv(self.file_locations[location])

    def objects_to_dict(self, data):
        dehydrated_objects = []
        for object in data:
            dehydrated_objects.append(object.__dict__)
        return dehydrated_objects

    def read_pickle(self, location):
        with open(location, "rb") as f:
            try:
                return pickle.load(f)
            except EOFError:
                return []

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)

    def get_player_id(self, discord_member):  # This is sooo confusing
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

    def set_title(self, playerID, title):
        self.get_player(playerID).set_title(title)
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def set_last_daily(self, playerID, daily):
        self.save_csv(self.objects_to_dict(self.players), "Players")
        return self.get_player(playerID).set_last_daily(daily)

    def set_next_daily(self, playerID, amount, text):
        self.get_player(playerID).set_next_daily(amount, text)
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def get_next_daily(self, playerID):
        return self.get_player(playerID).get_next_daily()

    def get_last_daily(self, playerID, daily):
        return self.get_player(playerID).set_next_daily(daily)

    def set_devoted(self, playerID, rune):
        self.get_player(playerID).set_devoted(rune)
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def get_devoted(self, playerID):
        return self.get_player(playerID).get_devoted()

    def get_faction(self, playerID):
        return self.get_player(playerID).get_faction()

    def get_daily(self, playerID):
        return self.get_player(playerID).get_daily()

    def get_name(self, playerID):
        return self.get_player(playerID).get_name()

    def set_relics(self, playerID, relics):
        self.get_player(playerID).set_relics(relics)
        self.save_csv(self.players, "Players")

    def get_hp(self, playerID):
        return self.get_player(playerID).get_HP()

    def set_hp_max(self, playerID, HP):
        self.get_player(playerID).set_HP_max(HP)
        self.save_csv(self.players, "Players")

    def get_hp_max(self, playerID):
        return self.get_player(playerID).get_HP_max()

    def redo_hp(self, playerID):
        self.set_hp_max(playerID, random.randint(1, 4) + random.randint(1, 4) + random.randint(1, 4))
        while self.get_hp_max(playerID) < self.get_hp(playerID):
            self.set_hp_max(playerID, random.randint(1, 4) + random.randint(1, 4) + random.randint(1, 4))
        self.save_csv(self.players, "Players")

    def set_hp(self, playerID, amount):
        if amount > self.get_hp_max(playerID):
            amount = self.get_hp_max(playerID)
        self.get_player(playerID).set_HP(amount)
        self.save_csv(self.players, "Players")

    def change_hp(self, playerID, amount):
        self.set_hp(playerID, self.get_player(playerID).get_HP() + amount)
        self.save_csv(self.players, "Players")

    def get_relics(self, playerID):
        return self.get_player(playerID).get_relics()

    def get_discord_reference(self, playerID):
        return self.get_player(playerID).get_discord_reference()

    def set_daily(self, playerID, when):
        self.get_player(playerID).set_daily(when)
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def randomise_runes(self, playerID):
        self.get_player(playerID).set_random_rune_scores()
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def get_rune_scores(self, playerID):
        return self.get_player(playerID).get_rune_scores()

    def increase_rune(self, playerID, rune, amount):
        self.get_player(playerID).increase_rune(rune, amount)
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def daily_runes(self, playerID):
        message = None
        try:
            for rune, score in (self.get_player(playerID).get_rune_scores()).items():
                if score == 0 or random.randint(1, score) == score:
                    self.increase_rune(playerID, rune, 1)
                    if score == 19:
                        message = "It seems something has changed within. Something has shifted. Power builds within you, and you fear it may someday overspill."
                        self.save_csv(self.objects_to_dict(self.players), "Players")
                        return message
        except TypeError as e:
            print("Error in daily_runes: ", e)

    def merge(self, originalID, newID):
        self.get_player(newID).set_id(originalID)
        self.save_csv(self.objects_to_dict(self.players), "Players")
        return "Those two players are now one!"

    def test(self, playerID, difficulty, rune):
        total = 0
        for i in range(difficulty):
            total += random.randint(1, 6)
        print(f"Failed check if: {self.get_rune_scores(playerID)[rune]} is bigger than {total}  ")
        return (self.get_rune_scores(playerID)[rune] - total)

    def force_founder(self, player_ID, faction_id):
        player = self.get_player(player_ID)
        player.set_faction_id(faction_id)
        player.set_title("Founder")

    def add_status(self, player_ID, status):
        print("Hi! I'm adding a status look at me!")
        self.get_player(player_ID).add_status(status)
        self.save_csv(self.objects_to_dict(self.players), "Players")

    def get_status(self, player_ID):
        return self.get_player(player_ID).get_status()

    def remove_status(self, player_ID, status):
        self.get_player(player_ID).remove_status(status)
