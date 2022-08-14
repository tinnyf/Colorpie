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


def tests():
    test_time_methods()


def test_time_methods():
    scenarios = {
        'Daily in the future': {
            'last_daily': datetime.datetime(2022, 8, 14, 14, 0, 0),
            'now': datetime.datetime(2022, 8, 14, 12, 0, 0),
            'expected': {
                '_daily_available': False,
                '_duration_until_next_reset': datetime.timedelta(hours=7),
                '_duration_from_last_daily_to_reset': datetime.timedelta(hours=5),
                'run': ["You're on cooldown for another 7:00:00"],
            },
        },
        'Last daily 1 minute before last reset time': {
            'last_daily': datetime.datetime(2022, 8, 13, 18, 59, 0),
            'now': datetime.datetime(2022, 8, 14, 12, 0, 0),
            'expected': {
                '_daily_available': True,
                '_duration_until_next_reset': datetime.timedelta(hours=7),
                '_duration_from_last_daily_to_reset': datetime.timedelta(days=1, minutes=1),
                'run': ['DAILY', 'EXTRA', 'RUNES'],
            },
        },
        'Daily at reset time yesterday': {
            'last_daily': datetime.datetime(2022, 8, 13, 19, 0, 0),
            'now': datetime.datetime(2022, 8, 14, 12, 0, 0),
            'expected': {
                '_daily_available': False,
                '_duration_until_next_reset': datetime.timedelta(hours=7),
                '_duration_from_last_daily_to_reset': datetime.timedelta(days=1),
                'run': ["You're on cooldown for another 7:00:00"],
            },
        },
    }
    for scenario, test_data in scenarios.items():
        command = DailyCommand(
            player_handler=MockPlayerHandler(test_data['last_daily']),
            daily_handler=MockDailyHandler(),
            now=test_data['now'],
            datetime=datetime
        )

        daily_available = command._daily_available(
            last_daily=test_data['last_daily'],
            reset_hour=19
        )
        assert daily_available is test_data['expected']['_daily_available'], daily_available

        duration_until_next_reset = command._duration_until_next_reset(reset_hour=19)
        assert duration_until_next_reset == test_data['expected']['_duration_until_next_reset'],\
            duration_until_next_reset

        duration_from_last_daily_to_reset = command._duration_from_last_daily_to_reset(
            last_daily=test_data['last_daily'],
            reset_hour=19
        )
        assert duration_from_last_daily_to_reset == test_data['expected']['_duration_from_last_daily_to_reset'],\
            duration_from_last_daily_to_reset

        messages = command.run(MockAuthor(), MockGuild())
        for message, expected_message in zip(messages, test_data['expected']['run']):
            assert message == expected_message,\
                f'Scenario "{scenario}" failed. Expected <{expected_message}> and got <{message}>'
