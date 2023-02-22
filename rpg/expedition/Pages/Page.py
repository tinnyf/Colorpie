import random

import discord


class Page:
    def __init__(self, player_handler, text, buttons=None, color=str(discord.Colour.random()), rewards={}, image=None,
                 before_run=None, output=None, expedition=None, step_cost=1, fail_text=None):
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
        self.rewards = rewards
        if fail_text is None:
            self.fail_text = self.text
        else:
            self.fail_text = fail_text

    def run(self, expedition):
        self.expedition = expedition
        self.run_buttons()
        self.main()
        return self.end()

    def run_buttons(self):
        self.buttons_assembled = self.choose_buttons(self.buttons)
        for reward, amount in self.rewards.items():
            self.expedition.rewards[reward] += amount  # if int, adds it. If list appends it.


    def end(self):
        self.before_run()
        return_embed = self.damage()
        return return_embed

    def main(self):
        return self.embed()



    def damage(self):
        for _ in range(self.step_cost):
            print("In step_loop")
            print(self.expedition.players)
            player_id = random.choice(self.expedition.players)
            print(player_id)
            self.player_handler.change_hp(player_id, -1)
            if self.player_handler.get_hp(player_id) < 0:
                try:
                    self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - 100)
                except Exception as E:
                    print(E)
                self.expedition.knockout(player_id)
                if player_id == self.expedition.host:
                    return discord.Embed(title="The leader has fallen, the expedition is over.",
                                         description=self.fail_text), discord.ui.View()
        return self.main()

    def before_run(self):
        pass

    def output(self):
        pass

    def embed(self):
        embed = discord.Embed(title=self.expedition.title, description=self.text)
        embed.add_field(name="Surviving adventurers", value=", ".join([
                                                                          f"{self.player_handler.get_name(player)}, HP:{self.player_handler.get_hp(player)}/{self.player_handler.get_hp_max(player)}"
                                                                          for player in self.expedition.players]))
        if self.expedition.defeated:
            embed.add_field(name="Defeated adventurers", value=", ".join(
                [self.player_handler.get_name(player) for player in self.expedition.defeated]))
        embed.set_footer(text=f"Currently {self.expedition.rewards['relics']} relics in pool")
        view = discord.ui.View()
        for button in self.buttons_assembled:
            view.add_item(button)
        print(embed, view)
        return (embed, view)  # needs to return embed,view


    async def interaction_check(self, interaction):
        return self.player_handler.get_player_id(interaction.author) == self.expedition.host


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


    def get_best_player(self, rune):
        greatest = 0
        for player_id in self.expedition.get_players:
            if self.player_handler.get_rune_scores(player_id)[rune] > greatest:
                active = player_id
                greatest = self.player_handler.get_rune_scores(player_id)[rune]
        if active > threshold:
            return active, greatest

