import discord
from discord import app_commands
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
from collections import Counter

class Qotd(commands.GroupCog, name = "qotd"):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.file_locations = {
            "questions": "src/data/questions", #[ {user_id: int , truths[] }}
        }
        try:
            self.questions = self.read_pickle(self.file_locations["questions"])
        except EOFError:
            self.questions = {}

    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    async def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)


    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = 'info')
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message("Please use /QOTD add to add your own questions. QoTD's will be posted daily!")

    async def add_autocomplete(self, interaction: discord.Interaction, current:str):
        return [
            app_commands.Choice(name = 'Silly QOTD', value = "Silly"),
            app_commands.Choice(name = 'Serious QOTD', value = "Serious")
        ]


    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.autocomplete(option = add_autocomplete)
    @app_commands.command(name = "add")
    async def add(self, interaction: discord.Interaction, option: str ):
        modal = discord.ui.Modal(title = "Add your own question here!")
        question_input = discord.ui.TextInput(label = "Please add your question!", max_length = 1024)

        async def callback(interaction: discord.Interaction):
            self.questions[random.randint(1,1000000)] = {"type" : option, "text" : question_input.value}
            await self.save_pickle(self.questions, self.file_locations["questions"])
            await interaction.response.send_message("Thank you for adding a question, it's been saved!")

        modal.on_submit = callback
        modal.add_item(question_input)
        await interaction.response.send_modal(modal)


    @app_commands.default_permissions(manage_messages = True)
    @app_commands.autocomplete(option = add_autocomplete)
    @app_commands.command(name = "post")
    async def post(self, interaction: discord.Interaction, option: str):
        key, current = random.choice(list(self.questions.items()))
        c = 0
        while not current ["type"] == option:
            key, current = random.choice(list(self.questions.items()))
            c += 1
            if c > 30:
                await interaction.response.send_message("We don't have any of those in stock, please get some more!")
                return False
        embed = discord.Embed(title = f"{option} Question of the day!")
        embed.description = current["text"]
        embed.set_footer(text = f"Please answer in Qotd-Answers! Keep discussion to general channels!")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Thank you for your message!", ephemeral = True)
        self.questions.pop(key)
        await self.save_pickle(self.questions, "questions")
