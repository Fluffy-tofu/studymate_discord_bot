import discord
from discord.ui import Button

from bot.utils.time_tracking import TimeTracker

time_tracking_data = {}


class TimeTrackerView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Start Tracking", style=discord.ButtonStyle.green)
    async def start_tracking(self, interaction: discord.Interaction, button: Button):
        await TimeTracker.start_tracking()

    @discord.ui.button(label="Stop Tracking", style=discord.ButtonStyle.red)
    async def stop_tracking(self, interaction: discord.Interaction, button: Button):
        await TimeTracker.start_tracking()