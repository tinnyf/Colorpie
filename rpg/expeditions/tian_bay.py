import discord

from rpg.expedition.Pages.EndPage import EndPage
from rpg.expedition.Pages.Page import Page
from rpg.expedition.buttons.LootButton import LootButton
from rpg.expedition.buttons.PageButton import PageButton
from rpg.expeditions.expedition import Expedition



class TianBay(Expedition):
    def __init__(self, player_handler):
        self.pages = [
                        (
                            Page(player_handler,
                                 "Your boat enters the water with a splash, and a rush of cold water. You've chartered this vessel for a cost; you'll need to earn it back. Be that as it may, Tian Bay is ready for you; the waves churn, and the depths hold countless secrets.",
                                 {"Head out into the bay": (PageButton, 1, discord.ButtonStyle.primary),
                                  "Approach the Capital": (PageButton, 2, discord.ButtonStyle.primary),
                                  "Trade along the Coast": (PageButton, 3, discord.ButtonStyle.primary)}, '#0A2647',
                                 rewards={"relics": -100}, step_cost=0
                                 )
                        ),
                        (
                            Page(player_handler,
                                 "The waters are calmer out here, but the rains pelt you and your supplies are dwindling. Nearby, a boat is broken upon a sandbar, but further away, you can see something tower below the waves.",
                                 {"Explore the wreck": (PageButton, 4, discord.ButtonStyle.primary),
                                  "Head to the towering shape": (PageButton, 5, discord.ButtonStyle.primary)}, '#144272',
                                 rewards={"relics": 0},
                                 )

                        ),
                        (
                            Page(player_handler,
                                 "The capital looms ahead. Entering it will not be an easy task, but you are going to risk it. Unless you wish to turn away?",
                                 {"Try to dock at the capital": (PageButton, 6, discord.ButtonStyle.primary),
                                  "Head out into the bay": (PageButton, 1, discord.ButtonStyle.primary),
                                  "Trade along the Coast": (PageButton, 3, discord.ButtonStyle.primary)}, '#205295',
                                 rewards={"relics": 0},
                                 )

                        ),
                        (
                            Page(player_handler,
                                 "Trading along the coast is boring and arduous, and does not pay well. Still, it is safe and reliable.",
                                 {"Do a day's work": (PageButton, 3, discord.ButtonStyle.primary),
                                  "Return the boat": (PageButton, 7, discord.ButtonStyle.primary)}, "#82C3EC",
                                 rewards={"relics": 10},
                                 )

                        ),
                        (
                        EndPage(player_handler,
                                "Inside the wreck is a chest. You take it, and haul it onto your ship. Since a storm is coming, you head back to shore.",
                                rewards={"relics": 130},
                                buttons={"Split the Loot": (LootButton, 4, discord.ButtonStyle.success)}

                                )

                    ),
                        (
                            Page(player_handler,
                                 "Beneath the water is a spire. How it got here, how it still stands, you don't know. Someone dives in, swims through a window, and hauls a waterlogged runeshield onto the boat. They tell you about a door further down, but a crash of thunder resounds in the distance. ",
                                 rewards={"relics": 70},
                                 buttons={"Break down the Door": (PageButton, 8, discord.ButtonStyle.primary),
                                          "Return to shore": (PageButton, 7, discord.ButtonStyle.primary)}, step_cost=3
                                 )

                        ),
                        (
                            Page(player_handler,
                                 "As you attempt to push into the capital's old docks, you find Seekers. They were already wounded, and you're able to take them down, but not without major injury. They have a few minor wonders upon them. ",
                                 rewards={"relics": 70},
                                 buttons={"Explore the docks again.": (PageButton, 6, discord.ButtonStyle.primary),
                                          "Return the boat": (PageButton, 7, discord.ButtonStyle.primary)}, step_cost=5,
                                 fail_text="You try to explore the docks, but the Seekers catch you unawares. Your crew is slaughtered, and you are slain.")
                        ),
                        (
                            EndPage(player_handler,
                                    "You return to the harbour, and hand over the ship.",
                                    buttons={"Split the Loot": (LootButton, 4, discord.ButtonStyle.success)}
                                    )

                        ),
                        (

                            Page(player_handler,
                                 "You throw yourself into the freezing water, and sink, holding your breath. It is hard to maneuver, but the door is rotten and you rip it open. Inside is an intact haul of relics. There's a passage that leads deeper, but the storm is closing in.",
                                 rewards={"relics": 180},
                                 buttons={"Explore the passage": (PageButton, 9, discord.ButtonStyle.primary),
                                          "Return to shore": (PageButton, 10, discord.ButtonStyle.primary)}  # 8
                                 )

                        ),
                        (
                            Page(player_handler,
                                 "The passage leads to an intact armory, with a sealed vault within. You take an ancient weapon that you don't understand, but know can sell. The storm is upon on you, and the journey home will not be easy. Still, the vault calls to you. Just one more trip?",
                                 rewards={"relics": 500},
                                 buttons={"Crack the vault": (PageButton, 11, discord.ButtonStyle.primary),
                                          "Flee to shore": (PageButton, 12, discord.ButtonStyle.primary)}
                                 )

                        ),
                        (
                            EndPage(player_handler,
                                    "Through howling winds and the strength of Kviz, you travel. At last you dock at the trading village, your booty in tow.",
                                    step_cost=3, buttons={"Split the Loot": (LootButton, 4, discord.ButtonStyle.success)},
                                    fail_text="You and your treasure are lost at sea. Water fills your lungs, and everything goes dark."
                                    )
                        ),
                        (
                            Page(player_handler,
                                 "You break the vault open, and grab several bulky, ancient, treasures, burning with power. When you return to the ship, exhausted and soaking wet, he storm rages around you, and your treasure is slowing you down. What do you do?",
                                 rewards={"relics": 10000},
                                 buttons={"Ditch your bounty (-8000 relics)": (PageButton, 13, discord.ButtonStyle.primary),
                                          "Do not yield a relic": (PageButton, 14, discord.ButtonStyle.primary)},
                                 step_cost=2  # 11

                                 )

                        ),
                        (
                            EndPage(player_handler,
                                    "The storm batters and buffets you, threatening to hurl you into the roiling water. The sun burns behind a cloud, a red drop in a churning black storm. When you finally arrive home, it is agonised and broken.",
                                    buttons={"Split the Loot": (LootButton, 4, discord.ButtonStyle.success)},
                                    fail_text="You and your treasure are lost at sea. Water fills your lungs, and everything goes dark.",
                                    step_cost=8

                                    )

                        ),
                        (
                            EndPage(player_handler,
                                    "You lighten your load, the treasures sinking into the churning ocean. Perhaps you can come back later, but you doubt it. The crew will talk. All that is to do now is live. The storm nearly tears the boat in half, but you make it back. Exhausted, broken, but safe.",
                                    buttons={"Split the Loot": (LootButton, 4, discord.ButtonStyle.success)},
                                    fail_text="You and your treasure are lost at sea. Water fills your lungs, and everything goes dark.",
                                    step_cost=9, rewards={"relics": -8000}

                                    )
                        ),
                        (
                            EndPage(player_handler,
                                    "You brave the storm, and despite everything, you live. The sea is black and red with blood that churns in a ceaseless gyre, but none of it will compare to the wealth that will greet you ashore",
                                    buttons={"Split the Loot": (LootButton, 4, discord.ButtonStyle.success)},
                                    fail_text = "Your boat is weighed down and sluggish, and the storm devours you. You, your treasure, and your hubris are smashed into the rocks, pulled under,and lost forever.",
                                    step_cost = 50)
                        )


     ]
        super().__init__("Braving the waves", self.pages)
        self.title = "Braving the waves"