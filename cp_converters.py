import discord
from discord.ext import commands
import asyncio
import json 

class SmartGroup(commands.Converter):
    async def convert(self,ctx,arg):
        def try_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False
                
        with open ('src/data/groups.json') as json_file_r0:
            try:
                grouplist = json.load(json_file_r0)
            except json.decoder.JSONDecodeError:
                print("JsonDecodeError")
                grouplist = {}
        Group_Iterator =filter(lambda b: arg.lower() in str(b).lower(), grouplist.keys())
        ActiveList = list(Group_Iterator)
        if len(ActiveList) == 0:
            raise commands.BadArgument
        if len(ActiveList) == 1:
            return ActiveList[0]
        else:
            memberlist_str = []
            for mem in range(len(ActiveList)):
                num = mem + 1
                mem_str = f"[{num}] {ActiveList[mem]}"
                memberlist_str.append(mem_str)
            memberlistEmbed = discord.Embed(title="Select a group or type 'cancel'.", description = '\n'.join(memberlist_str))
            await ctx.send(embed=memberlistEmbed)
            
            
        def member_pick(m):
            return m.author == ctx.author and m.channel == ctx.channel and (try_int(m.content) or m.content.lower() == "cancel")
        try:
            confirm = await ctx.bot.wait_for('message', check=member_pick, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send('Badge select timed out')
            raise commands.BadArgument
        else:
            if confirm.content.lower() == "cancel":
                await ctx.send('Selection canceled.')
                raise commands.BadArgument
            else:
                return ActiveList[int(confirm.content) - 1]
            
class SmartBadge(commands.Converter):
    async def convert(self,ctx,arg):
        def try_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False
                
        with open ('src/data/badges.json') as json_file_r0:
            try:
                badgelist = json.load(json_file_r0)
            except json.decoder.JSONDecodeError:
                print("JsonDecodeError")
                badgelist = {}
        Badge_Iterator =filter(lambda b: arg.lower() in str(b).lower(), badgelist.keys())
        ActiveList = list(Badge_Iterator)
        if len(ActiveList) == 0:
            raise commands.BadArgument
        if len(ActiveList) == 1:
            return ActiveList[0]
        else:
            memberlist_str = []
            for mem in range(len(ActiveList)):
                num = mem + 1
                mem_str = f"[{num}] {ActiveList[mem]}"
                memberlist_str.append(mem_str)
            memberlistEmbed = discord.Embed(title="Select a badge or type 'cancel'.", description = '\n'.join(memberlist_str))
            await ctx.send(embed=memberlistEmbed)
        
        def member_pick(m):
            return m.author == ctx.author and m.channel == ctx.channel and (try_int(m.content) or m.content.lower() == "cancel")
        try:
            confirm = await ctx.bot.wait_for('message', check=member_pick, timeout = 60.0)
        except asyncio.TimeoutError:
            await ctx.send('Badge select timed out')
            raise commands.BadArgument
        else:
            if confirm.content.lower() == "cancel":
                await ctx.send('Selection canceled.')
                raise commands.BadArgument
            else:
                return ActiveList[int(confirm.content) - 1]

        

class SmartMember(commands.Converter):
    async def convert(self, ctx, arg):
        def try_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False
            
        def try_lower(string):
            try:
                return string.lower()
            except AttributeError:
                return ""
        if not ctx.guild:
            self.bot.get_guild(id = 695401740761301056)
        is_id = try_int(arg)
        if is_id:
            member = ctx.guild.get_member(int(arg))
            if member:
                return member
            else:
                raise commands.BadArgument
        elif ctx.message.mentions == True:
            return ctx.message.mentions[0]

        else:
            member_iterator = filter(lambda m: arg.lower() in str(m).lower() or arg.lower() in try_lower(m.nick), ctx.guild.members)
            memberlist = list(member_iterator)
            if len(memberlist) == 0:
                raise commands.BadArgument
            if len(memberlist) == 1:
                return memberlist[0]
            else:
                memberlist_str = []
                for mem in range(len(memberlist)):
                    num = mem + 1
                    mem_str = f"[{num}] {memberlist[mem]}"
                    memberlist_str.append(mem_str)
                memberlistEmbed = discord.Embed(title="Select a member or type 'cancel'.", description = '\n'.join(memberlist_str), color=0x71368a)
                await ctx.send(embed=memberlistEmbed)

                def member_pick(m):
                    return m.author == ctx.author and m.channel == ctx.channel and (try_int(m.content) or m.content.lower() == "cancel")
                try:
                    confirm = await ctx.bot.wait_for('message', check=member_pick, timeout = 60.0)
                except asyncio.TimeoutError:
                    await ctx.send('Member select timed out')
                    raise commands.BadArgument
                else:
                    if confirm.content.lower() == "cancel":
                        await ctx.send('Selection canceled.')
                        raise commands.BadArgument
                    else:
                        return memberlist[int(confirm.content) - 1]

class SmartRole(commands.Converter):

    async def convert(self, ctx, arg):
        def try_int(string):
            try:
                int(string)
                return True
            except ValueError:
                return False

        if ctx.message.role_mentions:
            return ctx.message.role_mentions[0]
        else:

            role_iterator = filter(lambda r: arg.lower() in str(r).lower() or str(arg) == str(r.id), ctx.guild.roles)
            rolelist = list(role_iterator)

            if len(rolelist) == 0:
                raise commands.BadArgument
            elif len(rolelist) == 1:
                return rolelist[0]
            else:
                rolelist_str = []
                for r in range(len(rolelist)):
                    num = r + 1
                    r_str = f"[{num}] {rolelist[r]}"
                    rolelist_str.append(r_str)
                rolelistEmbed = discord.Embed(title="Select a role or type 'cancel'.", description = '\n'.join(rolelist_str), color=0xffb6c1)
                await ctx.send(embed=rolelistEmbed)

                def role_pick(m):
                    return m.author == ctx.author and m.channel == ctx.channel and (try_int(m.content) or m.content.lower() == "cancel")
                try:
                    confirm = await ctx.bot.wait_for('message', check=role_pick, timeout = 60.0)
                except asyncio.TimeoutError:
                    await ctx.send('Role select timed out')
                    raise commands.BadArgument
                else:
                    if confirm.content.lower() == "cancel":
                        await ctx.send('Selection canceled.')
                        raise commands.BadArgument
                    else:
                        return rolelist[int(confirm.content) - 1]
