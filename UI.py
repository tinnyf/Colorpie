import discord



class UI():

    def embed(title, description, fields: dict, color):
        embed = discord.Embed(title = title, description = description, color = discord.Colour.from_str(color))
        for title, value in fields.items():
            embed.add_field(name = title, value = value)
        return embed
