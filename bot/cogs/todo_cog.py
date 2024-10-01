
import discord
from discord import app_commands
from discord.ext import commands
from datetime import datetime, timezone

from bot.utils.display_todo_list import display_todo_list
from bot.utils.todo import add_todo_to_db
from bot.utils.todo import update_todo_in_db


class TodoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    todo_group = app_commands.Group(name="todo", description="Manage your todo list")

    @todo_group.command(name='list', description="displays todo list")
    async def todo(self, interaction: discord.Interaction):
        await display_todo_list(interaction)

    @todo_group.command(name='add', description="Add a todo to the list")
    @app_commands.describe(
        title="Title of the todo item",
        description="Description of the todo item",
        due_date="Due date of the todo item (YYYY-MM-DD)"
    )
    async def add_todo(self, interaction: discord.Interaction,
                       title: app_commands.Range[str, 1, 100],
                       description: app_commands.Range[str, 10, 1000],
                       due_date: str
                       ):
        try:
            due_date_obj = datetime.strptime(due_date, "%Y-%m-%d")

            due_date_obj = due_date_obj.replace(tzinfo=timezone.utc)

            # Get the current time (timezone-aware)
            current_time = datetime.now(timezone.utc)

            # Check if the due date is in the future
            if due_date_obj <= current_time:
                await interaction.followup.send("Invalid Due Date! Due date must be in the future.")
                return

            add_todo_to_db(
                user_id=str(interaction.user.id),
                username=interaction.user.name,
                title=title,
                description=description,
                due_date=due_date_obj
            )

            await interaction.response.send_message(f"Added todo: {title}", ephemeral=False)
        except ValueError:
            await interaction.response.send_message("Invalid date format. Please use YYYY-MM-DD.", ephemeral=True)
        except Exception as e:
            print(f"Error adding todo: {e}")
            await interaction.response.send_message("An error occurred while adding the todo.", ephemeral=True)

    @todo_group.command(name='update', description="Update a todo item")
    @app_commands.describe(
        todo_id="ID of the todo item to update",
        title="New title of the todo item",
        description="New description of the todo item",
        due_date="New due date of the todo item (YYYY-MM-DD HH:MM:SS)",
        status="New status of the todo item"
    )
    async def update_todo_command(self, interaction: discord.Interaction,
                                  todo_id: int,
                                  title: app_commands.Range[str, 1, 100] = None,
                                  description: app_commands.Range[str, 10, 1000] = None,
                                  due_date: app_commands.Range[str, 1, 50] = None,
                                  status: app_commands.Range[str, 1, 50] = None):

        try:
            update_fields = {}
            if title:
                update_fields['title'] = title
            if description:
                update_fields['description'] = description
            if due_date:
                update_fields['due_date'] = due_date
            if status:
                update_fields['status'] = status

            print(update_fields)

            # Call the update_todo function
            updated_todo, message = update_todo_in_db(todo_id, **update_fields)
            print('ok and now?')

            if updated_todo:
                print('did it work?')
                await interaction.response.send_message(f"Todo updated!", ephemeral=False)
            else:
                await interaction.response.send_message(message, ephemeral=True)
        except Exception as e:
            print(e)




async def setup(bot):
    await bot.add_cog(TodoCog(bot))
