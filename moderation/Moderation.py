import discord
from discord import app_commands
from discord.ext import commands
from moderation.Rules import Rules
from moderation.Channels import Channels

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rules = Rules()
        self.channels = Channels()

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = "rule")
    async def rule(self, interaction:discord.Interaction, rule: int):
        try:
            await interaction.response.send_message(embed = self.rules.rules_embed(rule))
        except KeyError:
            await interaction.response.send_message("We don't have that rule!")

    @app_commands.default_permissions(use_application_commands = True)
    @app_commands.command(name = "channel")
    async def channel(self, interaction: discord.Interaction, channel: str):
        try:
            await interaction.response.send_message(embed = self.channels.channel_embed(interaction.guild, channel))
        except KeyError:
            await interaction.response.send("We don't have that channel!")

    @app_commands.default_permissions(manage_messages = True)
    @app_commands.command(name = "clear")
    async def clear(self, interaction: discord.Interaction, number: int):
        messages = [message async for message in interaction.channel.history(limit = number, oldest_first = False)]
        for message in messages:
            print(message)
            await message.delete()
        await interaction.response.send_message(f"Cleared {number} messages!")
