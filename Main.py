import discord
import json
import asyncio
import random
import os
import cp_converters
from cp_converters import SmartMember
from discord.ext.commands import Bot, Context
from discord.ext import commands, tasks
import datetime
from datetime import datetime, time, date
import emojis
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=['~','-'], intents=intents)
council_channels = ['816153720651251722']
admin_users = [679680827831222310, 129628193811464193, 842106129734696992, ]
voter_roles = [776142371918184479, 776142246008455188]


@bot.event
async def on_reaction_remove(reaction, user):
    print (f"Reaction removed by {user.name}")


@bot.command(aliases=['tempmute'])
@commands.has_permissions(manage_messages=True)
async def mute(ctx, member: SmartMember, time=None, *, reason=None):
    if not member:
        await ctx.send("You must mention a member to mute!")
    elif not time:
        await ctx.send("You must give a time!")
    else:
        if not reason:
           reason="No reason given"
    #Now timed mute manipulation
        try:
            seconds = int(time[:-1]) #Gets the numbers from the time argument, start to -1
            duration = time[-1] #Gets the timed maniulation, s, m, h, d
            if duration == "s":
                seconds = seconds * 1
            elif duration == "m":
                seconds = seconds * 60
            elif duration == "h":
                seconds = seconds * 60 * 60
            elif duration == "d":
                seconds = seconds * 86400
            else:
                await ctx.send("Invalid duration input")
                return
        except Exception as e:
            print(e)
            await ctx.send("Invalid time input")
            return
        guild = ctx.guild
        Muted = guild.get_role(712159294023270450)
        await member.add_roles(Muted, reason=reason)
        muted_embed = discord.Embed(title="Muted a user", description=f"{member.mention} Was muted by {ctx.author.mention} for {reason} to {time}")
        await ctx.send(embed=muted_embed)
        print (seconds)
        await asyncio.sleep(seconds)
        await member.remove_roles(Muted)
        unmute_embed = discord.Embed(title="Mute over!", description=f"{ctx.author.mention} muted to {member.mention} for {reason} is over after {time}")
        await ctx.send(embed=unmute_embed)






# import Updater 
# from Updater import db_updates
# import General
# from General import db_general
import Council
from Council import cp_council
import NewCouncil
from NewCouncil import cp_NewCouncil
import Events
from Events import cp_events
# #Ver = 1.1
# 
# bot.add_cog(db_updates(bot))
bot.add_cog(cp_council(bot))
bot.add_cog(cp_events(bot))
bot.add_cog(cp_NewCouncil(bot))
bot.run('ODQwNjAxNTQ0NDk5MTM0NDg2.YJalMQ.btX1L8Y3a7Xx9FlJ-teZPXhyZc8')
