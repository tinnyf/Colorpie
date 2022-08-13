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
import pickle
import csv
import pandas


class DailyHandler(commands.Cog):

    def __init__(self, bot, playerhandler):
        self.file_locations = {
            "Daily": "src/data/daily"
        }
        try:
            self.daily = self.read_pickle(self.file_locations["Daily"])
        except EOFError:
            self.daily = []
        self.player_handler = playerhandler

    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)


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

    async def daily_extra(self, text, player_id):
        message = False
        if "Minted on the ascension of Tan-Mjol" in text or "dead Reclaimer scout" in text:
            t = self.player_handler.test(player_id, 2, "Yol" )
            if t > 0:
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + (5*t))
                message = f"You made {5*t} extra relics from your excellent negotation skills!"

        elif "Enamelled map" in text:
            t = self.player_handler.test(player_id, 5, "Ged")
            if t > 0:
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - 20)
                message = f"Inspired, you shift the arms to your current positions. The stars shift above you, and radiant light shines directly down upon you. You are empowered by the rune Ged. However, the item was consumed before you got your relics."
                self.player_handler.increase_rune(player_id, "Ged", 1)
                if self.player_handler.get_rune_scores(player_id)["Ged"] == 20:
                    await ctx.send("You explode with brilliant light. You are now a wielder of Ged, tied forever in spirit to this spot. Contact tinny.")

        elif "Money is money, right?" in text:
            player = random.choice(self.player_handler.get_players())
            adv = self.player_handler.get_rune_scores(player_id)["Yol"] - player.get_rune_scores()["Kviz"]
            if adv > 0:
                message = f"You successfully mugged {player.name}, they lose 20 relics"
                player.give_relics(-20)
            elif adv < -5:
                message =  f"{player.name} seriously hurt you. Your stats are damaged."
                self.player_handler.increase_rune(player_id, random.choice(self.player_handler.get_rune_scores(player_id).keys()), -1)

        elif "Unfortunately, the light is temperamental" in text:
            if self.player_handler.test(player_id, 3, "Stiya") > 0:
                message = "You're able to hold the light together, creating a torch that will never extinguish. Inside, the rune Stiya burns, and strengthens you."
                self.player_handler.increase_rune(player_id, "Stiya", 1)
                if self.player_handler.get_rune_scores(player_id)["Stiya"] == 20:
                    await ctx.send("You glow with the light of the makers. You are now a wielder of Stiya, the torch your locus of creation.")

        elif "chunk of glass is wedged in the earth" in text:
            if self.player_handler.test(player_id, 3, "Min") > 0:
                message = "Reflected in the glass, you can see more and more glass, a conglomerate that holds the sunlight in place, lighting the capital even at night."

        elif "collar of bronze ends" in text:
            adv = self.player_handler.test(player_id, 2, "Dorn") > 0
            if adv > 0:
                message  = "You are imbued with healing magic that allows you to heal injured players, making their medical bills cheaper and letting them work harder. {adv} players get 10 relics each, but they gave you half each!"
                players = random.choices(self.player_handler.get_players(), k = adv)
                for player in players:
                    player.set_relics(player.get_relics() + 5)
                    s = ", "
                    self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + 5 )
                message = message + f" Those players are {s.join(players)}, by the way"

        return(message)
