import discord
class Expedition:

    def __init__(self, pages, title, players):
        self.pages = pages
        self.title = title
        self.players = players

    def run(self, interaction):
        self.use_page(0, interaction)

    def use_page(self, page_index, interaction):
        embed, view = self.pages[index].run(self.players)
        await interaction.response.edit_message(embed = embed, view = view)



class Page:
    def __init__(self, text, expedition, buttons, color = str(discord.Colour.random()), image = None, before_run: function = None, output = None ):
        self.expedition = expedition
        self.buttons = self.choose_buttons(buttons)
        self.text = text
        self.image = image
        self.color = discord.Colour.fromstr(color)
        self.before_run = before_run
        self.output = output

    def run(self, players):
        self.output(players)
        if self.before_run:
            return self.before_run
        else:
            if self.output:
                self.output()
            else:
            return(self.text, self.buttons) #needs to return embed,view


    def choose_buttons(self, buttons):
        return [buttonclass(self.expedition, *args) for buttonclass, args in buttons.items()]:
