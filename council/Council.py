import discord
import discord.ext
from discord.ext import commands, tasks
import random
import json
import typing
import asyncio
import cp_converters
from cp_converters import SmartMember, SmartRole
import datetime
from datetime import date, time, datetime
from discord.ext.commands import bot
import pickle
admin_users = [679680827831222310, 129628193811464193, 697402445244137499, 842106129734696992]
voter_roles = [776142371918184479, 776142246008455188]
councillorID = 776142371918184479
council_channels = ['816153720651251722']
voterlist = ["The Athlete", "The Criminal", "The Brain", "The Basket-case", "Scryfall", "Jace", "Chandra", "Nissa", "Ugin", "Nicol Bolas", "Gideon", "Tybalt", "Dovin Baan", "Elesh Norn", "Ajani",
"Vorniclex", "Ragavan", "Saheeli Rai", "Sarkhan", "Tyvar", "Garruk", "Rowan (and Will)", "Will (and Rowan)", "Nahiri", "Sorin", "All of the Eldrazi", "Yawgmoth", "Urza"]


swordEmoji = '⚔️'
# -*- coding: utf-8 -*-

class cp_council(commands.Cog):
     def __init__(self,bot):
        locations = {"Symbols": "src/data/symbols"}
        self.bot = bot
        print('Cp_Council init')
        self.downlist = {}
        try:
            self.symbols = self.read_pickle("Symbols")
        except EOFError:
            self.symbols = {}
        with open ('src/data/council.json') as json_file_r0:
            try:
                self.councillist = json.load(json_file_r0)
                print(self.councillist.keys())
            except json.decoder.JSONDecodeError as p:
                print("JsonDecodeError")
                print(f"{p}")
                self.councillist = {}
        with open ('src/data/challenge.json') as json_file_r0:
            try:
                self.challengelist = json.load(json_file_r0)
                print(self.challengelist.keys())
            except json.decoder.JSONDecodeError as p:
                print("JsonDecodeError")
                print(f"{p}")
                self.challengelist = {}
        with open ('src/data/users.json') as json_file_r0:
            try:
                self.userlist = json.load(json_file_r0)
                print(self.userlist.keys())
            except json.decoder.JSONDecodeError as p:
                print("JsonDecodeError")
                print(f"{p}")
                self.userlist = {}

     def save_json_dict(self, dict):
        with open("src/data/council.json", 'w') as json_file:
            json.dump(dict,json_file)

     def save_json_dict2(self, dict):
        with open("src/data/challenge.json", 'w') as json_file:
            json.dump(dict,json_file)

     def save_json_dict3(self, dict): #What the fuck even is a parameter anyway lol
        with open("src/data/users.json", 'w') as json_file:
            json.dump(dict,json_file)

     def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

     def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)

     async def edit_element(self, ctx, bot, component): #This whole function should handle input data
        def edit_response(message):
            return message.author == ctx.author and message.channel == ctx.channel and ((message.content.lower()[0:4]) == ("edit") or message.content.lower()[0:4] == ("done"))
        try:
            response = await self.bot.wait_for('message', check =edit_response, timeout = 300.0)
        except asyncio.TimeoutError:
            await ctx.send('Response timed out')
            await component.delete(delay=1)
            return "Timeout"
        else:
            if response.content.lower()== "cancel":
                await ctx.send('Command canceled')
                await component.delete()
            else:
                print(response.content)
                return (response.content)

     async def CRole(self, ctx, user):
         roles_temp = user.roles
         if not ctx.guild.get_role(776142371918184479) in roles_temp:
             roles_temp.append(ctx.guild.get_role(776142371918184479))
             await user.edit(roles = roles_temp)


     async def CanVote(self, ctx, user, challenge):
         n = 0
         print ('check')
         temp = []
         try:
             for l in user.roles:
                 temp.append(l.id)
         except AttributeError:
             temp = self.bot.get_guild(695401740761301056).get_member(ctx.user.id).roles
         for val in voter_roles:
            if val in temp:
                print (val)
                n = 1
         if n == 0:
             return False
         else:
             if( str(user.id) == (str(self.challengelist[challenge]['Challenger']) or str(user.id) == str(self.challengelist[challenge]['Defender']))):
                 return False
             else:
                print (n)
                print (str(user.id))
                return True

     @commands.command(help = "Use ~inspect <seat emoji> in order to see who owns a particular seat! Useful if you need a particular councillor, but don't know who they are." )
     async def inspect(self, ctx, emoji : discord.Emoji):
         try:
             guild = ctx.guild
             await ctx.send(f'{(guild.get_member(self.councillist[str(emoji.id)]).name)} is the owner of the {str(emoji)} position.')
         except AttributeError:
             await ctx.send('Position vacant')

     @commands.command(help = "Use ~claim to take a particular seat. Please note that the <emoji> needs to be an existent seat unless you're an admin. You can use ~show to see all available seats!")
     async def claim(self, ctx, emoji: discord.Emoji):
        rcp = ctx.guild
        if not emoji.is_usable():
            ctx.send("Unrecognised emoji.")
            return false
        try:
            emojid = str(emoji.id)
            if self.councillist[emojid] == 'Empty':
                for i in self.councillist:
                    if str(self.councillist[i]) == str(ctx.author.id):
                        self.councillist[i] = "Empty"
                self.councillist[emojid] = ctx.author.id
                await ctx.send(f"You are now the owner of the {str(emoji)} position.")
                self.save_json_dict(self.councillist)
                await self.CRole(ctx, ctx.author)

            elif self.councillist[emojid]:
                await ctx.send(f"This position is already taken by {rcp.get_member(self.councillist[emojid]).name}.")
            else:
                await ctx.send("This position does not exist.")
        except KeyError as p:
                print (p)
                await ctx.send("This seat does not seem to exist. If it does, please @tinnyf")

     @commands.command()
     async def grant(self, ctx, emoji: discord.Emoji, user: SmartMember):
        global admin_users
        if not ctx.author.id in admin_users:
            await ctx.send("This is an admin only command")
            return False
        self.councillist[str(emoji.id)]= user.id
        self.save_json_dict(self.councillist)
        await self.CRole(ctx, user)
        await ctx.send(f'{user} is now the owner of the {str(emoji)} position.')

     @commands.command()
     async def chat(self, ctx, tchannel, *, message):
        global admin_users
        guild = self.bot.get_guild(695401740761301056)
        if not (ctx.author.id in admin_users or guild.get_member(ctx.author.id).top_role.position >= guild.get_role(696382214207832145).position):
            await ctx.send("This is an admin only command")
            return False
        else:
            guild = self.bot.get_guild(695401740761301056)
            for channel in guild.text_channels:
                if channel.name.lower() == tchannel.lower():
                    await channel.send(message)


     @commands.command(help = "Show is the most useful command. Using it will show every seat and owner. Please note that every seat will show up empty in DM's!")
     async def show(self,ctx):
        neatlist = []
        guild = ctx.guild
        for key in self.councillist:
            try:
                neatlist.append(f'{str(self.bot.get_emoji(int(key)))} - {guild.get_member(self.councillist[key]).name}')
            except AttributeError:
                neatlist.append(f'{str(self.bot.get_emoji(int(key)))} is empty')
                self.councillist[key] = "Empty"
        if ctx.author.id == 896587419606974575:
            random.shuffle(neatlist)
            await ctx.send("I may decide to feed your delusions of grandeur, boy.")
        p = "\n".join(neatlist)
        await ctx.send(p)




     @commands.command()
     async def purge(self, ctx):
         global admin_users
         user = ctx.author
         if not( ctx.author.id in admin_users):
            await ctx.send("You have no power here")
            return False
         else:
             await ctx.send("The council will be purged in 'about 5 minutes'")
             await asyncio.sleep(10)
             for idh in self.councillist.keys():
                 if self.councillist[idh] != "Empty":
                     emoji = self.bot.get_emoji(int(idh))
                     print(f" Emoji ID; {emoji.id}")
                     await self.depose(ctx, emoji)


     @commands.command(help = "You should be able to use ~depose on yourself to leave a seat. Failing that, please @tinnyf. Depose is otherwise an admin only command.")
     async def depose(self, ctx, emoji: discord.Emoji):
         global admin_users
         print (ctx.guild.id)
         user = ctx.guild.get_member(self.councillist[str(emoji.id)])
         if not( ctx.author.id in admin_users or (str(ctx.author.id) == str(self.councillist[str(emoji.id)]))):
             await ctx.send("You can only depose your own seat!")
             return False
         if self.councillist[str(emoji.id)]:
             self.councillist[str(emoji.id)] = 'Empty'
             await ctx.send(f' There is now no owner of {str(emoji)} position.')
             self.save_json_dict(self.councillist)
             roles_temp = user.roles
             try:
                 roles_temp.remove(ctx.guild.get_role(776142371918184479))
             except (IndexError, ValueError) as e:
                 pass
             await user.edit(roles = roles_temp)
         elif self.councillist[int(emoji.id)]:
             self.councillist[int(emoji.id)] = 'Empty'
             await ctx.send(f' There is now no owner of {str(emoji)} position.')
         else:
            await ctx.send("This seat doesn't exist")


     @commands.command()
     async def clear(self, ctx, emoji: discord.Emoji):
        global admin_users
        if not ctx.author.id in admin_users:
            await ctx.send("Only admins can do this")
            return False
        else:
            print ("Admin issued clear on {emoji.name}")
        try:
            self.councillist.pop(str(emoji.id))
            await ctx.send('Position Removed')
            self.save_json_dict(self.councillist)
        except KeyError:
            try:
                self.councillist.pop(int(emoji.id))
                await ctx.send('Position Removed')
                self.save_json_dict(self.councillist)
            except KeyError:
                await ctx.send('Position not found')



     @commands.command(help = "~todo simply tells you what ongoing challenges you're yet to vote in. Please note it can only track votes registered through the bot's challenge fuction")
     async def todo(self, ctx, debug = False):
         temp = []
         temp2 = []
         Tany = 0
         for l in ctx.author.roles:
             temp.append(l.id)
         if not 776142371918184479 in temp:
             await ctx.send(random.choice(["Nothing, your vote doesn't matter. Nothing you do matters here.", "Go and get a council seat and then come back!", "Discover the secrets of the colour pie!", "Annoy Jerdle", "Suggest improvements to my master", "Write an essay on your thoughts on Temur", "Tidy your room"]))
             return False
         for key, challenge in self.challengelist.items():
             print (key, challenge)
             n = 0
             for x in challenge.values():
                 print (x)
                 try:
                     if int(x) == ctx.author.id:
                         n = 1
                         Tany = 1
                 except TypeError:
                     if str(ctx.author.id) in x:
                         n = 1
             if not n == 1:
                 if not key in temp:
                     temp.append(key)
                     if debug == True:
                         await ctx.send(f"No Match Found: ctx.author.id = {ctx.author.id}, list of ID's in {key} (which we would call {str(self.bot.get_emoji(int(key)))} = {self.challengelist[key]}")
                     else:
                        await ctx.send(f" Vote in the {str(self.bot.get_emoji(int(key)))} election")
                        Tany = 1
         if not Tany == 1:
            await ctx.send("You've done all your tasks!")

     @commands.command(help = "To trade seats with another member, type ~trade <user>. The bot can usually recognise users from their username or nickname (as well as a mention, but I don't recommend that). They will recieve a DM telling them to confirm. Please note if for some reason they can't recieve a DM (for example, they've blocked the bot), the command ~accept request should still work.")
     async def trade(self, ctx, user:SmartMember):
         councillors = list(self.councillist.values())
         if not (ctx.author.id in councillors):
             await ctx.send("You don't have a seat!")
             await ctx.send(f"{ctx.author.id} |||| {councillors}")
             return False
         if not int(user.id) in councillors:
             await ctx.send("Your recipient doesn't have a seat")
         try:
             if self.userlist[str(user.id)]["Trade"] != "Empty":
                 await ctx.send("Your recipient already has a pending seat.")
                 return False
         except KeyError as r:
             print (r)
         try:
             self.userlist[str(user.id)]["Trade"] = str(ctx.author.id)
         except KeyError:
             self.userlist[str(user.id)] = {}
             self.userlist[str(user.id)]["Trade"] = str(ctx.author.id)
         self.save_json_dict3(self.userlist)
         await user.create_dm()
         await user.dm_channel.send(f"You've recieved a trade request from {ctx.author.name}, please type ~accept request to take it.")

     @commands.command()
     async def reject(self, ctx, sub = None):
         if sub is None:
             try:
                 if self.userlist[str(ctx.author.id)]["Trade"] != "Empty":
                    await ctx.send("You have an unfulfilled trade request, please type ~reject request to accept it")
             except KeyError as R:
                 print (R)
         elif sub.lower() == ('request' or 'trade'):
             try:
                 if self.userlist[str(ctx.author.id)]["Trade"] != "Empty":
                     await ctx.send("Trade request denied")
                     target = str(self.userlist[str(ctx.author.id)]["Trade"])
                     self.userlist[str(ctx.author.id)]["Trade"] = "Empty"
                     target = self.bot.get_guild(695401740761301056).get_member(int(target))
                     await target.create_dm()
                     await user.dm_channel.send(f"Your trade request to {ctx.author.name} was denied")
             except KeyError:
                 await ctx.send("You likely have no trade requests to reject.")

     @commands.group()
     async def accept(self, ctx):
         if ctx.invoked_subcommand is None:
             try:
                 if self.userlist[str(ctx.author.id)]["Trade"] != "Empty":
                    await ctx.send("You have an unfulfilled trade request, please type ~accept request to accept it")
             except KeyError as R:
                 print (R)

     @accept.command()
     async def request(self, ctx):
         targetseat = False
         originseat = False
         try:
             origin = self.userlist[str(ctx.author.id)]["Trade"]
             if origin == "Empty":
                 await ctx.send("You don't have a trade offer")
                 return False
         except KeyError:
             await ctx.send("You probably don't have a trade request, but @tinnyf if that's not the case")
             return False
         else:
             for key, value in self.councillist.items():
                 if str(value) == str(origin):
                     originseat = key
                 elif str(value) == str(ctx.author.id):
                     targetseat = key
             if not originseat:
                await ctx.send("The person who offered you a seat currently has no seat. Deleting trade offer.")
                self.userlist[str(user.id)]["Trade"] = "Empty"
                self.save_json_dict3(self.userlist)
                return False
             elif not targetseat:
                await ctx.send("You don't seem to have a seat. Deleting trade offer.")
                self.userlist[str(ctx.author.id)]["Trade"] = "Empty"
                self.save_json_dict3(self.userlist)
                return False
             else:
                self.councillist[str(originseat)] = int(ctx.author.id)
                self.councillist[str(targetseat)] = int(origin)
                await ctx.send("Seats transferred")
                guild = self.bot.get_guild(695401740761301056)
                channel = guild.get_channel(816153720651251722)
                await channel.send(f"{guild.get_member(int(origin)).name} and {ctx.author.name} have swapped seats!")
                self.save_json_dict(self.councillist)
                self.userlist[str(ctx.author.id)]["Trade"] = "Empty"
                self.save_json_dict3(self.userlist)

     @commands.command()
     async def Paypal(self,ctx):
         embed = discord.Embed()
         embed.description = "I'd like to say that I'm above money, but I'm definitely not. I would never encourage anyone to donate, but if you should wish to, please find my paypal [here](https://paypal.me/tinnyfcoder?locale.x=en_GB)."
         await ctx.send(embed=embed)


     @commands.group()
     async def challenge(self, ctx):
         if ctx.invoked_subcommand is None:
            await ctx.send('Valid subcommands are: Declare, View, and surrender')

     @challenge.command(aliases = ['Declare'], help = 'Use this command to declare a challenge against a particular seat. Usage: ~challenge declare seat' )
     async def declare(self, ctx, seat: discord.Emoji):
        if not str(seat.id) in self.councillist.keys():
            await ctx.send('Seat not found!')
            return False
        else:
            UI = await ctx.send(f'Please confirm you wish to challenge {ctx.guild.get_member(int(self.councillist[str(seat.id)])) } for this seat')
        await UI.add_reaction('✔')
        await UI.add_reaction('❌')
        n=1
        while n != 2 :
            try:
                reaction, user = await self.bot.wait_for('reaction_add',timeout = 60)
            except asyncio.TimeoutError:
                await ctx.send('Timed out!')
                await  UI.delete(delay = 1)
                return False
            else:
                message = reaction.message
            for k in reaction.message.reactions:
                if k.count == 2:
                    if (str(k.emoji)) == "✔":
                        self.challengelist[str(seat.id)] = {'Challenger' : str(ctx.author.id), 'Defender': str(self.councillist[str(seat.id)]), 'CVoters' : [], 'DVoters' : []}
                        await ctx.send(f"Councillors, hear me now! {ctx.author.name} has issued a challenge against {ctx.guild.get_member(int(self.councillist[str(seat.id)])) }. Please vote on the challenge using ~challenge view!")
                        await reaction.message.delete(delay = 3)
                        self.save_json_dict2(self.challengelist)
                        return True
                    elif str(k.emoji) == '❌':
                        await ctx.send ("Challenge cancelled")
                        await reaction.message.delete(delay = 2)
                        return False


     @challenge.command(aliases = ['View'], help = "~challenge view opens up an UI intended to allow users to easily view and vote on challenges. It's very useful, but if you're confused please ask another member of the council. My advice is to think of the emoji as buttons.")
     async def view(self, ctx, Auth = False):
        if (Auth == "True" or Auth == "true" and not ctx.author.id in admin_users):
            await ctx.send("Recieved True, but you're not an admin")
            Auth = False
        await self.bot.wait_until_ready()
        if len(self.challengelist) == 0:
            print("I don't think there are any challenges")
            return
        n=0
        guild = self.bot.get_guild(695401740761301056)
        while True:
            try:
                active = list(self.challengelist.keys())
                active = (active[n])
                host = guild.get_member(int(self.challengelist[active]["Challenger"]))
                defender = guild.get_member(int(self.challengelist[active]["Defender"]))
                embed = discord.Embed(title = f'Election for {str(self.bot.get_emoji(int(active)))}', colour = host.colour)
                embed.set_footer(text = "Challenge %r of %r. Use sword to vote for the challenger, or the emoji for the defender. Cross closes the UI. Use arrows to scroll." %(n+1, len(self.challengelist)))
                embed.set_thumbnail(url=host.display_avatar.url)
                embed.add_field(name = "⚔️Challenger⚔️", value = host.name)
                DefEmoji = self.bot.get_emoji(int(active))
                embed.add_field(name = f'{str(DefEmoji)}Defender{str(DefEmoji)}', value = defender.name )
            except AttributeError as r:
                print (r)
                self.challengelist.pop(active)
                await ctx.send(f"I didn't like the {str(self.bot.get_emoji(int(active)))} challenge so I deleted it, hope that's okay.")
                return False
            temp = []
            temp2 = ''
            for y in self.challengelist[active]["DVoters"]:
                if Auth == True or Auth == "true" or ctx.author.id == int(y):
                   p = f"**{guild.get_member(int(y)).name}**"
                   temp.append(p)
                else:
                    temp.append(random.choice(voterlist))
                temp2 = ', '.join(temp)
            if not len(temp) > 0:
                embed.add_field(name = "Voters for the defender", value = 'No votes yet!')
            else:
                embed.add_field(name = "Voters for the defender", value = f'{temp2}, \n votes = {len(temp)}')
            temp = []
            for y in self.challengelist[active]["CVoters"]:
                if Auth == True or Auth == "true" or ctx.author.id == int(y):
                   p = f"**{guild.get_member(int(y)).name}**"
                   temp.append(p)
                else:
                    temp.append(random.choice(voterlist))
                temp2 = ', '.join(temp)
            if not len(temp) > 0:
                embed.add_field(name = "Voters for the challenger", value = 'No votes yet!')
            else:
                embed.add_field(name = "Voters for the challenger", value = f'{temp2}, \n votes = {len(temp)}')
            try:
                await UI.edit(embed=embed)
            except UnboundLocalError:
                UI= await ctx.send(embed=embed)
            await UI.add_reaction('⚔')
            await UI.add_reaction(str(DefEmoji))
            await UI.add_reaction('⬅️')
            await UI.add_reaction('➡')
            await UI.add_reaction('❌')
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
                                if (str(k.emoji)) == "⚔":
                                        if (str(ctx.author.id) in self.challengelist[active]["CVoters"] or not await self.CanVote(ctx, ctx.author, active)):
                                            await ctx.send("You've already voted for this player or you're not allowed to vote")
                                            await reaction.remove(ctx.author)
                                            cl =2
                                            break
                                        self.challengelist[active]["CVoters"].append(str(ctx.author.id))
                                        try:
                                            self.challengelist[active]["DVoters"].remove(str(ctx.author.id))
                                        except ValueError as p:
                                            pass
                                        self.save_json_dict2(self.challengelist)
                                        await ctx.send("Voted for attacker!")
                                        await reaction.remove(ctx.author)
                                        cl = 2
                                        break
                                elif k.emoji == DefEmoji:
                                    if (str(ctx.author.id) in self.challengelist[active]["DVoters"] or not await self.CanVote(ctx, ctx.author, active)):
                                        await ctx.send("You've already voted for this player or you're not allowed to vote!")
                                        return False
                                    self.challengelist[active]["DVoters"].append(str(ctx.author.id))
                                    try:
                                        self.challengelist[active]["CVoters"].remove(str(ctx.author.id))
                                    except ValueError as p:
                                        pass
                                    self.save_json_dict2(self.challengelist)
                                    await ctx.send("Voted for defender!")
                                    await reaction.remove(ctx.author)
                                    cl = 2
                                    break


                                elif str(k.emoji) == '❌':
                                    await ctx.send ("Command Cancelled!")
                                    await reaction.message.delete(delay = 2)
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
                                        await UI.clear_reactions()
                                        break
                                elif str(k.emoji) =='➡':
                                    if n + 1 == len(self.challengelist):
                                        await ctx.send('No more entries in this direction')
                                        await reaction.remove(ctx.author)
                                    else:
                                        n = n+1
                                        cl =2
                                        print (n)
                                        await reaction.remove(ctx.author)
                                        await UI.clear_reactions()
                                        break
                                else:
                                    print (k.message)
                            elif user.bot == False:
                                await reaction.remove(user)



     @challenge.command()
     async def surrender(self, ctx, user : SmartMember = None, debug = False):
         if user is None:
             user = ctx.author
         else:
             if not (user == ctx.author or ctx.author.id in admin_users):
                 await ctx.send("You're not allowed to surrender on the behalf of someone else")
                 return false
         to_change = []
         if debug == 'True' or debug == True:
             await ctx.send("I can recieve this command I'm just being difficult")
         for n in self.challengelist.keys():
             n = str(n)
             if str(self.challengelist[n]['Challenger']) == str(user.id):
                 print ('Test')
                 if debug == False:
                     await ctx.send(f"{ctx.guild.get_role(776142371918184479).mention}, {user.name} has backed down from their challenge! {ctx.guild.get_member(int(self.challengelist[n]['Defender'])).name} shall retain their seat!")
                 to_change.append(n)
             elif str(self.challengelist[n]['Defender']) == str(user.id): #if user is defender
                 winner = ctx.guild.get_member(int(self.challengelist[n]['Challenger']))
                 await winner.add_roles(ctx.guild.get_role(776142371918184479))
                 await user.remove_roles(ctx.guild.get_role(776142371918184479))
                 if debug == False:
                     await ctx.send(f"{ctx.guild.get_role(776142371918184479).mention}, {ctx.guild.get_member(int(self.challengelist[n]['Challenger'])).name} has claimed the {str(self.bot.get_emoji(int(n)))} seat from {user.name}")
                 for i in self.councillist:
                     if str(self.councillist[i]) == str(self.challengelist[n]['Challenger']):
                         self.councillist[i] = "Empty"
                 self.councillist[n] = int(self.challengelist[n]['Challenger'])
                 to_change.append(n)
             else:
                print (f" n = {n}, {str(self.bot.get_emoji(int(n)))}, author.id = {user.id}, Challenger = {self.challengelist[n]['Challenger']} , Defender = {self.challengelist[n]['Defender']}")
         if to_change:
             for n in to_change:
                 test = self.challengelist.pop(n)
                 print (n)
                 print (test)
                 self.save_json_dict(self.councillist)
                 self.save_json_dict2(self.challengelist)

     @commands.command()
     async def people(self,ctx):
         toDelete = []
         for user in self.userlist:
             try:
                 await ctx.send(f'{ctx.guild.get_member(int(user)).name}')
             except AttributeError:
                 await ctx.send(f'({user}) has probably left the guild')
                 toDelete.append(user)
             except ValueError:
                 await ctx.send("The word EmbedStructure has got here somehow")
                 toDelete.append(user)
         for i in toDelete:
             self.userlist.pop(i)
         self.save_json_dict3(self.userlist)

     @commands.group()
     async def profile(self,ctx):
         if ctx.invoked_subcommand is None:
             try:
                 if self.userlist[str(ctx.author.id)]['EmbedStructure']:
                     await self.send(ctx)
             except KeyError:
                 await self.create(ctx)

     @profile.group()
     async def cleanfields(self,ctx,user: SmartMember = None):
         sadlist = ['1','2','3','4','5','6','7','8','9','0','.',' ']
         try:
             active = self.userlist[str(user.id)]['EmbedStructure']
             for i in active["fields"]:
                 p = i["name"]
                 n = 0
                 for letter in p:
                     if letter in sadlist:
                         n = n + 1
                     else:
                         break
                 test = p[n: :]
                 print (f'test = {test}')
                 i["name"] = test
                 p = i["value"]
                 n = 0
                 for letter in p:
                     if letter in sadlist:
                         n = n + 1
                     else:
                         break
                 i["value"] = p[n: :]
             self.save_json_dict3(self.userlist)

         except KeyError:
             await ctx.send('No such user found')

     @profile.group()
     async def send(self, ctx, user: SmartMember = None):
         if user is None:
             user = ctx.author
         try:
             Struct = self.userlist[str(user.id)]['EmbedStructure']
             embed = discord.Embed.from_dict(Struct)
             await ctx.send(embed=embed)
         except KeyError:
             await ctx.send("No configured profile!")

     @profile.group(aliases = ['edit'])
     async def create(self, ctx):
        try:
             Struct = self.userlist[str(ctx.author.id)]['EmbedStructure']
             embed = discord.Embed.from_dict(Struct)
        except KeyError:
             embed = discord.Embed(title = 'title', description = 'description', color = ctx.author.colour)
             embed.set_thumbnail(url=ctx.author.avatar_url)
             n = 0
             while n < 5:
                 embed.add_field(name = "Field Title", value =  "Field contents")
                 n = n + 1
        structlist = {0:'Struct'}
        structlist[1] = embed.title
        structlist[2] = embed.description
        n = 0
        c = 0
        for i in embed.fields:
            n = n + 1
            i.name = (f'{n}. {i.name}')
            structlist[n] = i.name
            embed.set_field_at((c), name = structlist[n], value = f'{n+1}. {i.value}')
            n = n + 1
            structlist[n] = f'{n}. Field contents'
            c = c + 1
        UI = await ctx.send(embed=embed)
        print (structlist)
        await ctx.send('Please type edit [index or name] [contents]. For example, to change the item marked 1 to hi, please write edit 1 hi. To change the title to potato write edit title potato. Type done when done.')
        while True:
            EDICT = embed.to_dict()
            response = await self.edit_element(ctx, bot, UI)
            if (response == "Timeout"):
                try:
                    self.userlist[str(ctx.author.id)]['EmbedStructure'] = EDICT
                except KeyError:
                    self.userlist[str(ctx.author.id)] = {}
                    self.userlist[str(ctx.author.id)]['EmbedStructure'] = EDICT

            elif not (response == "done" or response ==  "Done"):
                blist = response.split()
                del blist[0]
                target = blist.pop(0)
                text = " ".join(blist)
            else:
                target = ''
                text = ''
            if target.isdigit():
                for i in EDICT['fields']:
                    if (i['name']).split('.')[0] == target:
                        i['name'] =f"{target}. {text}"
                    elif (i['value']).split('.')[0] == target:
                        i['value'] = f"{target}. {text}"
            elif (response == 'done' or response == "Done"):
                for i in EDICT['fields']:
                    temp = (i["name"]).split('.')
                    del temp[0]
                    temp = ".".join(temp)
                    temp = temp[1: : ]
                    i["name"] = temp
                    temp = (i["value"]).split('.')
                    del temp[0]
                    temp = ".".join(temp)
                    temp = temp[1: : ]
                    i["value"] = temp
                await UI.edit(embed = embed)
                try:
                    self.userlist[str(ctx.author.id)]['EmbedStructure'] = EDICT
                except KeyError:
                    self.userlist[str(ctx.author.id)] = {}
                    self.userlist[str(ctx.author.id)]['EmbedStructure'] = EDICT
                await ctx.send('Saved')
                self.save_json_dict3(self.userlist)
                return True
            else:
                try:
                    EDICT[target] = text
                except KeyError as p:
                    await ctx.send("This object is not found")
            embed = discord.Embed.from_dict(EDICT)
            await UI.edit(embed = embed)

     @commands.command(aliases = ["hp", "housepoint"])
     @commands.dm_only()
     async def up (self, ctx, member: discord.Member, *, reason):
        if member != ctx.author:
            try:
                self.userlist[member.id]["reps"].append(reason)
            except KeyError:
                try:
                    self.userlist[member.id]["reps"] = [reason]
                except KeyError:
                    self.userlist[member.id] = {}
                    self.userlist[member.id]["reps"] = [reason]
            await ctx.send(f"Repped {member.name}")
            self.save_json_dict3(self.userlist)
        else:
            await self.bot.get_guild(695401740761301056).get_channel(695401740761301059).send(f'{ctx.author.mention} tried to upvote themselves lol')

     @commands.command(aliases = ["alert", "flag"])
     @commands.dm_only()
     async def down (self, ctx, member:discord.Member, *, reason):
         try:
            self.downlist[member.id].append(reason)
         except KeyError:
            self.downlist[member.id] = []
            self.downlist[member.id].append(reason)
         embed = discord.Embed(title="Recieved a flag!", description=f"{member.mention} was flagged!")
         embed.add_field(name = "Reason", value = reason)
         embed.add_field(name = "Flagger", value = ctx.author.name)
         embed.add_field(name = "Count", value = f"{len(self.downlist[member.id])} times this restart")
         embed.color = discord.Colour.red()
         await self.bot.get_guild(695401740761301056).get_channel(793161418365992970).send(embed=embed)
         await ctx.send("Your message is with staff!")
         print(f"Recieved downvote {member.nickname}, {reason}")

     @commands.command(aliases = ["total"])
     async def upshow (self, ctx, role: SmartRole):
        count = 0
        error_list = [ ]
        for Mid in self.userlist:
            try:
                if role in (ctx.guild.get_member(int(Mid))).roles:
                    count = count + len(self.userlist[Mid]["reps"])
            except KeyError:
                pass
            except TypeError:
                self.userlist[Mid]["reps"] = []
            except AttributeError:
                error_list.append(Mid)
        for user_id in error_list:
            del self.userlist[user_id]
        await ctx.send(f"That role has {count} points")
#     n )

     @commands.command()
     async def explain(self, ctx, emoji: discord.Emoji):
         text = await self.bot.wait_for("message", check = lambda m: m.channel == ctx.channel and m.author == ctx.author)
         try:
            self.symbols[emoji.id] = text.content
            self.save_pickle(self.symbols, "symbols")
         except AttributeError as e:
            symbols = {}
            symbols[emoji.id] = text.content
            print(text)
            self.save_pickle(symbols,"symbols")

     @commands.command()
     async def whatis(self, ctx, emoji: discord.Emoji):
         await ctx.send(self.symbols[emoji.id])
