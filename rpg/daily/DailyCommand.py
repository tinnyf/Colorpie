import random


class DailyCommand:
    def __init__(self, player_handler, daily_handler, datetime, author, logging_channel, now, reset_hour, tag=None):
        self.player_handler = player_handler
        self.daily_handler = daily_handler
        self.player_id = player_handler.get_player_id(author)
        self.author_name = author.name
        self.logging_channel = logging_channel
        self.player_id = self.player_handler.get_player_id(author)
        self.last_daily = player_handler.get_daily(self.player_id)
        self.now = now
        self.datetime = datetime
        self.reset_hour = reset_hour
        self.tag = tag.lower()

    def run(self):
        if self._daily_available() or self.player_id == 0:
            print(f"Daily_available {self._daily_available()}, {self.player_id}")
            self.player_handler.change_hp(self.player_id, random.randint(1, 4))
            if self.tag and self.tag.lower() in self.daily_handler.get_all_tags():
                try:
                    data = random.choice(list(x for x in self.daily_handler.get_dailys() if any(list(tag.lower() == self.tag.lower() for tag in x["tags"]))))
                except Exception as e:
                    print(e)
                print (f"Printing Data {data}!")
            else:
                data = self.daily_data()
            self.player_handler.set_relics(self.player_id,
                                           self.player_handler.get_relics(self.player_id) + int(data['relics']))

            messages = data['messages']
            new_messages, view = self.daily_handler.daily_extra(messages, self.player_id)
            data['messages'] += new_messages

            rune_message = self.player_handler.daily_runes(self.player_id)
            if rune_message:
                data['messages'].append(rune_message)
            return data, view
        else:
            return f"You're on cooldown for another {self._duration_until_next_reset()}", []

    def _daily_available(self) -> bool:
        return self._duration_from_last_daily_to_reset() > self.datetime.timedelta(days=1)

    def _duration_from_last_daily_to_reset(self):
        return self._find_next_reset_point() - self.last_daily

    def _duration_until_next_reset(self):
        return self._find_next_reset_point() - self.now

    def _find_next_reset_point(self):
        next_reset_point = self.now.replace(hour=self.reset_hour, minute=00, second=00)
        return next_reset_point if next_reset_point >= self.now else next_reset_point + self.datetime.timedelta(days=1)
