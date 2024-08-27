import discord


def study_embed():
    embed = discord.Embed(
        title="Study Response",
        description="You clicked the Study button!",
        color=discord.Color.blue()
    )
    return embed