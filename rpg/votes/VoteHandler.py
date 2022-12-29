import pickle

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

from rpg.votes.Vote import Vote



class VoteHandler(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.file_locations = {
        "Votes": "src/data/Vote"
            }

        try:
            self.votes = self.read_pickle(self.file_locations["Votes"])
        except EOFError:
            self.votes = []

    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    def save_pickle(self, data, location):
        print("Updated")
        with open(location, "wb") as f:
            pickle.dump(data, f)
        print("Updated")

    def get_votes(self):
        return self.votes

    def get_components(self, election):
        return election.get_components()

    def create(self, name, emoji_id, types): #Types is a list
        self.votes.append(Vote(name, emoji_id, types))
        self.save_pickle(self.votes, self.file_locations["Votes"])
        return "Created a new vote!"

    def get_election_from_value(self,value): #Uses Label as value?
        for vote in self.votes:
            if vote.name == value:
                return vote

    def get_option_from_value(self, election, value):
        return election.get_options()[value]

    def add_option(self, election, option, componentdict):
        election.add_option(option, componentdict)
        self.save_pickle(self.votes, self.file_locations["Votes"])
        return "Added a new option!"

    def get_types(self, election):
        return election.get_types()

    def get_emoji(self, election):
        return election.get_emoji()

    def remove_option(self, election, option):
        election.remove_option(option)
        self.save_pickle(self.votes, self.file_locations["Votes"])

    def remove_election(self, election):
        self.votes.remove(election)
        self.save_pickle(self.votes, self.file_locations["Votes"])

    def increment_option(self, election, option, increment):
        election.increment_option(option, increment)
        self.save_pickle(self.votes, self.file_locations["Votes"])
        return True

    def add_player_option(self, election, option, playerID):
        election.add_player_to_option(option, playerID)
        self.save_pickle(self.votes, self.file_locations["Votes"])

    def get_option_players(self, election, option):
        return election.get_option_players(option)
