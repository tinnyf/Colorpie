import discord
import discord.ext
from discord.ext import commands, tasks
import typing
import asyncio
from discord.ext.commands import Bot, Context
from discord_components import DiscordComponents, ComponentsBot, Button, Select, SelectOption
from Player import Player
from FactionHandler import FactionHandler
from PlayerHandler import PlayerHandler
from VoteHandler import VoteHandler
import cp_converters
from cp_converters import SmartMember
import random
import datetime
import collections
from datetime import datetime as dt
class CommandHandler(commands.Cog):


    def __init__(self, bot):
        self.bot = bot
        self.faction_handler = FactionHandler(bot)
        self.GUILD_ID = 695401740761301056
        self.MASTER_ROLE = 776142246008455188
        self.player_handler = PlayerHandler(bot)
        self.vote_handler = VoteHandler(bot)
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

    def is_tinnyf():
        def predicate(ctx):
            return ctx.message.author.id == 842106129734696992
        return commands.check(predicate)

    @commands.command()
    async def found(self, ctx, name):
        await ctx.send(self.faction_handler.found(name))

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
            election = await self.choose_election(ctx)
            option, interaction = await self.choose_option(ctx, election)
            print("Look down for option")
            print(option)
            if "relics" in self.vote_handler.get_types(election):
                relics = 0
                relic_message = await interaction.send(
                f"Please add some relics if you wish! You have {self.player_handler.get_relics(self.player_handler.get_player_id(ctx.author))} relics right now!",
                components = [
                    Button(label = "Add 10 relics!",
                    style = "3",
                    custom_id = "add_10"
                    ),
                    Button(
                    label = "Confirm",
                    style = "2",
                    custom_id = "confirm"
                    )
                    ])
                while True:
                    interaction = await self.bot.wait_for("button_click", check = lambda interaction: interaction.user.id == ctx.author.id and interaction.message.id == relic_message.id)
                    if interaction.custom_id == "add_10":
                        relics = relics + 10
                        await interaction.send(f"You've got {relics} relics commited right now")
                    elif interaction.custom_id == "confirm":
                        await interaction.send(f"Voted with {relics} relics")
                        if self.player_handler.get_relics(self.player_handler.get_player_id(ctx.author)) < relics:
                                relics = self.player_handler.get_relics( self.player_handler.get_player_id(ctx.author))
                        self.player_handler.set_relics(self.player_handler.get_player_id(ctx.author), self.player_handler.get_relics(self.player_handler.get_player_id(ctx.author)) - relics)
                        if not self.player_handler.get_player_id(ctx.author) in self.vote_handler.get_option_players(election, option):
                            relics = relics + 50
                        self.vote_handler.increment_option(election, option, relics)
                        self.vote_handler.add_player_option(election, option, self.player_handler.get_player_id(ctx.author))
                        await interaction.send("Vote confirmed!")
            else:
                if not self.player_handler.get_player_id(ctx.author) in self.vote_handler.get_option_players(election, option):
                    await self.vote_handler.increment_option(self, election, option, 1)
                    self.add_player_option(election, option, self.playerhandler.get_player_id(ctx.author))


    @vote.command()
    async def display(self, ctx):
        for vote in self.vote_handler.get_votes():
            print(vote.get_name())
            print(vote.get_options())

    @is_tinnyf()
    @vote.command()
    async def remove(self, ctx):
        election = await self.choose_election(ctx)
        option, interaction = await self.choose_option(ctx, election)
        self.vote_handler.remove_option(election, option)


    @is_tinnyf()
    @vote.command()
    async def delete(self, ctx):
        election = await self.choose_election(ctx)
        self.vote_handler.remove_election(election)

    @vote.command()
    async def create(self, ctx, name, emoji: discord.Emoji, *args):
        await ctx.send(self.vote_handler.create(name, emoji.id, list(args)))

    @vote.command(aliases = ["stand"])
    async def add(self, ctx):
        election = await self.choose_election(ctx)
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
        Subcomponent = SelectOption(label = name, description = description, value = value, emoji = emoji)
        subcomponent = Subcomponent.to_dict()
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
        if self.has_permission(invited, "Send Invites"):
            await self.invite_process(invited, player_handler.get_faction(member))
        elif self.get_role_from_id(master_role) in ctx.author.roles:
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

    def has_permissions(self, permission, player_id):
        try:
            return permission in self.faction_handler.get_permissions(self.player_handler.get_title(), self.player_handler.get_faction())
        except Exception as e:
            print (e)
            return False

    def is_master(self, user):
        return self.get_role_from_id(self.MASTER_ROLE) in ctx.user.roles

    def get_role_from_id(self, role_id): #Gets a discord role
        return (self.bot.get_guild(self.GUILD_ID)).get_role(role_id)

    def interaction_check(self, ctx, interaction):
        return interaction.user.id == ctx.author and interaction.message.id == sent_message.id

    async def choose_election(self, ctx):
        elections = self.vote_handler.get_votes()
        sent_message = await ctx.send(
            "Choose an election!",
            components = [
                Select(options = [SelectOption(
                    label = election.get_name(),
                    emoji = self.bot.get_emoji(election.get_emoji_id()),
                    description = "Pick me!",
                    value = i
                ) for i, election in enumerate(self.vote_handler.get_votes())],
                max_values = 1,
                id = "election_selector"
                )]
        )

        interaction = await self.bot.wait_for("select_option"
            , check = lambda i: i.user.id == ctx.author.id and i.custom_id == "election_selector" and i.message.id == sent_message.id)
        await interaction.send(f"Picked {interaction.component.options[int(interaction.values[0])].label} ")
        return self.vote_handler.get_votes()[int(interaction.values[0])]

    async def choose_option(self, ctx, election):
        options = self.vote_handler.get_components(election)
        subcomponents = []
        for option in options:
            t = SelectOption(**option)
            if len(t.description) > 98:
                t.description = "My description was too long!"
            subcomponents.append(t)
        sent_message = await ctx.send(
            "Choose an option to vote for!",
            components =[Select(options = subcomponents ,
            max_values = 1,
            id = "option_selector")])
        interaction = await self.bot.wait_for("select_option", check = lambda i: i.user.id == ctx.author.id and i.custom_id == "option_selector" and i.message.id == sent_message.id)
        return int(interaction.values[0]), interaction

    @commands.command()
    async def daily(self, ctx):
        try:
            player_id = self.player_handler.get_player_id(ctx.author)
            #IF daily is before the most recent 7pm
            # If it's after 7pm
            check_time = dt.now()
            next_reset_time = dt.now()
            if check_time.hour < 19:
                check_time = check_time - datetime.timedelta(days = 1)
            else:
                next_reset_time = next_reset_time + datetime.timedelta(days = 1)
            check_time = check_time.replace(hour = 19, minute = 00)
            next_reset_time = next_reset_time.replace(hour= 19, minute = 00)
            if check_time >= self.player_handler.get_daily(player_id):
                amount, data = self.faction_handler.daily_data()
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + int(amount))
                self.player_handler.set_daily(player_id, dt.now())
                await ctx.send(f"{data}")
                message = self.player_handler.daily_runes(self.player_handler.get_player_id(ctx.author))
                if message:
                    ctx.guild.get_member(842106129734696992).dm_channel.send(f"{ctx.author.name} has grown in power.")
                    await ctx.send(message)
            else:
                await ctx.send(f"You're on cooldown for another {str(next_reset_time- dt.now() )}") #It should be 7pm next to dt now
        except TypeError as e:
            print(e)

    @is_tinnyf()
    @commands.command()
    async def daily_create(self, ctx, value):
        lst = []
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check = lambda m: m.channel == ctx.channel and m.author == ctx.author)
        lst.append(value)
        lst.append(text.content)
        self.faction_handler.daily_create(lst)

    @is_tinnyf()
    @commands.command()
    async def daily_remove(self, ctx, value):
        lst = []
        await ctx.send("Waiting for input!")
        text = await self.bot.wait_for("message", check = lambda m: m.channel == ctx.channel and m.author == ctx.author)
        lst.append(value)
        lst.append(text.content)
        self.faction_handler.daily_remove(lst)

    @is_tinnyf()
    @commands.command()
    async def daily_stats(self, ctx):
        stats = []
        for list in self.faction_handler.get_dailys():
            stats.append(list[0])
        await ctx.send(collections.Counter(stats))

    @commands.command()
    async def print_daily(self, ctx):
        print(self.faction_handler.print_daily())
        self.faction_handler.daily_data()

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
