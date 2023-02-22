import discord

class Location():

    def __init__(self, location, channel):
        self.name = location
        self.on_create()
        self.channel = channel
        self.users = []
        self.characters = {}
        self.thread = None

    async def on_create(self):
        self.thread = await self.channel.create_thread(name=self.name)
        await self.thread.join()
        return self.thread

    async def add_user(self, user_id):
        self.users.append(user_id)
        self.thread.add_user(user)

    async def add_proxy(self, user, character):
        self.characters[user] = character

