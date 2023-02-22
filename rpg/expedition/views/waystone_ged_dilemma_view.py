import discord


class WaystoneGedDilemmaView(discord.ui.View):

    def __init__(self, interaction, expedition, player_handler):
        self.original_interaction = interaction
        self.expedition = expedition

    @discord.ui.button(label = "Go to the mountaintop")
    async def mountain(self):
        self.expedition.use_page(4, self.original_interaction)
        interaction.response.send_message("You've made your choice; the expedition will journey upwards to the ")

    @discord.ui.button(label = "Go to the temple")
    async def temple(self):
        self.expedition.use_page(3, self.original_interaction)

    @discord.ui.button(label = "Attune with Ged")
    async def Ged(self):
        self.original_interaction.response.send_message("The Ged practitioner smiles at you, and politely explains they've used all your gathered relics to temporarily make you attuned to Ged. You're not sure you appreciate that.")
        for player_id in self.expedition:
            if "Attuned to Ged" not in self.player_handler.get_status:
                self.player_handler.add_status(player_id, "Attuned to Ged")

