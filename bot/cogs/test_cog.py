import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.button_navigation.ui_index_embed import index_embed
from bot.views.button_navigation.ui_index_view import YesNoView


class TestCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test", description="index commands for studdsymate")
    async def test_command(self, interaction: discord.Interaction):
        view = YesNoView()
        embed = index_embed()
        await interaction.response.send_message(embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(TestCog(bot))

