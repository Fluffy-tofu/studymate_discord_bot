import discord


def math_embed():

    embed = discord.Embed(
                title="Math Practice",
                description="What topic would you like to practice?",
                colour=discord.Color.blue()
    )

    embed.set_thumbnail(url="https://cdn-icons-png.flaticon.com/512/746/746960.png")
    embed.set_footer(text="Use the buttons below to choose a topic!")

    return embed
