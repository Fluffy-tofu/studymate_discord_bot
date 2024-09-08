import discord
import datetime
from datetime import datetime


def single_graph_embed(result, expression):
    embed = discord.Embed(
        title="📊 Function Graph",
        description=f"Graph of the function: `{expression}`",
        color=discord.Color.blue()
    )

    embed.add_field(name="X Range", value=f"`x ∈ [{result['xmin']}, {result['xmax']}]`", inline=True)
    if result['ymin'] is not None and result['ymax'] is not None:
        embed.add_field(name="Y Range", value=f"`y ∈ [{result['ymin']}, {result['ymax']}]`", inline=True)
    else:
        embed.add_field(name="Y Range", value="Auto-scaled", inline=True)

    embed.add_field(name="\u200b", value="\u200b", inline=True)

    embed.set_image(url="attachment://plot.png")

    embed.set_footer(text=f"Generated at {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}")

    return embed
