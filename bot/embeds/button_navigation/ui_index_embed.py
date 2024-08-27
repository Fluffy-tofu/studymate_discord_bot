import discord


def index_embed():
    embed = discord.Embed(
        title="Study Bot",
        description="I aim to help you study and keep track of your studying habits!\n"
                    "What would you like to do today?",
        color=discord.Color.blue()
    )
    embed.add_field(name="Track your study time!",
                    value="Using the study bot you can track the daily time you study over a long period of time!",
                    inline=True)
    embed.add_field(name="Manage your todo list", value="The study bot allows you to add and view your todo items",
                    inline=False)

    return embed
