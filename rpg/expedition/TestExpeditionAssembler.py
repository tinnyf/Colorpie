import asyncio

from rpg.expeditions import expedition
import ExpeditionFactory

players = ["Creevy", "Thomas", "Cara", "Ernie"]

class Response():

    async def send_message(**message):
        print(message)

    async def edit_message(**message):
        print(message)

class MockInteraction():

    def __init__(self):
        self.response = Response



async def startup():
    expedition_factory = ExpeditionFactory.ExpeditionFactory()
    print (expedition_factory)
    print (expedition_factory.expeditions)
    expeditions = [Expedition.Expedition(title = key, pages = expedition, players = players, host ="Creevy") for key, expedition in expedition_factory.expeditions.items()]
    for expedition in expeditions:
        print(expedition.pages)
    await tests(expeditions)

async def tests(expeditions):
    scenarios = {
        "Into Rahamida 0":
            {"Index": 0, "Buttons": [0], "expected_relics": 35},
    }
    for scenario, values in scenarios.items():
        expedition = expeditions[(values["Index"])]
        await expedition.run(MockInteraction())
        for button in values["Buttons"]:
            await expedition.active_page.buttons[button].callback(MockInteraction())
        assert values["expected_relics"]== expedition.rewards["relics"],\
        f'Test failed; Expected {values["expected_relics"]} and recieved {expedition.rewards["relics"]}'
        




asyncio.run(startup())
