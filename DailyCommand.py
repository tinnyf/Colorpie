class DailyCommand:
    def __init__(self, player_handler, daily_handler, dt, datetime):
        self.player_handler = player_handler
        self.daily_handler = daily_handler
        self.dt = dt
        self.datetime = datetime

    def run(self, author, guild):
        player_id = self.player_handler.get_player_id(author)
        if self._daily_available(self.dt.now(), self.player_handler.get_daily(player_id), reset_hour=19):
            amount, data = self.daily_handler.daily_data()
            self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + int(amount))
            self.player_handler.set_daily(player_id, self.dt.now())

            messages = [f"{data}"]
            messages += self.daily_handler.daily_extra(data, player_id)

            rune_message = self.player_handler.daily_runes(self.player_handler.get_player_id(author))
            if rune_message:
                guild.get_member(842106129734696992).dm_channel.send(f"{author.name} has grown in power.")
                messages.append(rune_message)

            return messages
        else:
            return [f"You're on cooldown for another {self._duration_until_next_reset(self.dt.now(), reset_hour=19)}"]

    def _daily_available(self, now, last_daily, reset_hour) -> bool:
        return self._duration_from_last_daily_to_reset(now, last_daily, reset_hour) > self.datetime.timedelta(days=1)

    def _duration_from_last_daily_to_reset(self, now, last_daily, reset_hour):
        return self._find_next_reset_point(now, reset_hour) - last_daily

    def _duration_until_next_reset(self, now, reset_hour):
        return self._find_next_reset_point(now, reset_hour) - now

    def _find_next_reset_point(self, now, reset_hour):
        next_reset_point = now.replace(hour=reset_hour, minute=00, second=00)
        return next_reset_point if next_reset_point >= now else next_reset_point + self.datetime.timedelta(days=1)
