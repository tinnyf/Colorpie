import discord
from discord import app_commands
import discord.ext
from discord.ext import commands, tasks
import typing
import asyncio
from discord.ext.commands import Bot, Context
from Player import Player
from FactionHandler import FactionHandler
from PlayerHandler import PlayerHandler
from VoteHandler import VoteHandler
from DailyHandler import DailyHandler
from Integrations import Integrations
import cp_converters
from cp_converters import SmartMember
import random
import datetime
import collections
from datetime import datetime as dt
GUILD_ID = 695401740761301056

class CommandHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.faction_handler = FactionHandler(bot)
        self.GUILD_ID = 695401740761301056
        self.MASTER_ROLE = 776142246008455188
        self.player_handler = PlayerHandler(bot)
        self.vote_handler = VoteHandler(bot)
        self.daily_handler = DailyHandler(bot, self.player_handler)
        self.integrations = Integrations(bot)
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
        name = 'Give Relics',
        callback = self.give_relics_callback
        )
        self.bot.tree.add_command(self.ctx_menu)


    async def give_relics_callback(self, interaction: discord.Interaction, target : discord.Member):

        async def modal_callback(interaction: discord.Interaction):
            try:
                player_id = self.player_handler.get_player_id(target)
                print(f"player_id output: {player_id}")
                if player_id == False:
                    await interaction.response.send_message(f"This user probably hasn't registered!")
                    return False
            except AttributeError:
                await interaction.response.send_message(f"This user probably hasn't registered!")
                return False
            success, message= self.spend_relics(interaction.user, int(modal.children[0].value))
            if success == True:
                self.player_handler.set_relics(self.player_handler.get_player_id(target), self.player_handler.get_relics(player_id) + int(modal.children[0].value))
                await interaction.response.send_message(f"Sent {target.name} {modal.children[0].value} relics! How generous!")
            else:
                await interaction.response.send_message(message)

        modal = self.relic_modal(interaction.user, modal_callback)
        await interaction.response.send_modal(modal)

    def spend_relics (self, user, relics ):
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
        def predicate(ctx):
            return ctx.message.author.id == 842106129734696992
        return commands.check(predicate)

    def relic_modal(self, author, callback):
        modal = discord.ui.Modal(title = "Relic Input")
        modal.on_submit = callback
        relics = self.player_handler.get_relics(self.player_handler.get_player_id(author))
        relic_count = discord.ui.TextInput(
            label = f"Spend some of your {self.player_handler.get_relics(self.player_handler.get_player_id(author))} relics!",
            placeholder = f"1-{relics}", )
        modal.add_item(relic_count)
        return modal

    @is_tinnyf()
    @commands.command()
    async def found(self, ctx, name):
        role = await ctx.guild.create_role(name = name, reason = "Created for the game")
        await ctx.send(self.faction_handler.found(name, role.id))

     #this can't take self!
    @is_tinnyf()
    @commands.command()
    async def register(self, ctx, *, word):
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check = lambda m: m.channel == ctx.channel and m.author == ctx.author)
        self.faction_handler.register(word, text.content)

    @commands.cooldown(6, 1800, commands.BucketType.user)
    @commands.command()
    async def discover(self, ctx, *, word):
        try:
            await ctx.send(self.faction_handler.discover(word))
        except KeyError:
            await ctx.send(random.choice(self.DISCOVER_ERRORS))
        print(f"Someone tried to discover {word}")

    @discover.error
    async def discover_error(self,ctx,error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"You're on cooldown right now, please try again in {round(error.retry_after/60, 0)} minutes")
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
                        modal = discord.ui.Modal(title = "Assign Relics!")
                        pass
                                    #modal.add_item(discord.ui.TextInput,) =

                    else:
                        if not self.player_handler.get_player_id(ctx.author) in self.vote_handler.get_option_players(election, option):
                            await self.vote_handler.increment_option(self, election, option, 1)
                            self.add_player_option(election, option, self.playerhandler.get_player_id(ctx.author ) )

                vote_selector.callback = vote_selector_callback
                await ctx.author.send(view = view)




            view, election_selector = self.choose_election(election_selector_callback)
            election_selector.callback = election_selector_callback
            await ctx.author.send(view = view)

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

    @vote.command(aliases = ["stand"])
    async def add(self, ctx):
        election = self.choose_election(ctx)
        if ("election" in list(self.vote_handler.get_types(election)) and ctx.invoked_with == "stand"):
            name =   ctx.author.get_name()
            description = f"Click here to vote for {ctx.author.nickname}!"
            value = random.randint(0, 9999999)
            emoji = self.vote_handler.get_emoji(election)
        else:
            instruction = await ctx.send("Please pick a name for the option!")
            name = await self.bot.wait_for("message", check = lambda message: message.channel == ctx.channel and message.author.id == ctx.author.id)
            name = name.content
            await instruction.edit("Great! Please now pick a description!")
            description = await self.bot.wait_for("message", check = lambda message: message.channel == ctx.channel and message.author == ctx.author)
            description = description.content
            value = random.randint(0, 9999999)
            instruction = await ctx.send("Great! Please react to me with an Emoji!")
            reaction, user =await self.bot.wait_for("reaction_add", check = lambda reaction, user: reaction.message.content == instruction.content and user.id == ctx.author.id )
            emoji = reaction.emoji
        subcomponent = {"label": name, "description": description, "value": value, "emoji": emoji}
        print(subcomponent)
        await ctx.send(self.vote_handler.add_option(election, value, subcomponent))


    @commands.command(aliases = ["Sign-up", "sign-up"])
    async def signup(self, ctx):
        await ctx.send(self.player_handler.create(ctx.author))

    @commands.command()
    async def force_signup(self, ctx, member : SmartMember):
        await ctx.send(self.player_handler.create(member))

    @commands.command()
    async def invite(self, ctx, invited:SmartMember):
        if self.has_permission("Send Invites", self.player_handler.get_player_id(ctx.author)):
            await self.invite_process(invited, player_handler.get_faction(member))
        elif ctx.message.author.id == 842106129734696992:
            factions = self.faction_handler.get_factions()
            sent_message = await ctx.send(
                "Choose a faction",
                components = [
                    Select(
                        options = [
                            SelectOption(
                                label = faction.get_name(),
                                emoji = faction.get_emoji(),
                                description = faction.get_description(),
                                value = i
                            ) for i, faction in enumerate(self.faction_handler.get_factions())
                        ],
                        max_values = 1,
                        id = "faction_selector"
                    )
                ]
            )
            interaction = await self.bot.wait_for("select_option"
                , check = lambda i: i.user.id == ctx.author.id and i.custom_id == "faction_selector" and i.message.id == sent_message.id)
            selected_faction = self.get_selected_faction(self.faction_handler.get_factions(), interaction)
            await interaction.send(f"Selected {selected_faction.get_name()}")
            await self.invite_process(invited, selected_faction)
        else:
            await ctx.send("You don't have permission to invite someone to your faction.")


    async def invite_process(self, invitee, faction):
        await invitee.create_dm()
        sent_message = await invitee.dm_channel.send(f"You've recieved an invite to faction: {faction.name}",
        components = [
            Button(label = "Accept", style = 3, id = "AcceptButton"),
            Button(label = "Refuse", style = 4, id = "RefuseButton"),
        ])
        interaction = await self.bot.wait_for("button_click", check = lambda i: (sent_message.id == i.message.id))
        if interaction.custom_id == "AcceptButton":
            await invitee.dm_channel.send("You accepted this invite!")
            self.player_handler.change_faction(member, faction.get_id())
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
            return permission in self.faction_handler.get_permissions(self.player_handler.get_title(player_id), self.player_handler.get_faction(player_id))
        except Exception as e:
            print (e, "Error in has_permission")
            return False

    def is_master(self, user):
        return self.get_role_from_id(self.MASTER_ROLE) in user.roles

    def get_role_from_id(self, role_id): #Gets a discord role
        return (self.bot.get_guild(self.GUILD_ID)).get_role(role_id)

    def interaction_check(self, ctx, interaction):
        return interaction.user.id == ctx.author and interaction.message.id == sent_message.id

    def choose_election(self, ctx):
        selector_view = discord.ui.View()
        selector = discord.ui.Select(max_values = 1)
        for item in self.vote_handler.get_votes():
            selector.add_option(label = item.name, emoji = self.bot.get_emoji(item.emoji_id))
        selector_view.add_item(selector)
        return selector_view, selector

    def choose_option(self, election):
        options = self.vote_handler.get_components(election)
        selector_view = discord.ui.View()
        selector = discord.ui.Select(max_values = 1 )
        for option in options:
            print(option)
            t = discord.SelectOption(
            label = option["label"],
            description = option["description"],
            emoji = self.bot.get_emoji(option["emoji"]["id"])
            )
            if len(t.description) > 98:
                t.description = "My description was too long!"
            selector.append_option(t)
        selector_view.add_item(selector)
        return selector_view, selector


    @commands.command()
    async def daily(self, ctx):
        try:
            player_id = self.player_handler.get_player_id(ctx.author)
            check_time = dt.now()
            next_reset_time = dt.now()
            if check_time.hour < 19:
                check_time = check_time - datetime.timedelta(days = 1)
            else:
                next_reset_time = next_reset_time + datetime.timedelta(days = 1)
            check_time = check_time.replace(hour = 19, minute = 00)
            next_reset_time = next_reset_time.replace(hour= 19, minute = 00)
            if check_time >= self.player_handler.get_daily(player_id):
                amount, data = self.daily_handler.daily_data()
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + int(amount))
                self.player_handler.set_daily(player_id, dt.now())
                await ctx.send(f"{data}")
                extra = await self.daily_handler.daily_extra(data, player_id)
                if extra:
                    await ctx.send(extra)
                message = self.player_handler.daily_runes(self.player_handler.get_player_id(ctx.author))
                if message:
                    ctx.guild.get_member(842106129734696992).dm_channel.send(f"{ctx.author.name} has grown in power.")
                    await ctx.send(message)
            else:
                await ctx.send(f"You're on cooldown for another {str(next_reset_time- dt.now() )}") #It should be 7pm next to dt now
        except TypeError as e:
            print("Error in daily: ", e)

    @is_tinnyf()
    @commands.command()
    async def daily_create(self, ctx, value):
        lst = []
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check = lambda m: m.channel == ctx.channel and m.author == ctx.author)
        lst.append(value)
        lst.append(text.content)
        self.daily_handler.daily_create(lst)


    #should construct a new event object with paths + options with default args(weight=0, start = false)
    @app_commands.default_permissions(manage_messages = True)
    @app_commands.command(name = "create")
    async def event_create(self, interaction: discord.Interaction):
        modal = discord.ui.Modal(title = "Set Up an Event!")
        name = discord.ui.TextInput(
            label = "Choose a name for the event!" ,
            placeholder = "The duck of the night",
            required = True )
        text = discord.ui.TextInput(
            label = "Insert the text for the event!" ,
            placeholder = "Start typing!",
            required = True,
            style = paragraph
            )
        location = discord.ui.TextInput(
            label = "Choose a location for this event!",
            placeholder = "The Capital",
            required = True)



        async def modal_callback(interaction):
            name = name.value
            text = text.value
            location = location.value
            self.event_handler.create_event(name, text, location)
            await interaction.response.send_message("Added a new event!")


        modal.add_item(name)
        modal.add_item(text)
        modal.add_item(location)
        await interaction.response.send_modal(modal)



    @is_tinnyf()
    @commands.command()
    async def daily_remove(self, ctx, value):
        lst = []
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check = lambda m: m.channel == ctx.channel and m.author == ctx.author)
        lst.append(value)
        lst.append(text.content)
        self.daily_handler.daily_remove(lst)

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
    async def merge(self, ctx, original: SmartMember, new: SmartMember): #Sets one users' ID to be the same as anothers, effectively meaning it returns the same account
        await ctx.send(self.player_handler.merge(self.player_handler.get_player_id(original),self.player_handler.get_player_id(new)))

    @commands.group(aliases = ["relic"])
    async def relics(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f" You have {self.player_handler.get_relics(self.player_handler.get_player_id(ctx.author))} relics!")

    @relics.group()
    async def give(self, ctx, member: SmartMember, relics: int):
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
            components = [
                Select(
                    options = [
                        SelectOption(
                            label = faction.get_name(),
                            emoji = faction.get_emoji(),
                            description = faction.get_description(),
                            value = i
                        ) for i, faction in enumerate(self.faction_handler.get_factions())
                    ],
                    max_values = 1,
                    id = "faction_selector"
                )
            ]
        )
        interaction = await self.bot.wait_for("select_option"
        , check = lambda i: i.user.id == ctx.author.id and i.message.id == sent_message.id)
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
