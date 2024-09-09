import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
APPLICATION_ID = os.getenv('APPLICATION_ID')


class StudyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents, application_id=APPLICATION_ID)

    async def setup_hook(self):
        # Load all cogs here
        await self.load_extension('bot.cogs.todo_cog')
        await self.load_extension('bot.cogs.test_cog')
        await self.load_extension('bot.cogs.study_cog')
        await self.load_extension('bot.cogs.graph_cog')
        await self.load_extension('bot.cogs.test2')
        await self.load_extension('bot.cogs.time_tracking_cog')

        # Sync commands globally
        await self.tree.sync()
        print(f'Synced application commands globally')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def start(self):
        await super().start(TOKEN)


bot = StudyBot()