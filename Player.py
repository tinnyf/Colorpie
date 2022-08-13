from datetime import datetime
import datetime as dt
import random
import ast
#Faction[Title][Permission]T
#Faction[Users][Title]
#FactionMember.has_permission == User.has_title + Title.has_permission
#CpUser - invites stored somewhere.

class Player:
    def __init__(self, id, name, discord_reference, relics = 50, daily = datetime.now(), title = None, rune_scores = None, runes = None, faction = None,
    HP = random.randint(1,4) + random.randint(1,4) + random.randint(1,4),
    inventory = [],
    status = []


    ):
        self.id = id
        self.name = name
        self.relics = relics
        if isinstance(daily, str):
            daily = datetime.strptime(daily, "%Y-%m-%d %H:%M:%S.%f")
        self.daily = daily
        self.discord_reference = discord_reference
        self.title = None
        self.runes = ["Stiya", "Lana", "Kviz", "Sul", "Tuax", "Yol",
        "Min", "Thark", "Set", "Ged", "Dorn", "Lae"]
        if rune_scores == None:
            self.rune_scores = self.randomise_runes()
        else:
            self.rune_scores = rune_scores
        self.faction = faction
        self.HP = HP
        self.inventory = inventory
        self.status = status

    def get_id(self):
        return self.id

    def get_HP(self):
        return self.HP

    def set_HP(self, HP):
        self.HP = HP

    def get_inventory(self):
        return self.inventory

    def set_inventory(self, inventory):
        self.inventory = inventory

    def get_status(self):
        return self.status

    def set_status(self, status):
        self.status = status

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

    def get_faction(self):
        return self.faction

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
        if isinstance(self.rune_scores, str):
            return ast.literal_eval(self.rune_scores)
        return self.rune_scores

    def increase_rune(self, rune, amount):
        if isinstance(self.rune_scores, str):
            self.rune_scores = ast.literal_eval(self.rune_scores)
        self.rune_scores[rune] += 1
