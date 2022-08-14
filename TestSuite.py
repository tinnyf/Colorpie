from DailyCommand import DailyCommand
import datetime


class MockPlayerHandler:
    def get_player_id(self, author):
        return 1

    def get_daily(self, player_id):
        return MockDT().now()


class MockDailyHandler:
    def daily_data(self, player_id):
        return 2

    def daily_extra(self, player_id):
        return ['3']


class MockDT:
    def now(self):
        return datetime.datetime(2022, 8, 14, 12, 0, 0)


command = DailyCommand(MockPlayerHandler(), MockDailyHandler(), MockDT(), datetime)
assert command.run('AUTHOR', 'GUILD') == ["You're on cooldown for another 7:00:00"]
