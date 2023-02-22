import discord
from discord.ext import commands
from discord import app_commands
from rpg.rp.location import Location
from rpg.rp.character_modal import CharacterModal
from rpg.rp.character import Character


class RP(commands.GroupCog):

    def __init__(self, player_handler, bot):
        self.player_handler = player_handler
        self.bot = bot
        self.locations = []
        self.characters = {}

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="location", description="Creates a new rp at a location of your choice!")
    async def create(self, interaction, location: str):
        if location in list(thread.name for thread in self.locations):
            await interaction.response.send_message()
        else:
            self.locations.append(Location(location, interaction.channel))

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="character", description="Creates a new character for you to rp as!")
    async def proxy(self, interaction, name: str):
        player = self.player_handler.get_player(self.player_handler.get_player_id(interaction.user))
        character = Character(interaction.user.id, name, player)
        self.characters[interaction.user.name] = name
        await interaction.response.send_modal(CharacterModal(character))

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="join", description="Adds you to an existing rp thread!")
    async def join(self, interaction, location: str, character: str):
        try:
            self.get_location(location).add_proxy(interaction.user, character)
            await interaction.response.send_message("Added your character to that thread!")
        except Exception:
            await interaction.response.send_message("That location doesn't exist!")

    def get_location(self, location: str):
        return Location(**self.rpdata.get_location(location))



