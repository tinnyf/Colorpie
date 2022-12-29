import discord


class Channels():
    def __init__(self):
        self.categories = []
        self.server = []
        self.channels_dict = {"rules": (706218507662262362, "Home to the rules of the server, make sure you read them!", {"Link": 706218507662262362}, "#1F0322"),
            "roles": (706218507662262362,"Get your roles here! You can them for colors, gender, pings, and more!", {"Link": 695407854055718942}, "#55104F"),}

    def channel_embed(self, guild, channel):
        print(self.channels_dict[channel])
        for link, *rest in self.channels_dict[channel]:
            link = guild.get_channel(link).mention
            new_tuple = (link, rest)
        return UI.embed(new_tuple)
