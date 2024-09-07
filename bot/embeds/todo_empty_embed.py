import discord


def empty_todo_embed():

    empty_embed = discord.Embed(
        title="❌ No Todos Found!",
        description="Your todo list is currently empty. Add some tasks to get started!",
        color=discord.Color.red()
    )
    return empty_embed
