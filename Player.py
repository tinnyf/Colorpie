from datetime import datetime
import random
#Faction[Title][Permission]
#Faction[Users][Title]
#FactionMember.has_permission == User.has_title + Title.has_permission
#CpUser - invites stored somewhere.

class Player:
    def __init__(self, discord_reference, ID, name):
        self.id = ID
        self.name = name
        self.relics = 50
        self.daily = datetime.now()
        self.discord_reference = discord_reference
        self.title = None
        self.runes = ["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
        "Min", "Thark", "Set", "Ged", "Dorn", "Lae"]
        self.rune_scores = self.randomise_runes()

    def get_faction(self, source, member): #Source should always be the same, but I'm worried about calling for factiondict in here since it doesn't exist... is that stupid?
        for faction in source:
            if member.id in source[faction]["members"]:
                return faction
        return None ## not sure what to do about it returning string or bool. Is that an issue?

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_relics(self):
        return self.relics

    def get_daily(self):
        return self.daily

    def get_discord_reference(self):
        return self.discord_reference

    def get_title(self):
        return self.title

    def set_id(self, id):
        self.id = id

    def set_title(self, title):
        self.title = title

    def set_faction(self, faction):
        self.faction = faction

    def set_relics(self, relics):
        self.relics = relics

    def set_daily(self,time):
        self.daily = time

    def has_permission(self, permission):
        try:
            faction = self.get_faction(source, member)
            return source[faction]["members"][member.id]["Permissions"][permission]
        except KeyError:
            return False

    def give_relics(self, number):
        self.relics += number

    def randomise_runes(self):
        runes = ["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
        "Min", "Thark", "Set", "Ged", "Dorn", "Lae"]
        rune_levels = {}
        for rune in runes:
            rune_levels[rune] = random.randint(1,10) + random.randint(1,10)
            print("Randomised a rune!")
        return rune_levels

    def set_random_rune_scores(self):
        self.rune_scores = self.randomise_runes()
        print(self.rune_scores)

    def get_rune_scores(self):
        print(self.rune_scores)
        return self.rune_scores

    def increase_rune(self, rune, amount):
        self.rune_scores[rune] += amount
