

class Dilemma():

    def __init__(self, player_handler, player_id):
        self.player_handler = player_handler
        self.player_id = player_id
        self.embed = None
        self.view = None

    async def send(self, interaction):
        member = interaction.guild.get_member(self.player_handler.get_discord_reference(self.player_id))
        await member.send(view = self.view, embed = self.embed)