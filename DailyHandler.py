import discord
from discord import app_commands
import discord.ext
from discord.ext import commands, tasks
import random
import json
from DailyButtons import DailyButtons
import typing
import asyncio
import cp_converters
from cp_converters import SmartMember
import datetime
from datetime import date, time, datetime
import math
from discord.ext.commands import bot
import pickle
import csv
import pandas


class DailyHandler(commands.Cog):

    def __init__(self, bot, playerhandler):
        self.file_locations = {
            "Daily": "src/data/daily"
        }
        try:
            self.daily = self.read_pickle(self.file_locations["Daily"])
        except EOFError:
            self.daily = []
        self.player_handler = playerhandler
        self.daily_buttons = DailyButtons(self.player_handler)

    def read_pickle(self, location):
        with open(location, "rb") as f:
            return pickle.load(f)

    def save_pickle(self, data, location):
        with open(location, "wb") as f:
            pickle.dump(data, f)


    def daily_data(self):
         print(len(self.daily))
         amount, text = random.choice(list(self.daily))
         return amount, text

    def get_dailys(self):
        return(self.daily)

    def daily_create(self, lst):
        try:
            self.daily.append(lst)
            self.save_pickle(self.daily, self.file_locations["Daily"])
        except AttributeError as e:
            daily = []
            daily.append(lst)
            print(text)
            self.save_pickle(self.daily, self.file_locations["Daily"])

    def daily_remove(self, lst):
        self.daily.remove(lst)
        self.save_pickle(self.daily, self.file_locations["Daily"])

    def print_daily(self):
        print(self.daily)

    def daily_extra(self, text: str, player_id) -> (list[str], list[discord.ui.button]):
        messages = []
        buttons = []
        view = discord.ui.View()

        async def view_check(interaction:discord.Interaction):
            return self.player_handler.get_player_id(interaction.user) == player_id

        view.check = view_check

        if "Minted on the ascension of Tan-Mjol" in text or "dead Reclaimer scout" in text:
            t = self.player_handler.test(player_id, 2, "Yol" )
            if t > 0:
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + (5*t))
                messages.append(f"You made {5*t} extra relics from your excellent negotation skills!")

        elif "Enamelled map" in text:
            t = self.player_handler.test(player_id, 5, "Ged")
            if t > 0:
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - 20)
                messages.append(f"Inspired, you shift the arms to your current positions. The stars shift above you, and radiant light shines directly down upon you. You are empowered by the rune Ged. However, the item was consumed before you got your relics.")
                self.player_handler.increase_rune(player_id, "Ged", 1)
                if self.player_handler.get_rune_scores(player_id)["Ged"] == 20:
                    messages.append("You explode with brilliant light. You are now a wielder of Ged, tied forever in spirit to this spot. Contact tinny.")

        elif "Money is money, right?" in text:
            player = random.choice(self.player_handler.get_players())
            adv = self.player_handler.get_rune_scores(player_id)["Yol"] - player.get_rune_scores()["Kviz"]
            if adv > 0:
                messages.append(f"You successfully mugged {player.name}, they lose 20 relics")
                player.give_relics(-20)
            elif adv < -5:
                messages.append(f"{player.name} seriously hurt you. Your stats are damaged.")
                self.player_handler.increase_rune(player_id, random.choice(self.player_handler.get_rune_scores(player_id).keys()), -1)

        elif "Unfortunately, the light is temperamental" in text:
            if self.player_handler.test(player_id, 3, "Stiya") > 0:
                messages.append("You're able to hold the light together, creating a torch that will never extinguish. Inside, the rune Stiya burns, and strengthens you.")
                self.player_handler.increase_rune(player_id, "Stiya", 1)
                if self.player_handler.get_rune_scores(player_id)["Stiya"] == 20:
                    messages.append("You glow with the light of the makers. You are now a wielder of Stiya, the torch your locus of creation.")

        elif "chunk of glass is wedged in the earth" in text:
            if self.player_handler.test(player_id, 3, "Min") > 0:
                messages.append("Reflected in the glass, you can see more and more glass, a conglomerate that holds the sunlight in place, lighting the capital even at night.")

        elif "collar of bronze ends" in text:
            adv = self.player_handler.test(player_id, 2, "Dorn") > 0
            if adv > 0:
                message = "You are imbued with healing magic that allows you to heal injured players, making their medical bills cheaper and letting them work harder. {adv} players get 10 relics each, but they gave you half each!"
                players = random.choices(self.player_handler.get_players(), k = adv)
                for player in players:
                    player.set_relics(player.get_relics() + 5)
                    s = ", "
                    self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + 5 )
                messages.append(message + f" Those players are {s.join(players)}, by the way")

        elif "one star" in text:
            if self.player_handler.get_rune_scores(player_id)["Stiya"] > 20:
                message = "Within you it burns. Power is resurgent. The darkness will not hold. Let creation echo through the ruins."
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + 40)
            else:
                message = "It sits alone, red and dull, and the light it offers is little indeed."
            messages.append(message)

        elif "Signs of struggle" in text:
            if "Defies Kviz." in self.player_handler.get_status(player_id):
                messages.append("It is time to put an end to this. You form the two parallel lines with your fingertips, instinctively, as though guided by some power. The world is still before you, and the people slump, like puppets with their strings cut.")
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + 40)


        elif "Two stars" in text:
            if self.player_handler.get_rune_scores(player_id)["Lana"] > 20:
                messages.append("The sight empowers you. You know that these stars would have been seen by generations before and will be seen by generations to come.")


                view =  discord.ui.View()
                button_1 = discord.ui.Button(style = discord.ButtonStyle.success, label = "Devote to Lana (-100 Relics)")

                async def button_one_callback(interaction: discord.Interaction):
                    if int(self.player_handler.get_discord_reference(player_id)) == interaction.user.id:
                        self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - 100)
                        self.player_handler.set_next_daily = (player_id, 10, "You are now a follower of Lana, the eternal constant. This rune has acted as the principles behind the capital, and the unchanging rulership of the Mage-Kings. Now, it is up to you to shape it." )
                        await interaction.response.send_message("You offer up relics to devote yourself to the marble and gold. You hope it's worth it.")
                        self.player_handler.set_devoted(player_id, "Lana")
                        await interaction.message.delete()

                button_1.callback = button_one_callback

                button_2 = discord.ui.Button(style =discord.ButtonStyle.danger, label = "Reject the stars")

                async def button_two_callback(interaction: discord.Interaction):
                    if int(self.player_handler.get_discord_reference(player_id)) == interaction.user.id:
                        await interaction.response.send_message("You turn your back on the stars, and remain certain of the changing tides of life.")
                        await interaction.message.delete()

                button_2.callback = button_two_callback
                view.add_item(button_1)
                view.add_item(button_2)
            else:
                messages.append("The stars tear the sky, two constant watchers that stare, mismatched, at the ground.")

        elif "Gold, white, red. Gold, white, red." in text:
            if self.player_handler.get_rune_scores(player_id)["Sul"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Sul", 100, "You offer up relics in service of the ties that bind us all."))
            view.add_item(self.daily_buttons.reject_button("There is more that divides us than unites us. There is truth in this, and the stars lie in their suggestion."))

        elif "Today, the stars make a familiar symbol" in text:
            if self.player_handler.get_devoted(player_id) == "Sul":
                view.add_item(self.daily_buttons.defy_button(player_id, "Tuax", "Sul", "All things are one. Warding is against all that you believe, and it must fail."))

            elif self.player_handler.get_rune_scores(player_id)["Tuax"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Tuax", 100, "You offer up relics in service of the rune that divides within from without."))
            view.add_item(self.daily_buttons.reject_button("Given enough time, nowhere is truly secure. All things break apart in time."))

        elif "Only in the water" in text:
            if self.player_handler.get_rune_scores(player_id)["Yol"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Yol", 100, "You offer up relics in the chattering drive that has pushed humanity onward."))
            view.add_item(self.daily_buttons.reject_button("The best moments of life are alone, and quiet. Putting voice to something diminishes it."))

        elif "Where before they were dulled" in text:
            if self.player_handler.get_rune_scores(player_id)["Min"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Min", 100, "You offer up relics in service of the celestial watchers, and the power they have inspire."))
            else:

                def min_mark_extra():
                    self.player_handler.increase_rune(player_id, "Min", 5)
                    self.player_handler.change_hp(player_id, -2)

                view.add_item(self.daily_buttons.status_button(player_id, "Marked by Min", "You offer your body to the stars, and they scour you with radiant light. Your body becomes branded with a complicated starmap, displaying a night sky alien to this one.", "Offer your body to the stars", min_mark_extra))

            view.add_item(self.daily_buttons.reject_button("The stars are strange recently, and you feel you can put no faith in them."))

        elif "The sky is coming together" in text:

            print("Hi!")
            if self.player_handler.get_devoted(player_id) == "Tuax":
                view.add_item(self.daily_buttons.defy_button(player_id, "Thark", "Tuax", "Let not things flow together. Boundaries must be held, less the weak let the cracks in."))
            elif self.player_handler.get_rune_scores(player_id)["Thark"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Thark", 100, "You offer up relics to that which is more than the sum of its parts."))
            view.add_item(self.daily_buttons.reject_button("Alone, there is purpose. Alone, a thing stands powerful."))

        elif "It is a healing sky" in text:
            if self.player_handler.get_devoted(player_id) == "Sul":
                view.add_item(self.daily_buttons.defy_button(player_id, "Dorn", "Sul", "Let things hold. Dorn offers a cycle, of healing and breaking, rebirth chasing its own tail. This is weakness."))
            elif self.player_handler.get_rune_scores(player_id)["Dorn"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Dorn", 100, "You offer up relics to that which offers rebirth."))
            view.add_item(self.daily_buttons.reject_button("Decay, without renewal, has meaning of its own."))

            def lose_relics_extra():
                self.player_handler.set_hp(player_id, self.player_handler.get_hp_max(player_id))
                self.player_id.increase_rune(player_id, "Dorn", 2)

            view.add_item(self.daily_buttons.relics_button(player_id, -20, "You let Dorn heal you, and are restored by its power." , "Offer yourself to Dorn.", lose_relics_extra))


        elif "Now, it all blurs together" in text:
            print ("In!")

            if self.player_handler.get_devoted(player_id) == "Stiya":
                print("a")
                view.add_item(self.daily_buttons.defy_button(player_id, "Lae", "Stiya", "One is one and evermore shall be it so."))
            elif self.player_handler.get_rune_scores(player_id)["Lae"] > 19 and self.player_handler.get_relics(player_id) > 99:
                print("b")
                view.add_item(self.daily_buttons.devotion_button(player_id, "Lae", 100, "You offer up relics to the principles that rule, and the principles that shatter."))

            print("Mid!")
            randomlist = random.sample(["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
            "Min", "Thark", "Set", "Ged", "Dorn", "Lae"], 3)
            print(randomlist)
            try:
                print(randomlist[0], self.player_handler.get_devoted(player_id))
                print (type(self.player_handler.get_devoted(player_id)))
                if type(self.player_handler.get_devoted(player_id)) == str or not math.isnan(self.player_handler.get_devoted(player_id)):
                    print("hello!")
                    if self.player_handler.get_devoted(player_id) == randomlist[0]:
                        print("a")
                        view.add_item(self.daily_buttons.defy_button(player_id, randomlist[1], randomlist[0], "Unity offers a strange defiance."))
                        print("A")
                else:
                    print("here!")
                if self.player_handler.get_rune_scores(player_id)[randomlist[2]] > 19 and self.player_handler.get_relics(player_id) > 99:
                    print("b")
                    view.add_item(self.daily_buttons.devotion_button(player_id, randomlist[2], 100, "You offer up relics to the principles that rule, and the principles that shatter."))
                    print("B")
                else:
                    print ("Passed without incident")
            except Error as e:
                raise e

            view.add_item(self.daily_buttons.reject_button("You will find your own meaning."))
        elif "For each of you, the skies look different" in text:

            if self.player_handler.get_devoted(player_id) == "Min":
                view.add_item(self.daily_buttons.defy_button(player_id, "Ged", "Min", "Sky must overcome earth. The stars see no difference in their attitudes toward us, and this impartiality is precious."))
            elif self.player_handler.get_rune_scores(player_id)["Ged"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Ged", 100, "You offer up relics to the world that fosters our universalities and our differences."))

            print("Here!")
            view.add_item(self.daily_buttons.relics_button(player_id, 20, "You record notes, and later sell them. They're worth 20 relics.", "Jot down the stars as you see them."))


            def lose_relics_extra():
                self.player_id.increase_rune(player_id, "Ged", 2)

            print ("Here!")
            view.add_item(self.daily_buttons.relics_button(player_id, -20, "You explore the world around you, following the stars. Though you must pay, you feel more connected to the world." , "Follow the night guides.", lose_relics_extra))

        elif "The world is spread before you, countless options offered by it." in text:

            async def select_callback(interaction):
                print('callback init')
                rune = locations[select.values[0]]["rune"]
                print(rune)
                self.player_handler.increase_rune(player_id, rune, 2)
                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + 10)
                print("before response!")
                await interaction.response.send_message(locations[select.values[0]]["Message"])
                view.stop()

            locations = {"Minah Forest": {"Message": "In the forest depths, the trees seem to whisper. They promise a new genesis, new creation. A new beginning. You resonate more with the rune Stiya.", "relics": 10, "rune": "Stiya" },
            "The Capital Gates": {"Message": "The gateway to the capital is the same as it ever was. The marble and gold stands strong. You feel more connected to the rune Lana.", "rune": "Lana"},
            "Pass of Gul": {"Message": "Here, where the mountains have been broken, division is resurgent. Power crackles through the wound. You feel more connected to the rune Kviz.", "rune": "Kviz"},
            "The Bastion of Gul": {"Message": "Standing above the rubble, this stronghold of the capital's might will never fall. Even now. You feel more connected to the rune Sul.", "rune": "Sul"},
            "The Councilplace": {"Message": "Here, at this ancient meeting place, the gift of generations of speakers and councillors reaching back into history touches you. YOu feel more connected to the rune Yol", "rune": "Yol"},
            "Miya Peak Altar": {"Message": "At the edge of Miya peak is a great symbol, etched into a vast plinth. At its center is an altar, which seems so high it almost makes it to the stars. Your connection to the rune Min has grown", "rune": "Min"},
            "The Capital Forge": {"Message": "Here, ancient machines still combine mixtures. In this act of combination, Thark reaches back to you.", "rune": "Thark"},
            "Rahamida": {"Message": "This southern land have their own legends, and their own heroes. Countless times the aggression of the Kohgang broke against their shields. Now, in this monument to their success, you feel something stir. Your devotion to Set has grown.", "rune": "Set"}
            }

            select = discord.ui.Select(max_values = 1)
            for name, location in locations.items():
                select.add_option(label = name, value = name)

            select.callback = select_callback

            view.add_item(select)

        elif "The earth trembles" in text:
            if self.player_handler.get_devoted(player_id) == "Yol":
                view.add_item(self.daily_buttons.defy_button(player_id, "Set", "Yol", "Strength unyielding listens to no-one. It is through shared thought where change truly blossoms."))
            elif self.player_handler.get_rune_scores(player_id)["Set"] > 19 and self.player_handler.get_relics(player_id) > 99:
                view.add_item(self.daily_buttons.devotion_button(player_id, "Set", 100, "You offer up relics to strength that overcomes."))
            else:
                print("test")

                def set_mark_extra():
                    for rune in self.player_handler.runes:
                        if rune != "Set":
                            self.player_handler.increase_rune(player_id, rune, 5 -self.player_handler.get_rune_scores(player_id)[rune])
                            value = 5

                    self.player_handler.increase_rune(player_id, "Set", 2)
                    self.player_handler.change_hp(player_id, 2)

                print ("Hiya!")
                try:
                    view.add_item(self.daily_buttons.status_button(player_id, "Dominated by Set", "You offer your body to the power within, and are torn apart. Your mind and body are new, but you will be stronger than ever before. Given time. Given time", "[Dangerous] Be reborn by Set", set_mark_extra, discord.ButtonStyle.danger ))
                except Error as e :
                    print(Error)
            view.add_item(self.daily_buttons.reject_button("Might warps the ability for those who ought to rule. Strength alone does not a good leader make."))

        elif "A great beast" in text:
            if self.player_handler.get_devoted(player_id) == "Set" or "Dominated by Set" in self.player_handler.get_status(player_id):
                view.add_item(self.daily_buttons.relics_button(player_id, 60, "You tear the beasts head from its shoulders, and beat its writhing body to the ground. You sell them both for 60 relics.", "Slay the Beast"))
            elif "Defies Set" in self.player_handler.get_status(player_id):
                view.add_item(self.daily_buttons.relics_button(player_id, 60, "You guide the beasts upon the hunters, forcing them to yield. You take their swords and bows, selling them for 60 relics.", "Defy Set and the Hunters"))

            def lose_hp_extra():
                self.player_handler.change_hp(player_id, -2)

            print("a")
            view.add_item(self.daily_buttons.relics_button(player_id, 20, "With careful skill, you guide the hunters upon the clearing. With your weapons, you're able to defeat the beasts, but you're injured in the process. Still, they pay you.", "Join the Hunters", lose_hp_extra))
            print("b")
            view.add_item(self.daily_buttons.relics_button(player_id, 10, "You refuse to take any part in it. Walking away, you find a small treasure.", "Walk away"))
            print("c")



        elif "are joined by a third" in text:
            if self.player_handler.get_devoted(player_id):
                if self.player_handler.get_devoted(player_id) == "Lana":
                    messages.append("This is anathema. No storm can break the constants, and nothing should threaten forever.")
                    defy_button = discord.ui.Button(style = discord.ButtonStyle.danger, label = "Defy Kviz with Lana")

                    async def button_defy_callback(interaction: discord.Interaction):
                        if int(self.player_handler.get_discord_reference(player_id)) == interaction.user.id:
                            self.player_handler.increase_rune(player_id, "Kviz", 0 - self.player_handler.get_rune_scores(player_id)["Kviz"])
                            await interaction.response.send_message("You will never allow Kviz to triumph. Conflict will end. Peace will come. You declare this to the sky and you burn with power.")
                            self.player_handler.add_status(player_id, "Defies Kviz.")
                            await interaction.message.delete()

                    defy_button.callback = button_defy_callback
                    view.add_item(defy_button)
            else:
                if self.player_handler.get_rune_scores(player_id)["Kviz"] > 20:
                    messages.append("The conflict echoes deep within your heart. This is the first truth, proved where tides beat upon the shore and in the crashing of sword on sword.")
                    button_embrace = discord.ui.Button(style = discord.ButtonStyle.success, label = "Devote to Kviz (-100 Relics)")

                    async def button_one_callback(interaction: discord.Interaction):
                        if int(self.player_handler.get_discord_reference(player_id)) == interaction.user.id:
                            if self.player_handler.get_relics(player_id) > 100:
                                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - 100)
                                self.player_handler.set_next_daily = (player_id, 10, "You are now a follower of Kviz, the rune of fracture. Where the lines cross, the world will find itself torn against itself. The Fall was one such crossing. May there be more." )
                                await interaction.response.send_message("You offer up relics to devote yourself to the unceasing struggle. You hope it's worth it.")
                                self.player_handler.set_devoted(player_id, "Kviz")
                            else:
                                await interaction.response.send_message("You don't have enough money! Your daily has been reset, so you can earn some more.")
                                now = datetime.datetime(now)
                                now.day = now.day = 1
                                self.player_handler.set_daily(now)
                                self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) - 20)
                                await interaction.message.delete()



                    button_embrace.callback = button_one_callback
                    view.add_item(embrace_button)

                    button_shun = discord.ui.Button
                    async def button_two_callback(interaction: discord.Interaction):
                        if int(self.player_handler.get_discord_reference(player_id)) == interaction.user.id:
                            await interaction.response.send_message("You turn your back on the stars, and remain certain of the changing tides of life.")
                            await interaction.message.delete()

                    button_shun.callback = button_two_callback
                    view.add_item(button_shun)


        return messages, view
