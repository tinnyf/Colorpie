import discord
from discord import app_commands
from discord.ext import commands
from moderation.Rules import Rules
from moderation.Channels import Channels
from moderation.Color import Color
from moderation.WelcomeView import WelcomeView
import traceback


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.rules = Rules()
        self.channels = Channels()
        self.welcome_channel = 695755815612710982

        self.colours = {
        "White": Color(bot, 695402035595444384, 759088944201072672, 719986148453384192),
        "Blue": Color(bot, 695402040771346473, 759089040485777462, 719986148235018291),
        "Black": Color(bot, 695402050300674079, 759089094138789959, 719986148692197527),
        "Red": Color(bot, 695402020592549890,759089174170042388, 719986148474355722),
        "Green": Color(bot, 695402051491856455, 759089270127722536,719986148448927744),
        }


    @app_commands.command(name="rule")
    async def rule(self, interaction: discord.Interaction, rule: int):
        try:
            await interaction.response.send_message(embed=self.rules.rules_embed(rule))
        except KeyError:
            await interaction.response.send_message("We don't have that rule!")

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="channel")
    async def channel(self, interaction: discord.Interaction, channel: str):
        try:
            await interaction.response.send_message(embed=self.channels.channel_embed(interaction.guild, channel))
        except KeyError:
            await interaction.response.send("We don't have that channel!")


    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name = "welcomer")
    async def welcomer(self, interaction):
        try:
            role = interaction.guild.get_role(1071790927066189854)
            await interaction.user.add_roles(role)
            await interaction.response.send_message("Given you the welcomer role!", ephemeral = True)
        except Exception:
            print(traceback.format_exc())
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command(name="clear")
    async def clear(self, interaction: discord.Interaction, number: int):
        messages = [message async for message in interaction.channel.history(limit=number, oldest_first=False)]
        for message in messages:
            print(message)
            await message.delete()
        await interaction.response.send_message(f"Cleared {number} messages!")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        print("Seeing member join")
        try:
            welcome_channel = member.guild.get_channel(self.welcome_channel)
            welcome_message = "Welcome to r/Colorpie! We're a collection of nerds, mtgplayers, amateur philosophers and others, and we're delighted to meet you! To start, please pick a color by pressing a button below!"
            for colour, instance in self.colours.items():
                if isinstance(instance.emoji, int):
                    instance.emoji = await member.guild.fetch_emoji(instance.emoji)
            view = WelcomeView(member, self.bot, self.colours)
            print("Sending welcome message")
            await welcome_channel.send(welcome_message, view=view)
        except Exception:
            print(traceback.format_exc())

