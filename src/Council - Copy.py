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

class cp_game(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.gamechecker.start()

        with open ('src/data/Games.json') as json_file_r0:
            try:
                self.gamelist = json.load(json_file_r0)
            except json.decoder.JSONDecodeError:
                self.gamelist = {}
                
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
        with open("src/data/Games.json", "w") as json_file:
            json.dump(dict, json_file)

    @arrivals.before_loop
    async def before_arrivals(self):
        await self.bot.wait_until_ready()


    @tasks.loop(seconds=100)
    async def arrivals(self):
        guild = self.bot.get_guild(695401740761301056)
        channel = self.bot.get_channel(946549398417080370)
        await self.bot.wait_until_ready()
        embed = discord.Embed(title= "All events!")
        dt = datetime.now().strftime('%A, %d. %B %Y at %M past %I%p UTC')
        embed.set_footer(text = "Last updated at %r" %dt)
        embed.set_image(url = "")
        white = discord.utils.get(guild.emojis, name = "5wm")
        blue = discord.utils.get(guild.emojis, name = "5um")
        black = discord.utils.get(guild.emojis, name = "5bm")
        red = discord.utils.get(guild.emojis, name = "5rm")
        green = discord.utils.get(guild.emojis, name = "5gm")
        for game in self.gamelist:
            PlayerNeat = []
            for player in self.gamelist[game]["Players"]:
                player = guild.get_member(player)
                player= player.name
                PlayerNeat.append(player)
            text = f"Start time: {self.gamelist[game]['Date']}, List of players: {(PlayerNeat)}"
            embed.add_field(name = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}", inline = False, value = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}")
            embed.add_field(name = game, value = text, inline = True)
        try:
            message = await channel.fetch_message(channel.last_message_id)
            embed.add_field(name = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}", inline = False, value = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}")
            await message.edit(embed=embed) 
        except discord.NotFound:
            embed.add_field(name = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}", inline = False, value = f"{white}{blue}{black}{red}{green}{white}{blue}{black}{red}{green}")
            message = await channel.send(embed=embed)
            
##    @tasks.loop(seconds = 300.1)
##    async def gamechecker(self):
##        guild = self.bot.get_guild(758428574905925632)
##        print ("Test")
##        channel = self.bot.get_channel(758429006768373810)
##        await self.bot.wait_until_ready()
##        todelete =[]
##        for game in self.gamelist:
##            print(game)
##            print(self.gamelist[game]["Date"])
##            gametime = datetime.strptime(self.gamelist[game]["Date"], "%d %b %y %H:%M:%S")#28 Sep 20 20:00:00
##            differential = datetime.now()
##            active = gametime - differential
##            active = active.total_seconds()
##            players = []
##            for player in self.gamelist[game]["Players"]:
##                players.append((guild.get_member(player).mention))
##                players.append(" and")
##            print (active)
##            if active <= 86250 and active >= 86550:
##                channel.send ("%r starts in about a day! Currently playing are %r" %game, str((*players)))
##            elif active <= 21450 and active >= 21750:
##                channel.send ("%r starts in about six hours! Currently playing is %r" %game, str((*players)))
##            elif active <= 3450 and active >= 3750 :
##                channel.send ("%r starts in about an hour! Currently playing is %r" %game, str((*players)))
##            elif active <= 750 and active >= 450 :
##                channel.send ("%r starts in about ten minutes! Currently playing is %r" %game, str((*players)))
##            elif active <= 150 and active >= -150:
##                channel.send ("%r is starting! Currently playing is %r" %game, str((*players)))
##            elif active <= -3600:
##                todelete.append(game)
##        for game in todelete:
##            del self.gamelist[game]
##            self.save_json_dict(self.gamelist)
##
##        
##
##    
##    @gamechecker.before_loop
##    async def before_gamechecker(self):
##        print('waiting...')
##        await self.bot.wait_until_ready()

    @commands.group()
    async def game(self,ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("No such command found! Please use 'game add' to add a game, or 'game list' to see current ones ")

    @game.command(aliases = ["c", "a", "create"])
    async def add (self,ctx):
        embed = discord.Embed(title = "Game details")
        embed.set_footer(text = "Type cancel to cancel")
        member = ctx.author
        embed.set_thumbnail(url=member.avatar_url)
        embed.add_field(name = "Game name", value = "Please write a name for your game below")
        UI = await ctx.send(embed=embed)
        name = await self.element(ctx, bot, UI)
        embed.set_field_at(0, name = "Game name", value = name)
        dt = datetime.now() 
        dt = dt.strftime("%d %b %y %H:%M:%S")
        embed.add_field(name = "Time", value = "Please add a date and time in the format 'date month year H:M:S'. For example, for now, write %s" %(dt))
        await UI.edit(embed=embed)
        while True:
            while True:
                try:
                   time = await self.element(ctx, bot, UI)
                   if time == "cancel":
                       return False
                   time = datetime.strptime(time, "%d %b %y %H:%M:%S")
                   break
                except ValueError:
                    ctx.send("Please check your format and try again below!")
            if time == "cancel":
                break
            timeformat = time.strftime ("%A, %d. %B %Y at %M past %I%p UTC")
            embed.set_field_at(1, name = "Time", value = "Please type confirm or yes if the time is %a, or anything else if it is not" %timeformat)
            await UI.edit(embed=embed)
            reply = await self.element(ctx, bot, UI)
            if reply.lower() == "yes" or reply.lower() == "confirm":
                break
            elif reply.lower() == "cancel":
                await UI.delete(delay = 1)
                return False
            else:
                await ctx.send("Please try again!")
        embed.set_field_at(1, name = "Time", value = timeformat)
        embed.add_field(name = "Host", value = ctx.author.display_name)
        await UI.edit(embed=embed)
        await UI.add_reaction('✔')
        await UI.add_reaction('❌')
        embed.set_footer(text = "Confirm game creation?")
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
                        self.gamelist[name] = {"Host":ctx.author.id, "Date":time.strftime("%d %b %y %H:%M:%S"), "Players":[ctx.author.id]}
                        self.save_json_dict(self.gamelist)
                        await ctx.send("Game added!")
                        await UI.delete(delay = 3)
                        return True 
                    elif str(k.emoji) == '❌':
                        await ctx.send ("Game deleted!")
                        await UI.delete(delay = 2)
                        return False
                    
    @game.command(aliases = ["l, see, s"])
    async def list (self, ctx): 
        if len(self.gamelist) == 0:
            return
        n=0
        guild = ctx.guild
        while True:
            active = list(self.gamelist.keys())
            print (active)
            active = (active[n])
            print (guild.get_member(self.gamelist[active]["Host"]))
            host = guild.get_member(self.gamelist[active]["Host"])
            embed = discord.Embed(title = active, colour = host.colour)
            embed.set_footer(text = "Game %r of %r. Tick to join, Cross to close the UI. Use arrows to scroll." %(n+1, len(self.gamelist)))
            embed.set_thumbnail(url=host.avatar_url)
            embed.add_field(name = "Time", value = self.gamelist[active]["Date"])
            embed.add_field(name = "Host", value = host.name)
            temp = []
            for y in self.gamelist[active]["Players"]:
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
            while cl != 2 : 
                try:
                    reaction, user = await self.bot.wait_for('reaction_add',timeout = 60)
                except asyncio.TimeoutError:
                    await ctx.send('Timed out!')
                    await UI.delete(delay = 1)
                    return False
                else:
                    message = reaction.message
                for k in reaction.message.reactions:
                    print (k)
                    if k.count == 2:
                        async for user in reaction.users():
                            print (user) 
                            if user == ctx.author:
                                print ("Ding!")
                                if (str(k.emoji)) == "✔":
                                    self.gamelist[active]["Players"].append(ctx.author.id)
                                    self.save_json_dict(self.gamelist)
                                    await ctx.send("Game joined!")
                                    await UI.delete(delay = 3)
                                    return True
                                elif str(k.emoji) == '❌':
                                    await ctx.send ("Command Cancelled!")
                                    await UI.delete(delay = 2)
                                    return False
                                elif str(k.emoji) == '⬅️':
                                    print ("Boing!")
                                    if n == 0:
                                        await ctx.send('No more entries in this direction')
                                        await reaction.remove(ctx.author)
                                    else:
                                        print ("Clang")
                                        n = n-1
                                        cl = 2 
                                        await reaction.remove(ctx.author)
                                        break 
                                elif str(k.emoji) =='➡':
                                    if n + 1 == len(self.gamelist):
                                        await ctx.send('No more entries in this direction')
                                        await reaction.remove(ctx.author)
                                    else:
                                        n = n+1
                                        cl =2
                                        print (n)
                                        await reaction.remove(ctx.author)
                                        break
                            elif user.bot == False:
                                await reaction.remove(user)

    @game.command(aliases = ["del", "d"])
    async def delete(self, ctx, *, name):
        for game in list(self.gamelist.keys()):
            print (name)
            print (game) 
            if str(game) == str(name):
                active = self.gamelist[name]
                if ctx.author.id == active["Host"] or ctx.author.top_role.id == 758429516816580618:
                    del self.gamelist[name]
                    self.save_json_dict(self.gamelist)
                    ctx.send("Game deleted!")
                else:
                    ctx.send("You don't have permission to edit this entry!")

                    

        
    
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
                                                                                                                              
        
        
        
