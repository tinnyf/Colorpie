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

class Question():
        def __init__(self, type, message):
            self.type = type
            self.message = message

        def __str__(self):
            return self.message()


class Qotd(commands.GroupCog, name = "qotd"):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.file_locations = {
            "questions": "src/data/questions", #[ {user_id: int , truths[] }}
        }
        self.questions = []
        for question in self.read_pickle("questions"):
            self.questions.append(Question(**question))

    def read_pickle(self, location):
        try:
            with open(self.file_locations[location], "rb") as f:
                return pickle.load(f)
        except EOFError:
            return {}

    async def save_pickle(self, data, location):
        with open(location, "wb") as f:
            dehydrated = []
            for question in data:
                dehydrated.append(question.__dict__)
                pickle.dump(dehydrated, f)


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
    @app_commands.autocomplete(type = add_autocomplete)
    @app_commands.command(name = "add")
    async def add(self, interaction: discord.Interaction, type: str ):
        modal = discord.ui.Modal(title = "Add your own question here!")
        question_input = discord.ui.TextInput(label = "Please add your question!", max_length = 1024)

        async def callback(interaction: discord.Interaction):
            self.questions.append(Question(type, question_input.value))
            await self.save_pickle(self.questions, self.file_locations["questions"])
            await interaction.response.send_message("Thank you for adding a question, it's been saved!")

        modal.on_submit = callback
        modal.add_item(question_input)
        await interaction.response.send_modal(modal)


    @app_commands.default_permissions(manage_messages = True)
    @app_commands.autocomplete(type = add_autocomplete)
    @app_commands.command(name = "post")
    async def post(self, interaction: discord.Interaction, type: str):
        for question in self.questions:
            if question.type == type:
                new = question
                self.questions.remove(question)
                break

        embed = discord.Embed(title = f"{type} Question of the day!")
        embed.description = new.message
        embed.set_footer(text = f"Please answer in Qotd-Answers! Keep discussion to general channels!")
        await interaction.channel.send(embed=embed)
        await interaction.response.send_message("Thank you for your message!", ephemeral = True)
        await self.save_pickle(self.questions, self.file_locations["questions"])
