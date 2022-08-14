from DailyCommand import DailyCommand
import datetime


class MockPlayerHandler:
    def __init__(self, time):
        self.time = time

    def get_player_id(self, author):
        return 1

    def set_daily(self, player_id, time):
        pass

    def get_daily(self, player_id):
        return self.time

    def set_relics(self, player_id, relics):
        pass

    def get_relics(self, player_id):
        return 10

    def daily_runes(self, player_id):
        return 'RUNES'


class MockDailyHandler:
    def daily_data(self):
        return 20, 'DAILY'

    def daily_extra(self, data, player_id):
        return ['EXTRA']


class MockDT:
    def __init__(self, time):
        self.time = time

    def now(self):
        return self.time


class MockGuild:
    def get_member(self, guild_id):
        return MockMember()


class MockMember:
    def __init__(self):
        self.dm_channel = MockDMChannel()


class MockDMChannel:
    def send(self, message):
        pass


class MockAuthor:
    def __init__(self):
        self.name = 'AUTHOR'


command = DailyCommand(
    player_handler=MockPlayerHandler(datetime.datetime(2022, 8, 14, 14, 0, 0)),
    daily_handler=MockDailyHandler(),
    now=datetime.datetime(2022, 8, 14, 12, 0, 0),
    datetime=datetime
)

assert command._daily_available(
    last_daily=datetime.datetime(2022, 8, 14, 14, 0, 0),
    reset_hour=19
) is False

command = DailyCommand(
    player_handler=MockPlayerHandler(datetime.datetime(2022, 8, 14, 14, 0, 0)),
    daily_handler=MockDailyHandler(),
    now=datetime.datetime(2022, 8, 14, 12, 0, 0),
    datetime=datetime
)

assert command._daily_available(
    last_daily=datetime.datetime(2022, 8, 13, 14, 0, 0),
    reset_hour=19
) is True


command = DailyCommand(
    player_handler=MockPlayerHandler(datetime.datetime(2022, 8, 14, 14, 0, 0)),
    daily_handler=MockDailyHandler(),
    now=datetime.datetime(2022, 8, 14, 12, 0, 0),
    datetime=datetime
)

assert command._daily_available(
    last_daily=datetime.datetime(2022, 8, 13, 19, 0, 0),
    reset_hour=19
) is False

command = DailyCommand(
    player_handler=MockPlayerHandler(datetime.datetime(2022, 8, 14, 14, 0, 0)),
    daily_handler=MockDailyHandler(),
    now=datetime.datetime(2022, 8, 14, 12, 0, 0),
    datetime=datetime
)

assert command._daily_available(
    last_daily=datetime.datetime(2022, 8, 13, 19, 1, 0),
    reset_hour=19
) is False

command = DailyCommand(
    player_handler=MockPlayerHandler(datetime.datetime(2022, 8, 14, 14, 0, 0)),
    daily_handler=MockDailyHandler(),
    now=datetime.datetime(2022, 8, 14, 12, 0, 0),
    datetime=datetime
)

assert command._duration_until_next_reset(
    reset_hour=19
) == datetime.timedelta(hours=7, minutes=0)

assert command.run(MockAuthor(), MockGuild()) == ["You're on cooldown for another 7:00:00"]

command = DailyCommand(
    player_handler=MockPlayerHandler(datetime.datetime(2022, 8, 13, 14, 0, 0)),
    daily_handler=MockDailyHandler(),
    now=datetime.datetime(2022, 8, 14, 12, 0, 0),
    datetime=datetime
)
assert command.run(MockAuthor(), MockGuild()) == ['DAILY', 'EXTRA', 'RUNES']

