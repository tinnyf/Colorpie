import discord


class LootButton(discord.ui.Button):  # Only for end pages
    def __init__(self, expedition, label, page, style):
        self.expedition = expedition
        self.page = page  # refers to own page
        super().__init__(label=label, style=discord.ButtonStyle.green)

    async def callback(self, interaction):
        print("Hello from loot callback!")
        print(self.expedition.pages)
        print(self.page)
        print(self.expedition.pages[self.page])
        await self.expedition.pages[self.page].loot(self.expedition, interaction)

