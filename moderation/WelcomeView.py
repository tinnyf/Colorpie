import discord
from discord import app_commands
from discord.ext import commands
from moderation.Color import Color
from moderation.ColorButton import ColorButton

class WelcomeView(discord.ui.View):

    def __init__(self, member, bot, colors):
        self.member_id = member.id
        self.guild = member.guild
        self.bot = bot
        self.colors = colors
        super().__init__()
        for color, instance in colors.items():
           self.add_item(ColorButton(color, instance.emoji, instance.channel, instance.role, self.member_id))





