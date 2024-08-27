import discord
from discord import app_commands
from discord.ext import commands

from bot.utils.todo import list_todos_from_csv
from bot.embeds.todos_embed import todos_embed
from bot.embeds.todo_empty_embed import empty_todo_embed
from bot.views.delete_todo_view import DeleteToDoView



class TodoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='todo', description="displays todo list")
    async def todo(self, interaction: discord.Interaction):

        user_id = str(interaction.user.id)

        todos = list_todos_from_csv(user_id)
        if todos:
            view = DeleteToDoView()
            await interaction.response.send_message(embed=todos_embed(todos), view=view)
        else:

            view = DeleteToDoView()
            await interaction.response.send_message(embed=empty_todo_embed(), view=view, ephemeral=False)


async def setup(bot):
    await bot.add_cog(TodoCog(bot))
