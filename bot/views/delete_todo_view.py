import discord
from discord.ui import Button

from bot.modals.delete_todo_modal import DeleteToDoModal
from bot.modals.todo_modal import TodoModal


class DeleteToDoView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Add Todo", style=discord.ButtonStyle.blurple)
    async def add_todo(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id

        await interaction.response.send_modal(TodoModal(user_id))

    @discord.ui.button(label="Delete ToDo", style=discord.ButtonStyle.red)
    async def delete_todo(self, interaction: discord.Interaction, button: Button):
        user_id = interaction.user.id

        await interaction.response.send_modal(DeleteToDoModal(user_id))
