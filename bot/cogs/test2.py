import discord
from discord import app_commands
from discord.ext import commands

from bot.embeds.button_navigation.ui_index_embed import index_embed
from bot.views.button_navigation.ui_index_view import YesNoView


class Test2Cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="test2", description="index commands for studdsymate")
    async def test_command(self, interaction: discord.Interaction):
        print('es')


async def setup(bot):
    await bot.add_cog(Test2Cog(bot))

