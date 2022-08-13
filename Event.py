import random

def generate_event(data):
    return Event(data)

class Event:
    def __init__(self, message, relics, options, random_event, tags):
        self.message = message
        self.relics = relics
        self.options = options
        self.random_event = random_event
        self.tags = tags

    def __str__(self) -> str:
        return self.message



for event in (generate_daily_event(data) for data in read_csv('daily.txt')):
    print(event)
    events.append(event)
