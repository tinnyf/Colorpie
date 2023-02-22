import discord
import math
import traceback

class UserSelector(discord.ui.UserSelect):

    def __init__(self, rune, player, player_handler):
        self.rune = rune
        self.callback_check = {
            "Dorn": self.dorn_callback,
            "Set": self.set_callback,
            "Sul": self.sul_callback
        }
        self.player = player
        self.player_handler = player_handler
        super().__init__()

    async def callback(self, interaction):
        try:
            if self.player == interaction.user:
                target = self.values[0]
                player = self.player_handler.get_player(self.player_handler.get_player_id(self.player))
                target = self.player_handler.get_player(self.player_handler.get_player_id(target))
                if player.get_rune_scores()[self.rune] < 5:
                    await interaction.response.send_message("Your power is depleted and nothing will come of your attempts")
                    return False
                await interaction.response.send_message(await self.callback_check[self.rune](player, target))
        except Exception:
            print(traceback.format_exc())

    async def dorn_callback(self, player, target):
        amount = math.floor(player.get_rune_scores()["Dorn"] / 2)
        target.change_hp(amount)
        player.change_hp(0 - math.floor(amount / 2))
        player.increase_rune("Dorn", -1)
        return (
            f"You just restored {amount} hp to {self.values[0].name}, but lost some health yourself as Dorn's cycle rolls onward within you.")

    async def set_callback(self, player, target):
        if target != player:
            return (f"Set's power will only work inward.")
        else:
            amount = math.floor(player.get_rune_scores()["Set"] / 3)
            player.change_hp(amount)
            player.increase_rune("Set", -1)
            return (f"Reaching within, you restore {amount} hp to yourself, burning Set's favour for vitality.")

    async def sul_callback(self, player, target):
        if target != player:
            amount = math.floor(player.get_rune_scores()["Dorn"] / 4)
            player.change_hp(amount)
            target.change_hp(amount)
            player.increase_rune("Sul", -1)
            return (
                f"You redouble your bond, restoring both of your determination at the cost of devotion to the runes")
        else:
            return ("Sul cannot bind you to your own ego.")
