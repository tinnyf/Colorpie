import discord
import discord.ext
from discord.ext import commands, tasks
import json
import typing
import asyncio
import datetime
from datetime import date, time, datetime
from discord.ext.commands import bot

#Faction[Title][Permission]
#Faction[Users][Title]
#FactionMember.has_permission == User.has_title + Title.has_permission

#CpUser - invites stored somewhere.

class CpUser:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def get_faction(self, source, member): #Source should always be the same, but I'm worried about calling for factiondict in here since it doesn't exist... is that stupid?
        for faction in source:
            if member.id in source[faction]["members"]:
                return faction
        return None ## not sure what to do about it returning string or bool. Is that an issue?

    def has_permission(source, member, permission):
        try:
            faction = FactionMember.get_faction(source, member)
            return source[faction]["members"][member.id]["Permissions"][permission]
        except KeyError:
            return False
