class Character:
    def __init__(self, user_id, name, player, background = None, faction = None, rune = None, url = None, active = True):
        self.user = user
        self.name = name
        self.player = player
        self.background = background
        self.faction = faction
        self.rune = rune
        self.url = url
        self.active = active

