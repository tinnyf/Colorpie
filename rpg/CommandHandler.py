import asyncio
import collections
import datetime
import traceback
from datetime import datetime as dt
import functools
import math
import random
import typing
import cp_converters
from cp_converters import SmartMember

from rpg.UI.User_Selector import UserSelector
from rpg.daily.DailyCommand import DailyCommand
from rpg.daily.DailyHandler import DailyHandler
from rpg.faction.FactionHandler import FactionHandler, Faction
from rpg.player.PlayerHandler import PlayerHandler
from rpg.votes.VoteHandler import VoteHandler
from rpg.expedition.ExpeditionHandler import ExpeditionHandler

import discord
from discord import app_commands
import discord.ext
from discord.ext import commands, tasks
from discord.ext.commands import Bot, Context

GUILD_ID = 695401740761301056


class CommandHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.faction_handler = FactionHandler()
        self.GUILD_ID = 695401740761301056
        self.MASTER_ROLE = 776142246008455188
        self.player_handler = PlayerHandler(bot)
        self.vote_handler = VoteHandler(bot)
        self.daily_handler = DailyHandler(bot, self.player_handler)
        self.expedition_handler = ExpeditionHandler(self.player_handler)
        self.DISCOVER_ERRORS = [
            "That's a story for another time...",
            "I don't remember that one. Perhaps it's buried in the sand.",
            "When the skald comes, I'll ask her for you",
            "Maybe Kay would know? They're a terrible gossip.",
            "There's a book about this in the capital. I remember from my youth.",
            "They say there's someone out in Minah forest who knows about this.",
            "Every rune governs a different part of our world. It makes you wonder why they destroyed it.",
            "Lie by the fire and rest. You need it.",
            "The more things change, the more people stay the same.",
            "One is one and all alone and ever more shall be it so...",
            "Two, two, the white-gold lines, standing ever-proud oh... ",
            "Three, three, the violent... ",
            "Four for the sunlight keepers...",
            "Five for the symbols in the tomb...",
            "Six for the six councillors...",
            "Seven for the seven stars in the sky...",
            "Eight for the eight old makers...",
            "Nine for the nine brave fighters...",
            "Ten for the ten Constellations.... ",
            "Eleven for the eleven that slew the seven",
            "Twelve for the twelve world-changers. ",
            "From the top of Miya Peak, you can see for miles in each direction."
        ]
        self.runes = ["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
                      "Min", "Thark", "Set", "Ged", "Dorn", "Lae"]
        self.ctx_menu = discord.app_commands.ContextMenu(
            name='Give Relics',
            callback=self.give_relics_callback
        )
        self.see_relics = discord.app_commands.ContextMenu(
            name = "See Relics",
            callback = self.see_relics_callback
        )
        self.bot.tree.add_command(self.ctx_menu)
        self.bot.tree.add_command(self.see_relics)


    async def see_relics_callback(self, interaction, user: discord.Member):
        await interaction.response.send_message(
            f"{user.name} has {self.player_handler.get_relics(self.player_handler.get_player_id(user))} relics!")

    async def give_relics_callback(self, interaction: discord.Interaction, target: discord.Member):

        async def modal_callback(interaction: discord.Interaction):
            try:
                player_id = self.player_handler.get_player_id(target)
                print(f"player_id output: {player_id}")
                if not player_id:
                    await interaction.response.send_message(f"This user probably hasn't registered!")
                    return False
            except AttributeError:
                await interaction.response.send_message(f"This user probably hasn't registered!")
                return False
            success, message = self.spend_relics(interaction.user, int(modal.children[0].value))
            if success:
                self.player_handler.set_relics(self.player_handler.get_player_id(target),
                                               self.player_handler.get_relics(player_id) + int(modal.children[0].value))
                await interaction.response.send_message(
                    f"Sent {target.name} {modal.children[0].value} relics! How generous!")
            else:
                await interaction.response.send_message(message)

        discord_members = [player.get_discord_reference() for player in self.player_handler.get_players()]
        if not interaction.user.id in discord_members:
            await interaction.response.send_message("You must be registered to use this command!")
            return False
        modal = self.relic_modal(interaction.user, modal_callback)
        await interaction.response.send_modal(modal)

    def spend_relics(self, user, relics):
        player_id = self.player_handler.get_player_id(user)
        try:
            if relics <= 0:
                return False, "Invald Input"
            if relics <= self.player_handler.get_relics(player_id):
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - relics)
                return True, f"Spent {relics} relics!"
            else:
                return False, "You don't have enough relics!"
        except ValueError:
            return False, "Invalid Input!"

    def is_tinnyf():
        def predicate(interaction):
            return interaction.message.author.id == 842106129734696992

        return commands.check(predicate)

    def relic_modal(self, author, callback):
        modal = discord.ui.Modal(title="Relic Input")
        modal.on_submit = callback
        relics = self.player_handler.get_relics(self.player_handler.get_player_id(author))
        relic_count = discord.ui.TextInput(
            label=f"Spend some of your {self.player_handler.get_relics(self.player_handler.get_player_id(author))} relics!",
            placeholder=f"1-{relics}", )
        modal.add_item(relic_count)
        return modal

    @is_tinnyf()
    @app_commands.command()
    async def found(self, interaction, name:str):
        role = await ctx.guild.create_role(name=name, reason="Created for the game")
        await ctx.send(self.faction_handler.found(name, role.id))

    # this can't take self!
    @is_tinnyf()
    @commands.command()
    async def register(self, ctx, *, word):
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
        self.faction_handler.register(word, text.content)

    # @commands.cooldown(6, 1800, commands.BucketType.user)
    @commands.command()
    async def discover(self, ctx, *, word):
        try:
            await ctx.send(self.faction_handler.discover(word))
        except KeyError:
            await ctx.send(random.choice(self.DISCOVER_ERRORS))
        print(f"Someone tried to discover {word}")

    @discover.error
    async def discover_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(
                f"You're on cooldown right now, please try again in {round(error.retry_after / 60, 0)} minutes")
        else:
            raise error

    @commands.group()
    async def vote(self, ctx):
        if ctx.invoked_subcommand is None:

            async def election_selector_callback(interaction):
                print("Election Callback triggers!")
                election = self.vote_handler.get_election_from_value(election_selector.values[0])
                print(election)
                view, vote_selector = self.choose_option(election)

                async def vote_selector_callback(interaction):
                    print("Vote Callback triggers!!")
                    option = self.vote_handler.get_option_from_value(election, vote_selector.values[0])
                    if "Relics" in option:
                        modal = discord.ui.Modal(title="Assign Relics!")
                        pass
                        # modal.add_item(discord.ui.TextInput,) =

                    else:
                        if not self.player_handler.get_player_id(ctx.author) in self.vote_handler.get_option_players(
                                election, option):
                            await self.vote_handler.increment_option(self, election, option, 1)
                            self.add_player_option(election, option, self.playerhandler.get_player_id(ctx.author))

                vote_selector.callback = vote_selector_callback
                await ctx.author.send(view=view)

            view, election_selector = self.choose_election(election_selector_callback)
            election_selector.callback = election_selector_callback
            await ctx.author.send(view=view)

    @vote.command()
    async def display(self, ctx):
        for vote in self.vote_handler.get_votes():
            print(vote.get_name())
            print(vote.get_options())

    @is_tinnyf()
    @vote.command()
    async def remove(self, ctx):
        election = self.choose_election(ctx)
        option, interaction = await self.choose_option(ctx, election)
        self.vote_handler.remove_option(election, option)

    @is_tinnyf()
    @vote.command()
    async def delete(self, ctx):
        election = self.choose_election(ctx)
        self.vote_handler.remove_election(election)

    @vote.command()
    async def create(self, ctx, name, emoji: discord.Emoji, *args):
        await ctx.send(self.vote_handler.create(name, emoji.id, list(args)))

    @vote.command(aliases=["stand"])
    async def add(self, ctx):
        election = self.choose_election(ctx)
        if ("election" in list(self.vote_handler.get_types(election)) and ctx.invoked_with == "stand"):
            name = ctx.author.get_name()
            description = f"Click here to vote for {ctx.author.nickname}!"
            value = random.randint(0, 9999999)
            emoji = self.vote_handler.get_emoji(election)
        else:
            instruction = await ctx.send("Please pick a name for the option!")
            name = await self.bot.wait_for("message", check=lambda
                message: message.channel == ctx.channel and message.author.id == ctx.author.id)
            name = name.content
            await instruction.edit("Great! Please now pick a description!")
            description = await self.bot.wait_for("message", check=lambda
                message: message.channel == ctx.channel and message.author == ctx.author)
            description = description.content
            value = random.randint(0, 9999999)
            instruction = await ctx.send("Great! Please react to me with an Emoji!")
            reaction, user = await self.bot.wait_for("reaction_add", check=lambda reaction,
                                                                                  user: reaction.message.content == instruction.content and user.id == ctx.author.id)
            emoji = reaction.emoji
        subcomponent = {"label": name, "description": description, "value": value, "emoji": emoji}
        print(subcomponent)
        await ctx.send(self.vote_handler.add_option(election, value, subcomponent))

    @commands.command(aliases=["Sign-up", "sign-up"])
    async def signup(self, ctx):
        await ctx.send(self.player_handler.create(ctx.author))

    @commands.command()
    async def force_signup(self, ctx, member: SmartMember):
        await ctx.send(self.player_handler.create(member))

    @commands.command()
    async def invite(self, ctx, invited: SmartMember):
        if self.has_permission("Send Invites", self.player_handler.get_player_id(ctx.author)):
            await self.invite_process(invited, self.player_handler.get_faction(invited))
        elif ctx.message.author.id == 842106129734696992:
            factions = self.faction_handler.get_factions()
            sent_message = await ctx.send(
                "Choose a faction",
                components=[
                    discord.ui.Select(
                        options=[
                            discord.ui.SelectOption(
                                label=faction.get_name(),
                                emoji=faction.get_emoji(),
                                description=faction.get_description(),
                                value=i
                            ) for i, faction in enumerate(self.faction_handler.get_factions())
                        ],
                        max_values=1,
                        id="faction_selector"
                    )
                ]
            )
            interaction = await self.bot.wait_for("select_option"
                                                  , check=lambda
                    i: i.user.id == ctx.author.id and i.custom_id == "faction_selector" and i.message.id == sent_message.id)
            selected_faction = self.get_selected_faction(self.faction_handler.get_factions(), interaction)
            await interaction.send(f"Selected {selected_faction.get_name()}")
            await self.invite_process(invited, selected_faction)
        else:
            await ctx.send("You don't have permission to invite someone to your faction.")

    async def invite_process(self, invitee, faction):
        await invitee.create_dm()
        sent_message = await invitee.dm_channel.send(f"You've recieved an invite to faction: {faction.name}",
                                                     components=[
                                                         discord.ui.Button(label="Accept", style=3, id="AcceptButton"),
                                                         discord.ui.Button(label="Refuse", style=4, id="RefuseButton"),
                                                     ])
        interaction = await self.bot.wait_for("button_click", check=lambda i: (sent_message.id == i.message.id))
        if interaction.custom_id == "AcceptButton":
            await invitee.dm_channel.send("You accepted this invite!")
            self.player_handler.change_faction(invitee, faction.get_id())
            await sent_message.delete()
        if interaction.custom_id == "RefuseButton":
            await invitee.dm_channel.send("You rejected this invite!")
            await sent_message.delete()

    def change_faction(self, member, factionid):
        self.player_handler.set_title(self, member, None)
        self.player_handler.set_faction(self, member, factionid)
        self.faction_handler.add_member(player_handler.get_player_id(member))

    def get_selected_faction(self, factions, interaction):
        return factions[int(interaction.values[0])]

    def has_permission(self, permission, player_id):
        try:
            return permission in self.faction_handler.get_permissions(self.player_handler.get_title(player_id),
                                                                      self.player_handler.get_faction(player_id))
        except Exception as e:
            print(e, "Error in has_permission")
            return False

    def is_master(self, user):
        return self.get_role_from_id(self.MASTER_ROLE) in user.roles

    def get_role_from_id(self, role_id):  # Gets a discord role
        return (self.bot.get_guild(self.GUILD_ID)).get_role(role_id)

    def my_interaction_check(self, ctx, interaction):
        return interaction.user.id == ctx.author and interaction.message.id == sent_message.id

    def choose_election(self, ctx):
        selector_view = discord.ui.View()
        selector = discord.ui.Select(max_values=1)
        for item in self.vote_handler.get_votes():
            selector.add_option(label=item.name, emoji=self.bot.get_emoji(item.emoji_id))
        selector_view.add_item(selector)
        return selector_view, selector

    def choose_option(self, election):
        options = self.vote_handler.get_components(election)
        selector_view = discord.ui.View()
        selector = discord.ui.Select(max_values=1)
        for option in options:
            print(option)
            t = discord.SelectOption(
                label=option["label"],
                description=option["description"],
                emoji=self.bot.get_emoji(option["emoji"]["id"])
            )
            if len(t.description) > 98:
                t.description = "My description was too long!"
            selector.append_option(t)
        selector_view.add_item(selector)
        return selector_view, selector

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="expedition")
    async def expedition(self, interaction):
        try:
            await self.expedition_handler.start_waiting(interaction)
        except Exception:
            print(traceback.format_exc())

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="daily")
    async def daily(self, interaction, tag: str = "Day"):
        discord_members = [player.get_discord_reference() for player in self.player_handler.get_players()]
        print(discord_members)
        if not interaction.user.id in discord_members:
            print("Someone not signed up tried to daily")
            await interaction.response.send_message("You must be registered to use this command!")
        print("Before daily_command")
        daily_command = DailyCommand(
            player_handler=self.player_handler,
            daily_handler=self.daily_handler,
            datetime=datetime,
            author=interaction.user,
            logging_channel=interaction.guild.get_channel(952332255227969576),
            now=dt.now(),
            tag=tag,
            reset_hour=19
        )
        data, view = daily_command.run()
        if type(data) == str:
            await interaction.response.send_message(data)
            return False
        print("Before Embed")
        embed = discord.Embed(title=data['title'])
        print('Embed Created')
        try:
            embed.colour = discord.Colour.from_str(data['color'])
        except Exception as e:
            print(e)
            pass


        print("Post Color")
        for count, message in enumerate(data["messages"]):
            if count == 0:
                embed.description = message
            else:
                embed.add_field(name="Extra message", value=message)
        embed.add_field(name="Relics", value=data["relics"])

        print("Prior to send")
        self.player_handler.set_daily(self.player_handler.get_player_id(interaction.user), dt.now())
        try:
            await interaction.response.send_message(embed=embed, view=view)
            print("Sent message with view?")
        except AttributeError:
            await interaction.response.send_message(str(message))
        else:
            await interaction.response.send_message(str(message))


    def errors_on(function):

        @functools.wraps
        def wrapper(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except Exception as e:
                print(e)

        return wrapper

    @is_tinnyf()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command()
    async def remove_daily(self, interaction, title:str):
        await interaction.response.send_message(self.daily_handler.daily_remove(title))


    @is_tinnyf()
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.command(name = "daily_create")
    async def daily_create(self, interaction, place: str, relics: int, time: str, title: str, other: str = "None",
                           color: str = None):
        dailydict = {}
        await interaction.response.send_message("Waiting for input!")
        text = await self.bot.wait_for("message", check=lambda
            m: m.channel == interaction.channel and m.author == interaction.user)
        print("Message received!")
        dailydict['tags'] = [place, time, other]
        dailydict['color'] = color
        dailydict['messages'] = [text.content]
        dailydict['relics'] = relics
        dailydict['title'] = title
        print(f"Initiating daily_create with {dailydict}")
        self.daily_handler.daily_create(dailydict)

    def potency(self, index, rune):
        potdict = {"Stiya": ["Silence", "Lonely Whispers", "Murmurs of Creation", "Words of Power", "Verses of Genesis", "The Making-Song", "Consuming Chorus", "Resonance of the First Flame", "Cry of Creation", "Bellow of the Bellows", "The Shriek of the Dancer"],
                "Lana": ["Silence", "Unchanging Whispers", "Murmurs of Stillness", "Words of Statis", "The Stable Verses", "Songs of the past", "Chorus of years", "Resonance of the constant", "Cry of Gold", "Bellow of the Breathless", "Shriek of the Unchanging Skies " ],
                "Kviz": ["Silence", "Whispers of Fracture", "Murmurs of Dissent", "Words of Rebellion", "Verses of Versus", "Songs of the Rivals", "Chorus of the Struggle", "Rage Resonant", "Cry of Rage", "Bellow of the Fury", "Shriek of the Storm"],
                "Sul": ["Silence", "Whispers of Belonging", "Murmurs of Devotion", "Words everbound", "Verses of Binding", "Songs of the Chains", "Chorus of Sinew", "Resonant Souls", "Cry of the Garrison", "Bellow of the Believer", "Shriek of the Faithful" ],
                "Tuax": ["Silence", "Whispers of Divide", "Murmurs of Distance", "Words of Warding", "Verses of the Shield", "Song of Saltwater", "Chorus of the Defender", "Absent Resonance", "Cry of the Scattered", "Bellow of Silver", "Shriek of the Tombrune"],
                "Yol": ["Silence", "Whispers", "Murmurs", "Words", "Verses", "Song", "Chorus", "Resonance", "Cry", "Bellow", "Shriek"],
                "Min": ["Silence", "Whispers of Night", "Murmurs of the Shadow-Guide", "Words of Judgement", "Verses of Void", "Song of the Peak", "Chorus of the Stars", "Resonance of Farsight", "Celestial Cry", "Bellow of the Councillor", "Shriek of the Firmament", "Blaze of a thousand stars"],
                "Thark": ["Silence", "Playful Whispers", "Murmurs of the Moth", "Words of Combination", "Verses humming together", "Song of Unity", "Chorus of Chorus'", "Resonance of Resonance", "Cry of the thousand-as-one", "Bellow of Brass", "Shriek of the Windmoth"],
                "Set": ["Silence", "Whispers of Might", "Murmurs of Glory", "Words of Legend", "Verses of the Pass", "Song of Heroes", "Chorus of Gul", "Resonance of the Red Fox", "Cry of the Divine", "Bellow of Challenge", "Shriek of the Thunderspeakers"],
                "Ged": ["Silence", "Whispers of Dirt", "Murmurs of Travel", "Words of the Seas", "Verses of the Forests", "Song of the World", "Chorus of explorers", "A Yoyager's resonance", "Cry of the Circle", "Bellow of the Map-Maker", "Shriek of The Earth"],
                "Dorn": ["Silence", "Whispers of Comfort", "Murmurs of an End", "Words of Resurgence", "Verses of Restoration", "Song of the Slayer", "Chorus of Conflux", "Resonance of Bronze", "Cry of flesh-break", "A Doctor's Bellow", "Shriek of The Flux-Rune"],
                "Lae":["Silence of Stiya", "Whispers of Lana", "Murmurs of Kviz", "Words of Sul", "Verses of Tuax", "Song of Yol", "Chorus of Set", "Resonance of Ged", "Cry of Dorn", "Bellow of the runes", "Shriek of the Countless Powers"]}

        try:
            return potdict[rune][index]
        except IndexError:
            return "Power beyond words"
            # ["Silent", "Whispers", "Murmurs", "Words", "Verses", "Song", "Echoing Chorus", "Resounding Resonance",
            #   "Thunderous Cry", "Deafening Bellow", "Earsplitting Shriek"][index]





    def level_cost(self, player_id, current_runes):
        total = 0
        for current_rune in current_runes:
            print(total)
            total = total + math.floor((math.floor(self.player_handler.get_rune_scores(player_id)[current_rune]/2) ** 3)/2)
            print(total)
            total = total + sum(self.player_handler.get_rune_scores(player_id).values()) * 3
            total = total - 400
        print(total)
        return total


    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name = "runes_document")
    async def runes_document(self, interaction):
        await interaction.response.send_message("https://docs.google.com/document/d/1b5sqLpzG3-A6RgkZx6VVeVmq15la-dVHvPU4m_Wt98k/edit?usp=share_link")


    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="character")
    async def character(self, first_interaction: discord.Interaction):
        user = first_interaction.user
        player_id = self.player_handler.get_player_id(user)
        embed = discord.Embed(title=f"Character details {first_interaction.user.name}")
        try:
            if math.isnan(self.player_handler.get_devoted(player_id)):
                self.player_handler.set_devoted(player_id, None)
        except TypeError:
            pass
        if self.player_handler.get_devoted(player_id):
            embed.add_field(name="Devoted Rune", value=f"{self.player_handler.get_devoted(player_id)}")
        else:
            embed.add_field(name="Devoted Rune", value="None")
        if self.player_handler.get_status(player_id):
            embed.add_field(name="Traits", value="\n".join(self.player_handler.get_status(player_id)))
        else:
            embed.add_field(name="Traits", value="None")

        print("Pre Rune,Strings")
        rune_strings = []
        for rune, score in self.player_handler.get_rune_scores(player_id).items():
            rune_strings.append(f"{rune}: {self.potency(math.floor(score / 4), rune)} ({score})")

        print("Post")
        embed.add_field(name="HP",
                        value=f"{self.player_handler.get_hp(player_id)} / {self.player_handler.get_hp_max(player_id)}")
        embed.set_author(name=user.display_name, icon_url=user.display_avatar.url)
        print("Here!")
        embed.add_field(name="Runes", value="\n".join(rune_strings))
        embed.colour = user.color

        view = discord.ui.View()

        async def view_check(interaction: discord.Interaction):
            return interaction.user.id == first_interaction.user.id

        discard_button = discord.ui.Button(label="Discard your devotion", style=discord.ButtonStyle.danger)

        async def discard_callback(interaction: discord.Interaction):
            await interaction.response.send_message(f"You have rejected {self.player_handler.get_devoted(player_id)}")
            self.player_handler.set_devoted(player_id, None)
            embed.set_field_at(0, name="Devoted Rune", value="None")
            await interaction.message.edit(embed=embed, view=view)

        discard_button.callback = discard_callback

        custom_id = f"{player_id} select menu"
        selector = discord.ui.Select(custom_id=custom_id, max_values=12)
        print("post selector")
        for rune in self.player_handler.get_rune_scores(player_id).keys():
            print(rune)
            selector.add_option(label=rune,
                                description=f"Will add {self.level_cost(player_id, [rune])} to your level up cost")
            print("added option!")

        def get_button(player_id, relics, cost):
            if cost > relics:
                button = discord.ui.Button(label=f"Too expensive to level {cost}/{relics}",
                                           style=discord.ButtonStyle.danger, disabled=True, custom_id="Level_button")
            else:
                button = discord.ui.Button(label=f"Pay cost to level {cost}/{relics}",
                                           style=discord.ButtonStyle.primary, custom_id="Level_button")

                async def button_callback(interaction):
                    self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - cost)
                    for rune in selector.values:
                        self.player_handler.increase_rune(player_id, rune, 1)
                    await interaction.response.send_message("You leveled up your runes!")
                    self.player_handler.remove_status(player_id, f"Defies {str(rune)}")
                    view.clear_items()

                button.callback = button_callback
            return button

        level_button = discord.ui.Button(custom_id="Level_button", label="Select runes to level",
                                         style=discord.ButtonStyle.primary, disabled=True)
        view.add_item(level_button)
        print("Added level button")

        async def selector_callback(interaction):
            for item in view.children:
                if item.custom_id == "Level_button":
                    level_button = item
            view.remove_item(level_button)
            print("Selector 1")
            print(view.children)
            level_button = get_button(player_id, self.player_handler.get_relics(player_id),
                                      self.level_cost(player_id, selector.values))
            print(level_button)
            print("Selector 2")
            try:
                view.add_item(level_button)
            except Error as e:
                print(e)
            print("Selector 3")
            await interaction.response.edit_message(embed=embed, view=view)

        selector.callback = selector_callback
        print("Before adding Selector")
        view.add_item(selector)
        print("Added Selector")
        if self.player_handler.get_devoted(player_id):
            print(f"Devoted to {self.player_handler.get_devoted(player_id)}!")
            view.add_item(discard_button)

        view.interaction_check = view_check

        await first_interaction.response.send_message(embed=embed, view=view)

    @app_commands.default_permissions(use_application_commands=True)
    @app_commands.command(name="heal")
    async def heal(self, interaction, rune: str):
        try:
            view = discord.ui.View()
            view.add_item(item = UserSelector(rune, interaction.user, self.player_handler))
            await interaction.response.send_message("Choose who to heal!", view = view)
        except Exception:
            print(traceback.format_exc())

    @heal.autocomplete("rune")
    async def heal_options(self, interaction, current: str):
        runes = ["Dorn" , "Set",  "Sul"]
        return [app_commands.Choice(name = rune, value = rune, ) for rune in runes if current.lower() in rune.lower()]




    # @app_commands.default_permissions(use_application_commands=True)
    # @app_commands.command(name="trickortreat")
    # async def trick_callback(self, interaction: discord.Interaction, value: int):
    #     player = self.player_handler.get_player_id(interaction.user)
    #     if value > self.player_handler.get_relics(player):
    #         await interaction.response.send_message("You can't bet more relics than you have!")
    #         return False
    #     if value < 0:
    #         await interaction.response.send_message("You can't bet fewer than 0 relics. Obviously.")
    #         return False
    #     if random.randint(1, 10) >= 6:
    #         self.player_handler.set_relics(player, self.player_handler.get_relics(player) + value)
    #         await interaction.response.send_message(f"It's a treat! You get {value} relics!")
    #     else:
    #         self.player_handler.set_relics(player, self.player_handler.get_relics(player) - value)
    #         await interaction.response.send_message("You got tricked! You get nothing! You lose! Goodday sir!")

    @is_tinnyf()
    @commands.command()
    async def daily_remove(self, ctx, value):
        lst = []
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check=lambda m: m.channel == ctx.channel and m.author == ctx.author)
        lst.append(value)
        lst.append(text.content)
        self.daily_handler.daily_remove(lst)


    @is_tinnyf()
    @commands.command()
    async def get_op(self, ctx):
        if ctx.author.id == 842106129734696992:
           await ctx.author.add_roles([ctx.guild.get_role(696382214207832145)])

    @is_tinnyf()
    @commands.command()
    async def daily_stats(self, ctx):
        stats = []
        for list in self.daily_handler.get_dailys():
            stats.append(list[0])
        await ctx.send(collections.Counter(stats))

    @commands.command()
    async def print_daily(self, ctx):
        print(self.daily_handler.print_daily(), "print_daily")
        self.daily_handler.daily_data()

    @is_tinnyf()
    @commands.command()
    async def randomise_all(self, ctx):
        for player in self.player_handler.get_players():
            playerID = player.get_id()
            self.player_handler.randomise_runes(playerID)

    @is_tinnyf()
    @commands.command()
    async def stats(self, ctx, member: SmartMember):
        print(self.player_handler.get_rune_scores(self.player_handler.get_player_id(member)))

    @is_tinnyf()
    @commands.command()
    async def stats_all(self, ctx):
        for player in self.player_handler.get_players():
            playerID = player.get_id()
            print(self.player_handler.get_name(playerID))
            print(self.player_handler.get_rune_scores(playerID))

    @is_tinnyf()
    @commands.command()
    async def merge(self, ctx, original: SmartMember,
                    new: SmartMember):  # Sets one users' ID to be the same as anothers, effectively meaning it returns the same account
        await ctx.send(self.player_handler.merge(self.player_handler.get_player_id(original),
                                                 self.player_handler.get_player_id(new)))



    @app_commands.command(name = "relics", description = "Shows you how many relics you have!")
    async def app_relics(self, interaction):
        await interaction.response.send_message(f"You have {self.player_handler.get_relics(self.player_handler.get_player_id(interaction.user))} relics!")


    @commands.group(aliases=["relic"])
    async def relics(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(
                f" You have {self.player_handler.get_relics(self.player_handler.get_player_id(ctx.author))} relics!")

    @relics.group()
    async def give(self, ctx, member: SmartMember, relics: int):
        discord_members = [player.get_discord_reference() for player in self.player_handler.get_players()]
        if not member.id in discord_members:
            await ctx.send("You must be registered to use this command!")
            return False
        if relics < 0:
            await ctx.send("I hate you for trying this.")
            return False
        reciever_id = self.player_handler.get_player_id(member)
        sender_id = self.player_handler.get_player_id(ctx.author)
        if self.player_handler.get_relics(sender_id) >= relics:
            self.player_handler.set_relics(sender_id, self.player_handler.get_relics(sender_id) - relics)
            self.player_handler.set_relics(reciever_id, self.player_handler.get_relics(reciever_id) + relics)
            await ctx.send(f"You've given {member.name} {relics} relics! How generous!")
        else:
            await ctx.send("If messages from 5 colours were currency, you'd be rich!")

    @is_tinnyf()
    @commands.command()
    async def force_founder(self, ctx, founder: SmartMember):
        factions = self.faction_handler.get_factions()
        sent_message = await ctx.send(
            "Choose a faction",
            components=[
                Select(
                    options=[
                        SelectOption(
                            label=faction.get_name(),
                            emoji=faction.get_emoji(),
                            description=faction.get_description(),
                            value=i
                        ) for i, faction in enumerate(self.faction_handler.get_factions())
                    ],
                    max_values=1,
                    id="faction_selector"
                )
            ]
        )
        interaction = await self.bot.wait_for("select_option"
                                              , check=lambda
                i: i.user.id == ctx.author.id and i.message.id == sent_message.id)
        selected_faction = self.get_selected_faction(self.faction_handler.get_factions(), interaction)
        await interaction.send(f"Selected {selected_faction.get_name()}")
        self.faction_handler.add_member(self.player_handler.get_player_id(founder))
        self.player_handler.force_founder(self.player_handler.get_player_id(founder), selected_faction.get_id())
        await founder.add_roles(ctx.guild.get_role(selected_faction.get_role_id()))

    @commands.has_permissions(manage_messages=True)
    @commands.command()
    async def warn(self, ctx, user: SmartMember, rule):
        CHANNEL = ctx.guild.get_channel(980242255770181693)
        await CHANNEL.send(f"{user.display_name} was warned for breaking Rule {rule} by {ctx.author.name} ")

    @commands.group()
    async def faction(self, ctx):
        if ctx.invoked_subcommand is None:
            player_id = self.player_handler.get_player_id(ctx.author)
            await ctx.send(f"You're in the {self.player_handler.get_faction(player_id)}")
