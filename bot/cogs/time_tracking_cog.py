import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import button

from bot.utils.time_tracking import TimeTracker

GUILD_ID = 1270031183509590097


class TimeTrackingCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("TimeTrackingCog initialized")

    @app_commands.command(name="start_session", description="Start the timer for a study session")
    @app_commands.describe(
        subject="Add a subject for which you want to study",
    )
    async def start_session(self, interaction: discord.Interaction, subject: str):
        print("start_session command called")
        await TimeTracker.start_tracking(interaction, subject)

    @app_commands.command(name="stop_session", description="Stop the timer for a study session")
    async def stop_session(self, interaction: discord.Interaction):
        print("stop_session command called")
        await TimeTracker.stop_tracking(interaction)

async def setup(bot):
    await bot.add_cog(TimeTrackingCog(bot))
    print("TimeTrackingCog added to the bot")

