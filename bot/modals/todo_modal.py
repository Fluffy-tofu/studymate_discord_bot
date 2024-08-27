from discord.ui import Modal, TextInput
import discord
from discord import TextStyle

from bot.utils.todo import add_todo_to_csv


class TodoModal(Modal, title="Add Todo"):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    todo_input = TextInput(label="Todo Item", style=TextStyle.short, placeholder="Enter your todo item here")

    async def on_submit(self, interaction: discord.Interaction):
        todo_item = self.todo_input.value
        add_todo_to_csv(todo_item, self.user_id)
        await interaction.response.send_message(f"Added todo: {todo_item}", ephemeral=False)
