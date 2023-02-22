import discord

from rpg.expedition.Pages.EndPage import EndPage
from rpg.expedition.Pages.Page import Page
from rpg.expedition.buttons.LootButton import LootButton


class Waystone(EndPage):

    def __init__(self, player_handler, expedition = None):
        super().__init__(
            player_handler,
            "Watching over hills that surrender to the jungle is a waystone. Upon it has been carved an intricate set of markings, landmark buried by time inscribed upon the outlines unfamiliar landscape. You can find little, but a few relics are buried near the stone.",
            expedition,
            rewards = {"relics": 20},
            buttons = {"Split the Loot": (LootButton, 2, discord.ButtonStyle.primary)})

    def main(self):
        player_id, stat = self.get_best_player("Ged")
        if stat > 25:
            self.buttons_assembled.append(WaystoneGed(self.player_handler, player_id))
        return self.embed()




