import discord
import datetime
from discord.ui import Button

time_tracking_data = {}


class TimeTrackerView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Start Tracking", style=discord.ButtonStyle.green)
    async def start_tracking(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id
        now = datetime.now()
        time_tracking_data[user_id] = {'start_time': now, 'end_time': None}
        await interaction.response.send_message(f"Started tracking time for {interaction.user.mention}!",
                                                ephemeral=True)

    @discord.ui.button(label="Stop Tracking", style=discord.ButtonStyle.red)
    async def stop_tracking(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id
        if user_id in time_tracking_data and time_tracking_data[user_id]['end_time'] is None:
            now = datetime.now()
            time_tracking_data[user_id]['end_time'] = now

            start_time = time_tracking_data[user_id]['start_time']
            end_time = time_tracking_data[user_id]['end_time']
            elapsed_time = end_time - start_time
            elapsed_hours, remainder = divmod(elapsed_time.total_seconds(), 3600)
            elapsed_minutes, elapsed_seconds = divmod(remainder, 60)

            embed = discord.Embed(
                title="Time Tracking Result",
                description=f"Your tracked session:\n"
                            f"**Start Time:** {start_time}\n"
                            f"**End Time:** {end_time}\n"
                            f"**Elapsed Time:** {int(elapsed_hours)} hours, {int(elapsed_minutes)} minutes, {int(elapsed_seconds)} seconds",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed, ephemeral=False)
        else:
            await interaction.response.send_message("You don't have an active tracking session.", ephemeral=False)
