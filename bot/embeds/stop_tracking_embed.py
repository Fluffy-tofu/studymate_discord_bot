import discord


def stop_tracking_embed(start_time, end_time, elapsed_hours, elapsed_minutes, elapsed_seconds):
    embed = discord.Embed(
        title="Time Tracking Result",
        description=f"Your tracked session:\n"
                    f"**Start Time:** {start_time}\n"
                    f"**End Time:** {end_time}\n"
                    f"**Elapsed Time:** {int(elapsed_hours)} hours, {int(elapsed_minutes)} minutes, {int(elapsed_seconds)} seconds",
        color=discord.Color.green()
    )
    return embed
