from Event import Event
import csv

class EventHandler(commands.Cog):

    def __init__(self, bot, playerhandler):
        self.file_locations = {
            "Events": "src/data/event"
            }
        events = []
        for event in (generate_daily_event(data) for data in read_csv('daily.txt')):
            print(event)
            events.append(event)

    def read_csv(file):
        with open(file, newline= '') as csvfile:
            readfile = csv.reader(csvfile, delimiter =' ', quotechar ='|')
            return readfile

    def save_csv(file, data):
        with open(file, 'w', newline ='') as csvfile:
            writefile = csv.writer(csvfile, delimiter =' ', quotechar ='|'m quoting = csv.QUOTE_MINIMAL)
            for item in data:
                writefile.writerow(item)
