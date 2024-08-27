import discord
from discord import SelectOption
from discord.ui import Select


class MathTopicView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(self.topic_select())

    def topic_select(self):
        options = [
            SelectOption(label="Algebra", value="algebra"),
            SelectOption(label="Calculus", value="calculus"),
            SelectOption(label="Geometry", value="geometry")
        ]
        select = Select(placeholder="Choose a topic", options=options)
        select.callback = self.topic_callback
        return select

    async def topic_callback(self, interaction: discord.Interaction):
        topic = interaction.data["values"][0]
        view = MathSubtopicView(topic)
        await interaction.response.edit_message(content=f"You selected {topic}. Now choose a subtopic:", view=view)
