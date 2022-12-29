class Vote:
    def __init__(self, name, emoji_id, types):
        self.options = {}
        self.types = types
        self.name = name
        self.emoji_id = emoji_id

    def get_options(self):
        return self.options

    def get_types(self):
        return self.types

    def get_name(self):
        return self.name

    def get_emoji_id(self):
        return self.emoji_id

    def add_option(self, option, componentdict):
        self.options[option] = [0, componentdict, []]

    def get_components(self):
        componentdicts = []
        for option, value in self.options.items():
            print(option, value)
            componentdicts.append(value[1])
        return componentdicts

    def increment_option(self, option, amount):
        self.options[option][0] = self.options[option][0] + amount

    def add_player_to_option(self, option, playerID):
        try:
            self.options[option][2].append(playerID)
        except TypeError:
            p = self.options[option][2]
            self.options[option][2] = []
            self.options[option][2].append(playerID)
            self.options[option][2].append(p)

    def get_option_players(self, option):
        print(self.options.get(option))
        t = self.options.get(option)[2]
        if isinstance(t, int):
            self.options[option][2] = []
            self.options[option][2].append(playerID)
            self.options[option][2].append(t)
        return self.options.get(option)[2]


    def remove_option(self, option):
        del self.options[option]
