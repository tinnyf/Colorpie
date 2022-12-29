import discord


class DailyButtons:
    def __init__(self, player_handler):
        self.player_handler = player_handler

    def devotion_button(self, player_id, rune, cost,  message):
        devotion_button = discord.ui.Button(style = discord.ButtonStyle.primary, label = f"Devote to {rune} ({cost} Relics)" )

        async def callback(interaction:discord.Interaction):
            self.player_handler.set_devoted(player_id, rune)
            self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - cost)
            await interaction.response.send_message(message)
            devotion_button.view.stop()

        devotion_button.callback = callback
        return devotion_button

    def reject_button(self, message):
        button = discord.ui.Button(style = discord.ButtonStyle.primary, label = f"Turn your back on the stars")

        async def callback(interaction: discord.Interaction):
            await interaction.response.send_message(message)
            button.view.stop()

        button.callback = callback
        return button

    def defy_button(self, player_id, defy_rune, with_rune, message):
        button = discord.ui.Button(style = discord.ButtonStyle.primary, label = f"Defy {defy_rune} with {with_rune}.")

        async def callback(interaction: discord.Interaction):
            self.player_handler.add_status(player_id, f"Defies {defy_rune}")
            self.player_handler.increase_rune(player_id, defy_rune, 0 - self.player_handler.get_rune_scores(player_id)[defy_rune])
            await interaction.response.send_message(message)
            button.view.stop()

        button.callback = callback
        return button

    def status_button(self, player_id, status, message, label, extra = None, style = discord.ButtonStyle.primary):
        button = discord.ui.Button(style = style, label = label)

        async def callback(interaction: discord.Interaction):
            self.player_handler.add_status(player_id, status)
            await interaction.response.send_message(message)
            extra()
            button.view.stop()

        button.callback = callback
        return button

    def item_button(self,player_id, item, message, label, extra = None):
        button = discord.ui.Button(style = discord.ButtonStyle.primary, label = label)

        async def callback(interaction: discord.Interaction):
            self.player_handler.add_item(player_id, item)
            await interaction.response.send_message(message)
            if extra:
                extra()
            button.view.stop()

        button.callback = callback
        return button

    def relics_button(self, player_id, relics, message, label, extra = None):
        button = discord.ui.Button(style = discord.ButtonStyle.primary, label = label)

        async def callback(interaction: discord.Interaction):
            self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + relics)
            await interaction.response.send_message(message)
            if extra:
                extra()
            button.view.stop()


        button.callback = callback
        return button
