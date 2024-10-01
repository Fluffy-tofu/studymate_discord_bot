import discord
from datetime import datetime, timezone


def todos_embed(todos):
    try:
        embed = discord.Embed(
            title="📝 Your Todo List",
            description="Here's a summary of your tasks:",
            color=discord.Color.blue()
        )

        for i, todo in enumerate(todos, 1):
            # Ensure due_date is timezone-aware
            if todo.due_date.tzinfo is None:
                due_date = todo.due_date.replace(tzinfo=timezone.utc)
            else:
                due_date = todo.due_date

            # Calculate days left
            days_left = (due_date - datetime.now(timezone.utc)).days

            status_emoji = "🟢" if todo.status.lower() == "in progress" else "🔴" if todo.status.lower() == "not started" else "🟡"

            value = (
                f"{status_emoji} **{todo.title}**\n"
                f"└ Due: {due_date.strftime('%Y-%m-%d')} ({days_left} days left)"
            )

            if todo.description:
                value += f"\n  *{todo.description[:50]}{'...' if len(todo.description) > 50 else ''}*"

            embed.add_field(
                name=f"Task id: {todo.id}",
                value=value,
                inline=False
            )

        total_tasks = len(todos)
        completed_tasks = sum(1 for todo in todos if todo.status.lower() == "completed")

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/8161/8161879.png")
        embed.set_footer(
            text=f"Completed: {completed_tasks}/{total_tasks} | Use the buttons below to manage your tasks!")

        return embed
    except Exception as e:
        print(f"Error in todos_embed: {e}")
        return discord.Embed(title="Error", description="An error occurred while creating the todo list.",
                             color=discord.Color.red())
