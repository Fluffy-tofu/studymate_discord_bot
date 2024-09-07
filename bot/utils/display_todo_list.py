import discord

from bot.utils.todo import list_todos_from_csv
from bot.embeds.todos_embed import todos_embed
from bot.embeds.todo_empty_embed import empty_todo_embed
from bot.views.delete_todo_view import DeleteToDoView


async def display_todo_list(interaction: discord.Interaction):
    user_id = str(interaction.user.id)
    todos = list_todos_from_csv(user_id)
    view = DeleteToDoView()

    if todos:
        embed = todos_embed(todos)
    else:
        embed = empty_todo_embed()

    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
