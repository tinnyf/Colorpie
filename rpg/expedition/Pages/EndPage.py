from rpg.expedition.Pages.Page import Page
import math


class EndPage(Page):

    async def loot(self, expedition, interaction):
        print("Loot init")
        print(expedition.players)
        for player_id in expedition.players:
            print(player_id)
            relics = math.floor(self.expedition.rewards["relics"] / len(expedition.players))
            self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + relics)
        await interaction.response.send_message(f"Each player got {relics} relics!")
