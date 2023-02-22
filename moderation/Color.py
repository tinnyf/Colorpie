from discord.ext import commands
class Color(commands.Cog):

    def __init__(self, bot, role_id, channel_id, emoji_id):
        self.bot = bot
        self.role = role_id
        self.channel = channel_id
        self.emoji = emoji_id

    @commands.Cog.listener()
    async def on_ready(self):
        print("On ready in colour fired")
        self.guild = await self.bot.fetch_guild(695401740761301056)
        self.channel = self.guild.get_channel(self.channel)
        self.emoji = self.guild.get_emoji(self.emoji_id)
        self.role = self.guild.get_role(self.role_id)