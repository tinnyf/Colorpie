import random

import discord


class Page:
    def __init__(self, player_handler, text, buttons=None, color=str(discord.Colour.random()), rewards={}, image=None,
                 before_run=None, output=None, expedition=None, step_cost=1):
        print("Hello from page!")
        self.player_handler = player_handler
        self.expedition = expedition
        self.step_cost = step_cost
        print(f"Length of buttons: {buttons}")
        self.buttons = buttons
        self.buttons_assembled = None
        self.text = text
        self.image = image
        self.color = discord.Colour.from_str(color)
        self.before_run = before_run
        self.output = output
        self.rewards = rewards

    def run(self, expedition):
        print("Hello from run!")
        self.expedition = expedition
        self.buttons_assembled = self.choose_buttons(self.buttons)
        for reward, amount in self.rewards.items():
            self.expedition.rewards[reward] += amount  # if int, adds it. If list appends it.

        for _ in range(self.step_cost):
            print("In step_loop")
            print(self.expedition.players)
            player_id = random.choice(self.expedition.players)
            print(player_id)
            self.player_handler.change_hp(player_id, -1)
            if self.player_handler.get_hp(player_id) < 0:
                self.expedition.knockout(player_id)
                if player_id == self.expedition.host:
                    return discord.Embed(title ="The leader has fallen, the expedition is over.", description = self.text), discord.ui.View()
        if self.before_run:
            return self.before_run
        else:
            if self.output:
                self.output()
            else:
                embed = discord.Embed(title=self.expedition.title, description=self.text)
                embed.add_field(name = "Surviving adventurers", value = ", ".join([self.player_handler.get_name(player) for player in self.expedition.players]))
                if self.expedition.defeated:
                    embed.add_field(name = "Defeated adventurers", value = ", ".join([self.player_handler.get_name(player) for player in self.expedition.defeated]))
                embed.set_footer(text=f"Currently {self.expedition.rewards['relics']} relics in pool")
                view = discord.ui.View()
                for button in self.buttons_assembled:
                    view.add_item(button)
                print(embed, view)
                return (embed, view)  # needs to return embed,view

    def choose_buttons(self, buttons):
        try:
            button_instances = []
            print("Preloop")
            for label, args in buttons.items():
                print("Loop init")
                print(label, args)
                buttonclass, *rest = args
                print(buttonclass, rest)
                print(*rest)
                button_instances.append(buttonclass(self.expedition, label, *rest))
                print(button_instances)
                print("Loop-finished")
            return button_instances
        except AttributeError as e:
            print("Attribute Error at line 52")
            print("e")
            return None
