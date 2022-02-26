import discord
import discord.ext
from discord.ext import commands, tasks
import random
import json
import typing
import asyncio
import cp_converters
from cp_converters import SmartMember
import datetime
from datetime import date, time, datetime 
from discord.ext.commands import bot

                                        
class cp_NewCouncil(commands.Cog):
     def __init__(self,bot):
        self.bot = bot
