import pandas


def read_csv(location):
    data_base = []
    df = pandas.read_csv(location, index_col=0)
    for index, row in df.iterrows():
        data_base.append(row.to_dict())
    return data_base


locations = {"Players": "src/data/players"}
players = read_csv(locations["Players"])
print(players)
for player in players:
    print(player)