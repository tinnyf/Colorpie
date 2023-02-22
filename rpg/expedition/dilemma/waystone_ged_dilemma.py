import discord

from rpg.expedition.dilemma.dilemma import Dilemma
from rpg.expedition.views.waystone_ged_dilemma_view import WaystoneGedDilemmaView


class WaystoneGedDilemma(Dilemma):
    def __init__(self, player_id, player_handler, expedition, interaction):
        super().__init__(player_handler, player_id)
        self.view = WaystoneGedDilemmaView(interaction, expedition, player_handler)
        self.embed = self.get_embed()

    def get_embed():
        embed = discord.Embed(title="A monument to Ged",
                              description="Ged is beloved in Rahamida almost as much "
                                          "as its rival Mim is hated. This waystone marks the unfolding world as it "
                                          "once was, "
                                          "and in doing so it connects you to the worshippers of the Principle of the "
                                          "World. "
                                          "Revealed to you, the best practitioner of Ged in the exploration party, "
                                          "are two sites; a long lost temple, and a mountain that will rise above the "
                                          "land. "
                                          "Of course, you could take the opportunity to seek Ged's gifts upon the "
                                          "party instead, offering relics up to the Principle. "

                              )
        return embed
