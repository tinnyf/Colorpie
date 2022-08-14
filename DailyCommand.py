class DailyCommand:
    def __init__(self, player_handler, daily_handler, dt, datetime):
        self.player_handler = player_handler
        self.daily_handler = daily_handler
        self.dt = dt
        self.datetime = datetime

    def run(self, author, guild):
        messages = []
        player_id = self.player_handler.get_player_id(author)
        check_time = self.dt.now()
        next_reset_time = self.dt.now()
        if check_time.hour < 19:
            check_time = check_time - self.datetime.timedelta(days=1)
        else:
            next_reset_time = next_reset_time + self.datetime.timedelta(days=1)
        check_time = check_time.replace(hour=19, minute=00)
        next_reset_time = next_reset_time.replace(hour=19, minute=00)
        if check_time >= self.player_handler.get_daily(player_id):
            amount, data = self.daily_handler.daily_data()
            self.player_handler.set_relics(player_id, self.player_handler.get_relics(player_id) + int(amount))
            self.player_handler.set_daily(player_id, self.dt.now())
            messages.append(f"{data}")

            for extra_message in self.daily_handler.daily_extra(data, player_id):
                messages.append(extra_message)

            message = self.player_handler.daily_runes(self.player_handler.get_player_id(author))
            if message:
                guild.get_member(842106129734696992).dm_channel.send(f"{author.name} has grown in power.")
                messages.append(message)
        else:
            messages.append(f"You're on cooldown for another {str(next_reset_time - self.dt.now())}")

        return messages

    def _daily_available(self, now, last_daily, reset_hour) -> bool:
        next_reset_point = now.replace(hour=reset_hour, minute=00, second=00)
        if next_reset_point < now:
            next_reset_point += self.datetime.timedelta(days=1)

        return next_reset_point - last_daily > self.datetime.timedelta(days=1)
