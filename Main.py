import discord
from discord import app_commands
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
from Council import cp_council
from CommandHandler import CommandHandler
from FactionHandler import FactionHandler
from Games import TruthGame
from Qotd import Qotd
from Trials import Trials
from Moderation import Moderation

intents = discord.Intents.all()
council_channels = ['816153720651251722']
admin_users = [679680827831222310, 129628193811464193, 842106129734696992,]
voter_roles = [776142371918184479, 776142246008455188]
GUILD_ID = discord.Object(id = 695401740761301056)

class BotInit(Bot):
    def __init__(self, *, intents, application_id, command_prefix):
        super().__init__(intents=intents, application_id = application_id, command_prefix = command_prefix)


    async def setup_hook(self):
        self.tree.copy_global_to(guild=GUILD_ID)
        await self.tree.sync(guild=GUILD_ID)


bot = BotInit(intents=intents, application_id = 974427338857132033, command_prefix =['~','-', "Oh 5 Colors, hear me now ", "5 Colors, I bid thee ", "5 colors, I bid thee"])

@bot.event
async def on_member_remove(member):
    channel = bot.get_guild(695401740761301056).get_channel(695755815612710982)
    await channel.send(f"Goodbye {member.name}! It's been a pleasure!")

@bot.event
async def on_message_delete(message):
    channel = bot.get_guild(695401740761301056).get_channel(1036599243567272036)
    log = discord.Embed(
        title = "Deleted Message",
        description = message.content,
        timestamp = datetime.now(),
        color= message.author.color)
    log.set_author(name=message.author.display_name,icon_url=message.author.display_avatar.url )
    log.add_field(name = "message channel", value =message.channel.name)
    log.add_field(name = "message link", value = message.jump_url)
    await channel.send(embed= log )
    for attachment in message.attachments:
        t = await attachment.to_file()
        await channel.send(file = t)

@bot.event
async def on_message_edit(before,after):
    channel = bot.get_guild(695401740761301056).get_channel(1036599243567272036)
    differences = []
    fixed = ""
    for count, character in enumerate(before.content):
        if character != after.content[count]:
            fixed += f"*{character}*"
        else:
            fixed += character

    log = discord.Embed(
        title = "Edited Message",
        description = before.content,
        timestamp = datetime.now(),
        color = before.author.color)
    log.set_author(name=before.author.display_name,icon_url=before.author.display_avatar.url )
    if len(after.content) < 1000:
        log.add_field(name = "New Text", value = after.content )
    log.add_field(name = "Link to current Message", value = after.jump_url)
    await channel.send(embed= log )

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

# #Ver = 1.1
#
# bot.add_cog(db_updates(bot))



async def cogloader(bot):
    await bot.add_cog(cp_council(bot))
    #await bot.add_cog(cp_events(bot))
    await bot.add_cog(CommandHandler(bot))
    await bot.add_cog(FactionHandler(bot))
    await bot.add_cog(TruthGame(bot))
    await bot.add_cog(Qotd(bot))
    await bot.add_cog(Trials(bot))
    await bot.add_cog(Moderation(bot))

async def main(bot):
    await cogloader(bot)


    async with bot:
        await bot.start(token)




@app_commands.default_permissions(use_application_commands = True)
@bot.tree.context_menu(name='Alert Moderators')
async def report_message(interaction: discord.Interaction, message: discord.Message):
    # We're sending this response message with ephemeral=True, so only the command executor can see it
    await interaction.response.send_message(
        f'Thanks for reporting this message by {message.author.mention} to our moderators.', ephemeral=True
    )
    # Handle report by sending it into a log channel
    log_channel = interaction.guild.get_channel(793161418365992970)  # replace with your channel id
    embed = discord.Embed(title='Reported Message')
    if message.content:
        embed.description = message.content
    embed.set_author(name=message.author.display_name, icon_url=message.author.display_avatar.url)
    embed.timestamp = message.created_at
    url_view = discord.ui.View()
    url_view.add_item(discord.ui.Button(label='Go to Message', style=discord.ButtonStyle.url, url=message.jump_url))
    await log_channel.send(f"Reported by {interaction.user.name}. {interaction.guild.get_role(696382214207832145).mention}", embed=embed, view=url_view)


@app_commands.default_permissions(use_application_commands = True)
@bot.tree.command(name= 'suggest', description = "Send an anonymous suggestion to the mod team!")
async def AnonSuggest(interaction: discord.Interaction):
    modal = discord.ui.Modal(title = "Give a suggestion!")
    rationale = discord.ui.TextInput(placeholder = "It'll be really fun", required = True, label = "Rationale for Suggestion")
    suggestion = discord.ui.TextInput(placeholder = "We should all change our names to be themed", required = True, label = "Suggestion body", style = discord.TextStyle.paragraph)
    modal.add_item(suggestion)
    modal.add_item(rationale)

    async def callback(interaction: discord.Interaction):
        CHANNEL = interaction.guild.get_channel(793161418365992970)
        embed = discord.Embed(title = 'Suggestion')
        embed.description = suggestion.value
        embed.add_field(name = "Rationale", value = rationale)
        await CHANNEL.send(embed=embed)
        await interaction.response.send_message("Thanks for your suggestion! It's with staff right now!", ephemeral = True)

    modal.on_submit = callback
    await interaction.response.send_modal(modal)

@app_commands.default_permissions(use_application_commands = True)
@bot.tree.command(name = 'questionnaire', description = "Please answer our questionnaire about the server")
async def questionnaire(interaction: discord.Interaction):
    modal = discord.ui.Modal(title = "Your voice")

    uncomfortable_input= discord.ui.TextInput(label = "User Flagging",
    placeholder = "If another user is making you feel uncomfortable or upset, what do you do?.", style = discord.TextStyle.paragraph, max_length = 1024)

    improvement_input = discord.ui.TextInput(label = "egg",
    placeholder = "All ideas are appreciated", style = discord.TextStyle.paragraph, max_length = 1024)

    listen_input = discord.ui.TextInput(label = "Do you feel listened to?",
    placeholder = "We aim to improve through feedback", style = discord.TextStyle.short, max_length = 1024)

    listen_improve_input = discord.ui.TextInput(label = "How can we improve with this?",
    placeholder = "All ideas are appreciated", style = discord.TextStyle.paragraph, max_length = 1024)

    arguement_input = discord.ui.TextInput(label = "Discussion Flagging",
    placeholder = "If a discussion is escalating out of control, what do you do?", style = discord.TextStyle.paragraph, max_length = 1024)

    arguement_improve_input = discord.ui.TextInput(label = "Suggesting improvements",
    placeholder = "How can we improve reporting for hostile users and situations?", style = discord.TextStyle.paragraph, max_length = 1024)

    children = [listen_input, listen_improve_input, arguement_input, uncomfortable_input, arguement_improve_input]
    for item in children:
        modal.add_item(item)

    async def callback(interaction: discord.Interaction):
        CHANNEL = interaction.guild.get_channel(793161418365992970)
        embed= discord.Embed(title = "Interaction Feedback")
        for child in modal.children:
            embed.add_field(name = child.label ,value = child.value)
        embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
        await CHANNEL.send(embed=embed)
        await interaction.response.send_message("Thank you for your input! We really appreciate it", ephemeral = True )

    modal.on_submit = callback
    await interaction.response.send_modal(modal)




with open("token.txt") as f:
    token = f.read()

asyncio.run(main(bot))
