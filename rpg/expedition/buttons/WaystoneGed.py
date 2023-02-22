import discord

from rpg.expedition.dilemma.waystone_ged_dilemma import WaystoneGedDilemma


class WaystoneGed(discord.ui.Button):

    def __init__(self, player_handler, player_id):
        self.player_id = player_id
        self.player_handler = player_handler

    async def callback(self, interaction: discord.Interaction):
        await WaystoneGedDilemma.send(interaction)
        await interaction.response.send_message(f"Waiting for {interaction.guild.get_member(self.player_handler.get_discord_reference(self.player_id)).nick} to respond")


