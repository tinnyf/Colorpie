import discord
from Expeditions import Expedition, Page
from ExpeditionButtons import PageButton



class ExpeditionFactory():

    def __init__(self):
        self.expeditions = {

        "Into Rahamida" : [
            ("In search of relics, you've passed from the former land of the Kohgang. Here, at the furthest reach of the country, you see the mountains and jungles of another country spreading into the distance.",
            {PageButton: ("Explore the jungles for treasure",1, discord.ButtonStyle.primary), PageButton: ("Press deeper into Rahamida", 2, discord.ButtonStyle.primary), '#80F7D4'),
            ("The jungles are dense, and the trek through them is hard. Disoriented, you nonetheless come across an overgrown tomb, vines creeping up its flank.",
            {PageButton: ("Press on into Rahamida", 2, discord.ButtonStyle.primary), PageButton: ("Explore the tomb", 3, discord.ButtonStyle.primary), '#313628''},
            ("At the top of a hill, you come to a waystone. Upon the bald boulder has been carved an intricate set of markings - landmarks buried by time upon an unfamiliar landscape. You travel to them each, gathering relics, but at this time you can go no further."),
            ("In the depths of the tomb, you come to a sarcophagus. ")


            )
               ),
            (""   ),
            (""   ),
            (""   ),



            ]


        }

    def get_expedition(self):
        expedition = random
        return Expendition()

















        ]
