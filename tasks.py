import discord
import discord.ext
from discord.ext import commands, tasks
import random

class Looper(commands.Cog):
    def __init__(self):
        try:
            self.index = self.read_pickle("src/data/index")
        except EOFError:
            self.index = 0
        try:
            self.messages = self.read_pickle("src/data/index")
            #messages[type][time]
        except EOFError:
            self.messages = {}
        self.counter.start()


    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)

    @tasks.loop(seconds=60.0)
    async def counter(self):
        self.index += 1
        try:
            self.messages["repeating"][str(index)]

        except
