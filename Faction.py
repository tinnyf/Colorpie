class Faction:
    def __init__(self, name):
        self.members = []
        self.emoji = None
        self.name = name
        self.titles = {}
        self.description = "Description would go here"
        self.perks = []
        self.DEFAULT_EMOJI_ID = 948664629771509780
        self.faction_id = None

    def get_emoji(self):
        if self.emoji == None:
            return self.DEFAULT_EMOJI_ID
        return self.emoji

    def get_name(self):
        return self.name

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
