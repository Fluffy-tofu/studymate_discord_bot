import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')


class StudyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='!', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print(f'Synced application commands')

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')

    async def start(self):
        await super().start(TOKEN)


bot = StudyBot()
