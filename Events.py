import discord
import discord.ext
from discord.ext import commands, tasks
import json
import typing
import asyncio
import datetime
from datetime import date, time, datetime 
from discord.ext.commands import bot 
# -*- coding: utf-8 -*-

class cp_events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
##        self.eventchecker.start()
        self.arrivals.start()
        with open ('src/data/events.json') as json_file_r0:
            try:
                self.eventlist = json.load(json_file_r0)
            except json.decoder.JSONDecodeError:
                self.eventlist = {}
                
    async def element(self, ctx, bot, component): #This whole function should handle input data
        def edit_response(message): 
            return message.author == ctx.author and message.channel == ctx.channel
        try:
            response = await self.bot.wait_for('message', check =edit_response, timeout = 120.0)
        except asyncio.TimeoutError:
            await ctx.send('Response timed out')
            await component.delete(delay=1)
        else:
            if response.content.lower()== "cancel":
                await ctx.send('Command canceled')
                await component.delete()
            else:
                return (response.content)
            
    def save_json_dict(self, dict):
        with open("src/data/events.json", "w") as json_file:
            json.dump(dict, json_file)


    @tasks.loop(seconds=30)
    async def arrivals(self):
        guild = self.bot.get_guild(695401740761301056)
        channel = self.bot.get_channel(946549398417080370)
        await self.bot.wait_until_ready()
        embed = discord.Embed(title= "All events!")
        dt = datetime.now().strftime('%A, %d. %B %Y at %M past %I%p UTC')
        embed.set_footer(text = "Last updated at %r" %dt)
        embed.set_image(url = "https://cff2.earth.com/uploads/2022/01/17122033/Predatory-dinosaurs-scaled.jpg")
        white = discord.utils.get(guild.emojis, name = "5wm")
        blue = discord.utils.get(guild.emojis, name = "5um")
        black = discord.utils.get(guild.emojis, name = "5bm")
        red = discord.utils.get(guild.emojis, name = "5rm")
        green = discord.utils.get(guild.emojis, name = "5gm")
        embed.add_field(name = f"______________________________", inline = False, value = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}")
        for event in self.eventlist:
            PlayerNeat = []
            for player in self.eventlist[event]["Players"]:
                player = guild.get_member(player)
                player= player.name
                PlayerNeat.append(player)
            PlayerNeat = " ".join(PlayerNeat)
            TimeDelta = (datetime.strptime(self.eventlist[event]['Date'], "%d %b %y %H:%M:%S")) - datetime.now()
            text = f"Start time: {self.eventlist[event]['Date']}. \n **List of players: {(PlayerNeat)}**. \n Starts in: {TimeDelta}"
            embed.add_field(name = event, value = text, inline = False)
        try:
            message = await channel.fetch_message(channel.last_message_id)
            await message.edit(embed=embed)
        except discord.errors.HTTPException:
            message = await channel.send(embed=embed)


    @arrivals.before_loop
    async def before_arrivals(self):
        await self.bot.wait_until_ready()

    @commands.group()
    async def event(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No such command found! Please use 'event add' to add a event, or 'event list' to see current ones ")

    @event.command(aliases = ["c", "a", "create"])
    async def add (self,ctx):
        embed = discord.Embed(title = "event details")
        embed.set_footer(text = "Type cancel to cancel")
        member = ctx.author
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name = "event name", value = "Please write a name for your event below")
        UI = await ctx.send(embed=embed)
        name = await self.element(ctx, bot, UI)
        embed.set_field_at(0, name = "event name", value = name)
        dt = datetime.now() 
        dt = dt.strftime("%d %b %y %H:%M:%S")
        embed.add_field(name = "Time", value = "Please add a date and time in the format 'date month year H:M:S'. For example, for now, write %s. Please note that times should be UTC. Should be." %(dt))
        await UI.edit(embed=embed)
        while True:
            try:
                time = await self.element(ctx, bot, UI)
                if not time:
                    print("Test")
                    return False
                time = datetime.strptime(time, "%d %b %y %H:%M:%S")
                break
            except ValueError:
                await ctx.send("Please check your format and try again below!")
            if time == "cancel":
                break
        timeformat = time.strftime ("%A, %d %B %Y at %M past %I%p UTC")
        embed.set_field_at(1, name = "Time", value = timeformat)
        embed.add_field(name = "Host", value = ctx.author.display_name)
        await UI.edit(embed=embed)
        await UI.add_reaction('✔')
        await UI.add_reaction('❌')
        embed.set_footer(text = "Confirm event creation?")
        n=1
        while n != 2 : 
            try:
                reaction, user = await self.bot.wait_for('reaction_add',timeout = 60)
            except asyncio.TimeoutError:
                await ctx.send('Timed out!')
                UI.delete(delay = 1)
                return False
            else:
                message = reaction.message
            for k in reaction.message.reactions:
                if k.count == 2:
                    if (str(k.emoji)) == "✔":
                        assembled = {name: { "Host":ctx.author.id, "Date":time.strftime("%d %b %y %H:%M:%S"), "Players":[ctx.author.id]}}
                        self.eventlist[name] = {"Host":ctx.author.id, "Date":time.strftime("%d %b %y %H:%M:%S"), "Players":[ctx.author.id]}
                        self.save_json_dict(self.eventlist)
                        await ctx.send("Event added!")
                        await reaction.message.delete(delay = 3)
                        return True 
                    elif str(k.emoji) == '❌':
                        await ctx.send ("Event deleted!")
                        await reaction.message.delete(delay = 2)
                        return False
                    
    @event.command(aliases = ["l, see, s, view"])
    async def list (self, ctx): 
        if len(self.eventlist) == 0:
            return
        n=0
        guild = ctx.guild
        while True:
            active = list(self.eventlist.keys())
            active = (active[n])
            host = guild.get_member(self.eventlist[active]["Host"])
            embed = discord.Embed(title = active, colour = host.colour)
            embed.set_footer(text = "event %r of %r. Tick to join, Cross to close the UI. Use arrows to scroll." %(n+1, len(self.eventlist)))
            embed.set_thumbnail(url=host.avatar_url)
            embed.add_field(name = "Time", value = self.eventlist[active]["Date"])
            embed.add_field(name = "Host", value = host.name)
            temp = []
            for y in self.eventlist[active]["Players"]:
               p = guild.get_member(y).name
               temp.append(p)
            embed.add_field(name = "Players", value = temp)
            try:
                await UI.edit(embed=embed)
            except UnboundLocalError:
                UI= await ctx.send(embed=embed)
            await UI.add_reaction('✔')
            await UI.add_reaction('❌')
            await UI.add_reaction('⬅️')
            await UI.add_reaction('➡')
            cl=1
            p = 0
            while cl != 2 : 
                try:
                    reaction, user = await self.bot.wait_for('reaction_add',timeout = 60)
                except asyncio.TimeoutError:
                    if not p == 1:
                        await ctx.send('Timed out!')
                    await UI.delete(delay = 1)
                    return False
                else:
                    message = reaction.message
                for k in message.reactions:
                    if k.count == 2:
                        async for user in reaction.users():
                            if user == ctx.author:
                                print (k)
                                if (str(k.emoji)) == "✔":
                                    self.eventlist[active]["Players"].append(ctx.author.id)
                                    self.save_json_dict(self.eventlist)
                                    await ctx.send("event joined!")
                                    await reaction.message.delete(delay = 3)
                                    return True
                                elif str(k.emoji) == '❌':
                                    await ctx.send ("Command Cancelled!")
                                    await reaction.message.delete(delay = 2)
                                    print ("Call to delete registered")
                                    p = 1
                                    return False
                                elif str(k.emoji) == '⬅️':
                                    if n == 0:
                                        await ctx.send('No more entries in this direction')
                                        await reaction.remove(ctx.author)
                                    else:
                                        n = n-1
                                        cl = 2 
                                        await reaction.remove(ctx.author)
                                        break 
                                elif str(k.emoji) =='➡':
                                    if n + 1 == len(self.eventlist):
                                        await ctx.send('No more entries in this direction')
                                        await reaction.remove(ctx.author)
                                    else:
                                        n = n+1
                                        cl =2
                                        print (n)
                                        await reaction.remove(ctx.author)
                                        break
                                else:
                                    print (k.message)
                            elif user.bot == False:
                                await reaction.remove(user)

    @event.command(aliases = ["del", "d"])
    async def delete(self, ctx, *, name):
        for event in list(self.eventlist.keys()):
            if str(event) == str(name):
                active = self.eventlist[name]
                if ctx.author.id == active["Host"] or ctx.author.top_role.id == 758429516816580618: #As in, if they're an impostor. I should start storing a lot of this in a config somewhere.
                    del self.eventlist[name]
                    self.save_json_dict(self.eventlist)
                    await ctx.send("event deleted!")
                else:
                    await ctx.send("You don't have permission to edit this entry!")






            
##    @tasks.loop(seconds = 300.1)
##    async def eventchecker(self):
##        guild = self.bot.get_guild(758428574905925632)
##        print ("Test")
##        channel = self.bot.get_channel(758429006768373810)
##        await self.bot.wait_until_ready()
##        todelete =[]
##        for event in self.eventlist:
##            print(event)
##            print(self.eventlist[event]["Date"])
##            eventtime = datetime.strptime(self.eventlist[event]["Date"], "%d %b %y %H:%M:%S")#28 Sep 20 20:00:00
##            differential = datetime.now()
##            active = eventtime - differential
##            active = active.total_seconds()
##            players = []
##            for player in self.eventlist[event]["Players"]:
##                players.append((guild.get_member(player).mention))
##                players.append(" and")
##            print (active)
##            if active <= 86250 and active >= 86550:
##                channel.send ("%r starts in about a day! Currently playing are %r" %event, str((*players)))
##            elif active <= 21450 and active >= 21750:
##                channel.send ("%r starts in about six hours! Currently playing is %r" %event, str((*players)))
##            elif active <= 3450 and active >= 3750 :
##                channel.send ("%r starts in about an hour! Currently playing is %r" %event, str((*players)))
##            elif active <= 750 and active >= 450 :
##                channel.send ("%r starts in about ten minutes! Currently playing is %r" %event, str((*players)))
##            elif active <= 150 and active >= -150:
##                channel.send ("%r is starting! Currently playing is %r" %event, str((*players)))
##            elif active <= -3600:
##                todelete.append(event)
##        for event in todelete:
##            del self.eventlist[event]
##            self.save_json_dict(self.eventlist)
##
##        
##
##    
##    @eventchecker.before_loop
##    async def before_eventchecker(self):
##        print('waiting...')
##        await self.bot.wait_until_ready()

  

                    

        
    
##    @commands.check(commands.dm_only())
##    @commands.command(aliases = ["f", "fuzzy"])
##    async def Fuzzy(self, ctx, *, text):
##        print (ctx.author)
##        print (text)
##        guild = self.bot.get_guild(758428574905925632)
##        checkChannel = self.bot.get_channel(758462288008314916)
##        printChannel = self.bot.get_channel(760102374894469151)
##        embed = discord.Embed(title = "Fuzzy")
##        embed.add_field(name = "❤", value = text)
##        UI = await checkChannel.send(embed = embed)
##        await UI.add_reaction('✔')
##        await UI.add_reaction('❌')
##        ctx.send("Message recieved! Please wait for it to appear :D It might take a short while")
##        while True:
##            reaction, user = await self.bot.wait_for('reaction_add')
##            message = reaction.message
##            for k in reaction.message.reactions:
##                print (k)
##                if k.count == 2:
##                    if (str(k.emoji)) == "✔":
##                        SEND = await printChannel.send(embed=embed)
##                        await UI.delete(delay = 3)
##                        checkChannel.send("Confirmed")
##                        return True 
##                    elif str(k.emoji) == '❌':
##                        await checkChannel.send("Deleted!")
##                        await UI.delete(delay = 2)
##                        return False
                                                                                                                              
        
        
        
