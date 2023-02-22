from discord import ui


class CharacterModal(ui.Modal, title="Make your character!"):

    def __init__(self, character):
        self.character = character
        self.background = ui.TextInput(label="Add your character's backstory here!")
        self.faction = ui.TextInput(label="Add your character's associated faction here!")
        self.rune = ui.TextInput(label="What rune or principle is yours?")

    async def on_submit(self, interaction):
        self.character.background = self.background
        self.character.faction = self.faction
        self.character.rune = self.rune
        await interaction.response.send_message("Added your character to the bot!", ephemeral=True)
