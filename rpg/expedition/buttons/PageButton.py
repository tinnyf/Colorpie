import discord


class PageButton(discord.ui.Button):
    def __init__(self, expedition, label, page, style):
        self.page = page
        self.expedition = expedition
        super().__init__(label = label, style = style)

    async def callback(self, interaction:discord.Interaction):
        await self.expedition.use_page(self.page, interaction)
