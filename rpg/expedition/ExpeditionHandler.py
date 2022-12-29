import random

import discord

from rpg.expedition.ExpeditionFactory import ExpeditionFactory
from rpg.expedition.views.WaitingView import WaitingView


class ExpeditionHandler:
    def __init__(self, player_handler):
        self.player_handler = player_handler
        self.expedition_factory = ExpeditionFactory(player_handler)

    @staticmethod
    def start_expedition(interaction, expedition):
        expedition.run(interaction)

    async def start_waiting(self, interaction):
        title = random.choice(list(self.expedition_factory.expeditions.keys()))
        print(title)
        expedition = self.expedition_factory.expeditions[title]
        print(expedition)
        embed = discord.Embed(title="Expedition Waiting to start", description=title)
        embed.add_field(name="Players", value="No players yet")
        embed.add_field(name="Host", value=interaction.user.name)
        print("Before View")
        view = WaitingView(interaction, expedition, embed, self.player_handler, [])
        print(interaction.message)
        await interaction.response.send_message(embed=embed, view=view)
