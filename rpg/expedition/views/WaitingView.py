import traceback

import discord

from rpg.expeditions.expedition import Expedition


class WaitingView(discord.ui.View):
    def __init__(self, interaction, expedition, embed, player_handler, players = []):
        self.original_interaction = interaction
        self.player_handler = player_handler
        self.host = player_handler.get_player_id(interaction.user)
        self.players = players
        self.expedition = expedition
        self.embed = embed
        super().__init__()

    @discord.ui.button(label="Start the Expedition")
    async def start_button(self, interaction: discord.Interaction, button):
        try:
            self.expedition.set_up_players(self.players, self.host)
            await self.expedition.run(interaction)
        except Exception:
            print(traceback.format_exc())
    @discord.ui.button(label="Join the Expedition")
    async def join_button(self, interaction: discord.Interaction, button):
        print(self.player_handler.get_player_id(interaction.user))
        if not self.player_handler.get_player_id(interaction.user) in self.players \
                and not self.player_handler.get_player_id(interaction.user) == self.host:
            self.players.append(self.player_handler.get_player_id(interaction.user))
            print(self.players)
            self.embed.set_field_at(0, name="Players",
                                    value="\n".join(list(self.player_handler.get_name(player) for player in self.players)))
            print("before_edit")
            await interaction.response.edit_message(embed=self.embed,
                                                    view=self)
        else:
            await interaction.response.send_message("You're already in this expedition!", ephemeral=True)

    @discord.ui.button(label="Cancel the Expedition")
    async def cancel_button(self, interaction: discord.Interaction, button):
        print("Cancel_button")
        print(interaction.message)
        try:
            await interaction.message.delete()
            await interaction.response.send_message("Cancelled the expedition!")
        except Exception as e:
            print(e)