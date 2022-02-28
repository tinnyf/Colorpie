import discord
import discord.ext
from discord.ext import commands, tasks
import typing
import asyncio
from discord.ext.commands import bot
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from FactionHandler import FactionHandler

class CommandHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def found(self, ctx, name):
        await ctx.send(FactionHandler.found(ctx, name))
