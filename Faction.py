class Faction:
    def __init__(self, name, role_id):
        self.members = []
        self.emoji = None
        self.name = name
        self.titles = {
            "Founder" :
            ["all"],
            "Champion" :
            ["change_permissions",
            "invite_users",
            "visit_restricted",
            "set_taxes",
            "withdraw_relics",
            "buy_options",
            "create_titles"
            ],
            "Default" :
            [


            ]
        }
        self.description = "Description would go here"
        self.perks = []
        self.shop = {}
        self.locations = {} #"location": Channel_ID
        self.DEFAULT_EMOJI_ID = 948664629771509780
        self.faction_id = None
        self.role_id = role_id

    def get_emoji(self):
        if self.emoji == None:
            return self.DEFAULT_EMOJI_ID
        return self.emoji

    def set_shop_items(self, items): #items should be dict
        self.shop = items

    def get_role_id(self):
        return self.role_id

    def add_shop_item(self, item, values): #k. v
        self.shop[item] = values

    def get_name(self):
        return self.name

    def set_faction_id(self, faction_id):
        self.faction_id = faction_id

    def get_description(self):
        return self.description

    def get_perks(self):
        return self.perks

    def get_titles(self):
        return self.titles

    def get_permissions(self, title):
        return(self.titles[title])

    def get_members(self):
        return self.members

    def add_member(self, memberid):
        members.append(memberid)

    def add_permission(self, role, permission):
        self.titles[role].append(permission)

    def remove_permission(self, role, permission):
        self.titles[role].pop(permission)

    def add_title(self):
        self.titles[role][title] = []

    def add_location(self, location, channel_id):
        self.locations[location] = channel_id

    def set_emoji(self, emoji_id):
        self.emoji = emoji_id

    def add_perk(self, perk):
        self.perks.append(perk)

    def remove_perk(self, perk):
        self.perks.remove(perk)

    def set_name(self, name):
        self.name = name
