import discord

from rpg.expedition.Pages.EndPage import EndPage
from rpg.expedition.Pages.Page import Page
from rpg.expedition.buttons.LootButton import LootButton
from rpg.expedition.buttons.PageButton import PageButton
from rpg.expeditions.expedition import Expedition


class Rahamida(Expedition):

    def __init__(self, player_handler):
        self.pages = [

                Page(player_handler,
                     "In search of relics, you've passed from the former land of the Kohgang. Here, at the furthest reach of the country, you see the mountains and jungles of another country spreading into the distance.",
                     {"Explore the jungles for treasure": (PageButton, 1, discord.ButtonStyle.primary),
                      "Press deeper into Rahamida": (PageButton, 2, discord.ButtonStyle.primary)}, '#80F7D4',
                     rewards={"relics": 10})
            ,

                Page(player_handler,
                     "The jungles are dense, and the trek through them is hard. Disoriented, you nonetheless come across an overgrown tomb, vines creeping up its flank.",
                     {"Press on into Rahamida": (PageButton, 2, discord.ButtonStyle.primary),
                      "Explore the tomb": (PageButton, 3, discord.ButtonStyle.primary)}, '#313628',
                     rewards={"relics": 10})
            ,

                EndPage(player_handler,
                        "At the top of a hill, you come to a waystone. Upon the bald boulder has been carved an intricate set of markings - landmarks buried by time upon an unfamiliar landscape. You travel to them each, gathering relics, but at this time you can go no further.",
                        rewards={"relics": 20},
                        buttons={"Split the Loot": (LootButton, 2, discord.ButtonStyle.primary)}
                        )
            ,

                EndPage(player_handler,
                        "In the depths of the tomb, you come to a sarcophagus. Climbing inside, you seal the lid above you. Power seeps inside of you, your body breaking, only held together by a lost, unknown, power.",
                        rewards={"relics": 60},
                        buttons={"Split the Loot": (LootButton, 3, discord.ButtonStyle.primary)}, step_cost=5
                        )
            ,
        ]
        super().__init__(title = "Into Rahamida", pages = self.pages)
        self.title = "Into Rahamida"