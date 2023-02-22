import discord
import traceback

class ColorButton(discord.ui.Button):

    def __init__(self, name, emoji, channel, role, member_id):
        self.channel = channel
        self.role = role
        self.member_id = member_id
        super().__init__(emoji = emoji, label = name)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id == self.member_id:
            try:
                print("Recieved callback for colorbutton")
                if isinstance(self.role, int):
                   self.role = interaction.guild.get_role(self.role)
                await interaction.user.add_roles(self.role)
                if isinstance(self.channel, int):
                    self.channel = interaction.guild.get_channel(self.channel)
                await self.channel.send(f"@Welcomer please welcome {interaction.user.name} to your number!")
                await interaction.response.send_message(f"Please go to {self.channel.mention} to meet some like-minded people!", ephemeral = True)
                self.view.stop()
            except Exception as e:
                print(traceback.format_exc())
        else:
           await interaction.response.send_message("Stop messing around with other people's joining process >:(")

