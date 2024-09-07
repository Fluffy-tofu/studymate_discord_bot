import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.display_todo_list import display_todo_list


class TodoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='todo', description="displays todo list")
    async def todo(self, interaction: discord.Interaction):
        await display_todo_list(interaction)


async def setup(bot):
    await bot.add_cog(TodoCog(bot))
