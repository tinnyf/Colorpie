import discord
from discord.ext import commands, tasks

class Integrations(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    def view_from_message(self, message):
        return discord.ui.from_message(message)


    class Dropdown(discord.ui.Select):
        def __init__(self, options, placeholder = "Choose an Option...", min = 1, max = 1):
            super().__init__(placeholder = placeholder, min_values = min, max_values = max, options=options)

    class UI_Container(discord.ui.View):
        def __init__(self, *components):
            super().__init__()
            for component in components:
                self.add_item(component)

    def make_option(self, label, description, emoji):
        return discord.SelectOption(label = label, description = description, emoji = emoji)
