import discord
from datetime import datetime
from bot.embeds.todos_embed import todos_embed
from bot.embeds.todo_empty_embed import empty_todo_embed
from bot.views.delete_todo_view import DeleteToDoView
from bot.db.database import SessionLocal
from bot.db.models import User, Todo


async def display_todo_list(interaction: discord.Interaction):
    user_id = interaction.user.id
    username = interaction.user.name
    now = datetime.now()

    with SessionLocal() as db_session:
        # Query the User by discord_id
        user = db_session.query(User).filter_by(discord_id=str(user_id)).first()

        # Create the user in the database if they don't exist
        if not user:
            user = User(discord_id=str(user_id), username=username,
                        email='placeholder@test.com', password_hash='placeholder')
            db_session.add(user)
            db_session.flush()

        # Query the todos for the user from the database
        todos = db_session.query(Todo).filter_by(discord_user_id=user.discord_id).order_by(Todo.created_at.asc()).all()

    view = DeleteToDoView()

    # Check if any todos exist
    if todos:
        # You need to modify the todos_embed to work with your database Todos instead of CSV-based todos
        embed = todos_embed(todos)
    else:
        embed = empty_todo_embed()

    await interaction.response.send_message(embed=embed, view=view, ephemeral=False)
