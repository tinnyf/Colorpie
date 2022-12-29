
class Expedition:
    def __init__(self, title, pages, host, players):
        print("Begin expedition init")
        self.pages = pages #dict
        self.defeated = []
        self.title = title
        self.host = host
        self.players = players
        self.players.insert(0, host)
        self.active_page = None
        self.rewards = {"relics": 0, "items": []}
        print("End expedition init")

    async def run(self, interaction):
        print("Hello from expedition.run!")
        await self.use_page(0, interaction)

    async def use_page(self, page_index, interaction):
        print("Hello from use_page!")
        embed, view = self.pages[page_index].run(self)
        print(embed,view)
        await interaction.response.edit_message(embed=embed, view=view)
        self.active_page = self.pages[page_index]

    def knockout(self, player):
        self.defeated.append(player)
        self.players.remove(player)