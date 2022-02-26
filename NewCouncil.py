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
   file_locations =  {
      "Factions": 'src/data/faction.json',
   }
  
   def __init__(self,bot):
      self.bot = bot

      def read_json(self, location):
         with open(file_locations[location], "r" ) as json_file_r0:
            try:
               return json.load(json_file_r0)
           except json.decoder.JSONDecodeError:
               return {}

      self.faction_dict = self.read_json("Factions") 

   def save_json_dict(self, dict, location):
      with open(file_locations[location], 'w') as json_file:
         json.dump(dict,json_file)


@commands.command()
async def found(self, ctx, name):
   self.faction_dict[name] = {}
   self.save_json_dict(self.faction_dict, "Factions") #Is it worth binding faction_dict with the key "Factions" somewhere?
   ctx.send("Created a new faction with name: {name}")

@commands.command(aliases = ["ping"])
async def pong(self, ctx):
   ctx.send(ctx.invoked_with)