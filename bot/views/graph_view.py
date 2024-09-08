import discord
from discord.ui import Button

from bot.embeds.graph_features_embed import create_graph_function_showcase


class GraphFeaturesView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Math Functions & Formatting", style=discord.ButtonStyle.blurple)
    async def add_todo(self, interaction: discord.Interaction, button: Button):
        embed = create_graph_function_showcase()
        await interaction.response.send_message(embed=embed)
