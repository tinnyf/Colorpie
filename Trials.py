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

class Trials(commands.GroupCog, name = "trials"):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.file_locations = {
            "trials": "src/data/trials", #[ {user_id: int , truths[] }}
        }
        try:
            self.trials = self.read_json_dict(self.file_locations["trials"])
        except EOFError:
            self.trials = {}
        print(self.trials)

    def read_json_dict(self, location):
        try:
            with open(location) as f:
                return json.load(f)
        except FileNotFoundError:
            print("Warning: Trials not found")
            return {}

    async def save_json_dict(self, data, location):
        with open(location, "w") as f:
            json.dump(data, f)

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = 'info')
    async def info(self, interaction: discord.Interaction):
        await interaction.response.send_message("Please use /trials add to register your own short trial, or use /trials browse to view them!")

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = 'add')
    async def add(self, interaction: discord.Interaction, option: str):
        modal = discord.ui.Modal(title = "Make your 4 question trial!")
        for i in range(4):
            question_input= discord.ui.TextInput(label = "Please add your question!", max_length =256)
            modal.add_item(question_input)

        async def callback(interaction: discord.Interaction):
            questions = []
            for text_input in modal.children:
                print(text_input.label)
                questions.append(text_input.value)
            self.trials[option] = questions
            await self.save_json_dict(self.trials, self.file_locations["trials"])
            await interaction.response.send_message("Saved your trial!", ephemeral = True)

        modal.on_submit = callback
        await interaction.response.send_modal(modal)

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = 'browse')
    async def browse(self, interaction: discord.Interaction):
        buttons = []
        for name, trial in self.trials.items():

            async def callback(interaction: discord.Interaction):
                print(self.trials[name])
                modal = self.get_modal(name)
                await interaction.response.send_modal(modal)
                view.delete

            button = discord.ui.Button(label = name, style = discord.ButtonStyle.primary)
            button.callback = callback
            buttons.append(button)

        view = discord.ui.View()
        for button in buttons:
            view.add_item(button)
        await interaction.response.send_message('See a list of trials you could do!', view = view, ephemeral = True)

    async def undertake_autocomplete(self,interaction: discord.Interaction, current:str):
        options = []
        for trial in self.trials.keys():
            options.append(trial)
        return options

    def get_modal(self, name):
        modal = discord.ui.Modal(title = name)
        for question in self.trials[name]:
            modal.add_item(discord.ui.TextInput(label = "See text for question!", placeholder = question,  max_length = 4000))

        async def callback(interaction: discord.Interaction):
            embeds = []
            for text_input in modal.children:
                title = text_input.placeholder
                desc = text_input.value
                embed = discord.Embed(title = title, description = desc)
                embeds.append(embed)
            await interaction.response.send_message(embeds=embeds)

        modal.on_submit = callback
        return modal


    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.autocomplete(option = undertake_autocomplete)
    @app_commands.command(name = 'undertake')
    async def undertake(self, interaction: discord.Interaction, option:str):
        modal = self.get_modal(option)
        modal.on_submit = callback
        await interaction.response.send_modal(modal)
