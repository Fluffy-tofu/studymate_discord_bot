from discord.ui import Modal, TextInput
import discord
from discord import TextStyle

from bot.utils.todo import delete_todo_from_db


class DeleteToDoModal(Modal, title="Delete ToDo"):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id

    delete_input = TextInput(label="Delete Todo Item", style=TextStyle.short,
                             placeholder="Enter the number of the todo item to delete")

    async def on_submit(self, interaction: discord.Interaction):

        num_todo_item = self.delete_input.value
        try:
            num_todo_item = int(num_todo_item)
            if delete_todo_from_db(num_todo_item, self.user_id):
                await interaction.response.send_message(f"Todo item {num_todo_item} has been deleted", ephemeral=False)
            else:
                await interaction.response.send_message(f"Invalid todo item number: {num_todo_item}", ephemeral=False)
        except ValueError:
            await interaction.response.send_message("Please enter a valid number", ephemeral=False)
