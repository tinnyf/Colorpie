import pickle

from rpg.rp.character import Character
from rpg.rp.location import Location


class RpData():

    def __init__(self):
        self.locations = []
        self.players = []
        self.file_locations = {
        "Locations": "src/data/locations",
        "Characters": "src/data/character"
            }
        self.location_repo = self.read_csv("Locations")
        try:
            self.character_repo = self.read_csv("Characters")
            try:
                for character in self.character_repo:
                    self.characters.append(Character(**character))
            except Exception as e:
                print(e)
        except FileNotFoundError as e:
            print(f"Error in RpData: {e}")

    def read_csv(self, location):
        data_base = []
        df = pandas.read_csv(self.file_locations[location], index_col=0)
        for index, row in df.iterrows():
            data_base.append(row.to_dict())
        return data_base

    def save_csv(self, data, location):
        if not isinstance(data[1], dict):
            data = self.objects_to_dict(data)
        dataframe = pandas.DataFrame(data)
        csv = dataframe.to_csv(self.file_locations[location])

    def objects_to_dict(self, data):
        dehydrated_objects = []
        for object in data:
            dehydrated_objects.append(object.__dict__)
        return dehydrated_objects