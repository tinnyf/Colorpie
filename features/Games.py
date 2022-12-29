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

class TruthGame(commands.GroupCog, name = "2truths"):

    def __init__(self, bot):
        self.bot = bot
        super().__init__()
        self.file_locations = {
            "truths": "src/data/2T1L", #[ {user_id: int , truths[] }}
            "scores": "src/data/scores"
        }
        try:
            self.truths = self.read_pickle(self.file_locations["truths"])
            print(self.truths)
        except EOFError:
            self.truths = []
        try:
            self.scores = self.read_pickle(self.file_locations["scores"])
        except EOFError:
            self.scores = {}


    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    async def save_pickle(self, data, location):
        print("Updated")
        with open(location, "wb") as f:
            pickle.dump(data, f)
        print("Updated")


    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = 'info', description = "Explains the 2t1l game!")
    async def truths(self, interaction: discord.Interaction):
        await interaction.response.send_message("This is a game wherein you have to pick the lie out of three options! To play, do /2t1l play. To register your own truths and lies, do /2t1l add!")

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = 'play')
    async def play(self, interaction:discord.Interaction):
        player = interaction.user
        truths_temp = random.sample(self.truths, len(self.truths))
        truths_all = []
        for pair in truths_temp:
            if not pair["id"] == interaction.user.id:
                truths_all.append(pair)
        score = 0

        def get_quiz(user, truths, index): #returns user, [lie, true, true]
            while True:
                print(f"Iteration: {index}")
                print(truths[index])
                id = truths[index]["id"]
                truths_update = truths[index]["truths"]
                if not id == user.id:
                    break
                index = index + 1
            return id, truths_update, index

        def update_embed(embed, user, truths):
            embed.set_author(name=user.display_name,icon_url=user.display_avatar.url )
            for count,value in enumerate(random.sample(truths, 3)):
                try:
                    embed.set_field_at(count, name = f"Option {count + 1 }.", value = value)
                except IndexError:
                    embed.add_field(name = f"Option {count + 1}.", value = value)
            embed.color = user.color
            return embed

        async def good_callback(interaction: discord.Interaction):
            print("interaction id incoming!")
            print(interaction.id)
            nonlocal index
            nonlocal score
            nonlocal embed
            nonlocal correct
            for truth in self.truths:
                if truths_all[index]["truths"] == truth["truths"]:
                    try:
                        truth["right_counter"] += 1
                    except KeyError:
                        truth["right_counter"] = 1
            await self.save_pickle(self.truths, self.file_locations["truths"])
            index += 1
            score += 1
            if index > len(truths_all):
                await interaction.response.send_message(f"You got through all of the questions! Wow!")
                self.scores[interaction.user.id] = score
                await self.save_pickle(self.scores, self.file_locations["scores"])
                await interaction.message.delete()
                return True
            try:
                id, truths, index = get_quiz(interaction.user, truths_all, index)
            except IndexError:
                await interaction.response.send_message(f"You got through all of the questions! Wow!")
                self.scores[interaction.user.id] = score
                await self.save_pickle(self.scores, self.file_locations["scores"])
                await interaction.message.delete()
                return True

            embed = update_embed(embed, interaction.guild.get_member(id), truths)
            await interaction.response.edit_message(embed=embed, view=view)

            for count, field in enumerate(embed.fields):
                if field.value == truths_all[index]["truths"][1]:
                    correct = count + 1
                    print ("Correct value created!")
                    print(f"Correct value = {correct}")

            for Button in view.children:
                if int(Button.custom_id) == correct:
                    Button.callback = good_callback
                else:
                    Button.callback = bad_callback


        async def bad_callback(interaction: discord.Interaction):
            for truth in self.truths:
                if truths_all[index]["truths"] == truth["truths"]:
                    try:
                        truth["wrong_counter"] += 1
                    except KeyError:
                        truth["wrong_counter"] = 1

            try:
                if score > self.scores[interaction.user.id]:
                    await interaction.response.send_message(f"You beat your high score with a score of {score}!")
                    self.scores[interaction.user.id] = score
                else:
                    await interaction.response.send_message(f"You scored {score} points, {self.scores[interaction.user.id] -score} points away from your personal best!" )
            except KeyError:
                await interaction.response.send_message(f"You scored {score} points!")


            await self.save_pickle(self.scores, self.file_locations["scores"])
            await self.save_pickle(self.truths, self.file_locations["truths"])
            await interaction.message.delete()
            return False


        embed = discord.Embed(title = "Two truths, One Lie!")
        embed.set_footer(text = "Hit the button corresponding to the answer you think is a lie!" )
        view = discord.ui.View()
        index = 0
        id, truths, index = get_quiz(interaction.user, truths_all ,index)
        embed = update_embed(embed, interaction.guild.get_member(id), truths)

        async def check(interaction: discord.Interaction):
            return interaction.user == player
        view = discord.ui.View()
        view.interaction_check = check


        for count, field in enumerate(embed.fields):
            if field.value == truths_all[index]["truths"][1]:
                correct = count + 1
                print ("Correct value created!")
                print(f"Correct value = {correct}")

        view.add_item(discord.ui.Button(
        label = "Option one is the false one!", custom_id = "1"))
        view.add_item(discord.ui.Button(
        label = "Option two can't be true!", custom_id = "2"))
        view.add_item(discord.ui.Button(
        label = "Option three seems wrong to me!", custom_id = "3"))
        ui = await interaction.response.send_message(view = view, embed = embed)
        for Button in view.children:
            if int(Button.custom_id) == correct:
                Button.callback = good_callback
            else:
                Button.callback = bad_callback

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = "add", description = "Add your own two truths and a lie questions!")
    async def truths_add(self, interaction: discord.Interaction):
        modal = discord.ui.Modal(title = "Add your two truths and a lie!")
        lie_input = discord.ui.TextInput(label = "One lie", max_length = 1024)
        true_input_1 = discord.ui.TextInput(label = "One Truth (of two)", max_length = 1024)
        true_input_2 = discord.ui.TextInput(label = "Another Truth", max_length = 1024)


        async def callback(interaction: discord.Interaction):
            self.truths.append({"id": interaction.user.id, "truths": [lie_input.value,true_input_1.value,true_input_2.value] })
            await self.save_pickle(self.truths, self.file_locations["truths"])
            await interaction.response.send_message("Thank you for adding two truths and a lie :D", ephemeral = True)

        modal.add_item(lie_input)
        modal.add_item(true_input_1)
        modal.add_item(true_input_2)
        modal.on_submit = callback
        await interaction.response.send_modal(modal)

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = "stats", description = "View your stats")
    async def truth_stats(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Stats for your questions!")
        embed.set_author(name=interaction.user.display_name,icon_url= interaction.user.display_avatar.url )
        for count, ltt in enumerate(self.truths):
            if ltt["id"] == interaction.user.id:
                try:
                    right = ltt["right_counter"]
                    wrong = ltt["wrong_counter"]
                    embed.add_field(name= f"Question {count+1}", value = f"Right Answers: {right}, Wrong Answers: {wrong}")
                except KeyError:
                    pass
        await interaction.response.send_message(embed=embed)

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = "leaderboard", description = "View high scores!")
    async def lb(self, interaction: discord.Interaction):
        embed = discord.Embed(title = "Two Truths Leaderboard!")
        embed.description = ""
        greatest = Counter(self.scores).most_common(10)
        for count, line in enumerate(greatest):
            embed.description = embed.description + f'[{count + 1}]: {interaction.guild.get_member(line[0]).display_name} - {line[1]} \n'
        await interaction.response.send_message(embed=embed)

    @app_commands.default_permissions(manage_messages = True)
    @app_commands.command(name = "reset_qs")
    async def reset(self, interaction: discord.Interaction):
        for truth in self.truths:
            truth["wrong_counter"] = 0
            truth["right_counter"] = 0
        await self.save_pickle(self.truths, self.file_locations["truths"])
        await interaction.response.send_message("Reset question probablities")
