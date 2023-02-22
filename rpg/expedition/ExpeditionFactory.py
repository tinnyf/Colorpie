import random
import traceback

import discord

from rpg.expedition.Pages.Page import Page
from rpg.expedition.Pages.EndPage import EndPage
from rpg.expeditions.expedition import Expedition
from rpg.expedition.buttons.LootButton import LootButton
from rpg.expedition.buttons.PageButton import PageButton
from rpg.expeditions.into_rahamida import Rahamida
from rpg.expeditions.tian_bay import TianBay


class ExpeditionFactory():

    def __init__(self, player_handler):
        self.player_handler = player_handler
        self.expeditions = [
            TianBay,
            Rahamida
        ]

    def get_expedition(self, expedition=None):
        print("hello!")
        try:
            if expedition is None:
                expedition = random.choice(self.expeditions)
            expedition = expedition(self.player_handler)
            return expedition
        except Exception:
            print(traceback.format_exc())