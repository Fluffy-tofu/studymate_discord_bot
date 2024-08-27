import discord


def todos_embed(todos):
    embed = discord.Embed(
        title="📝 Your Todo List",
        description="Here's what you need to get done!",
        color=discord.Color.blue()
    )

    for i, todo in enumerate(todos):
        embed.add_field(
            name=f"**Task {i + 1}:**",
            value=f"🗒️ {todo}",
            inline=False
        )

        embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/8161/8161879.png")
        embed.set_footer(text="Use the buttons below to manage your tasks!")

    return embed
