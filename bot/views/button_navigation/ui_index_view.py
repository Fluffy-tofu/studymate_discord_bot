import discord
from discord.ui import Button

from bot.views.button_navigation.ui_time_tracker_view import TimeTrackerView
from bot.views.button_navigation.ui_math_topic_view import MathTopicView

from bot.embeds.button_navigation.ui_study_embed import study_embed
from bot.embeds.button_navigation.ui_math_embed import math_embed

from bot.utils.display_todo_list import display_todo_list


class YesNoView(discord.ui.View):
    def __init__(self):
        super().__init__()

    @discord.ui.button(label="Study", style=discord.ButtonStyle.blurple)
    async def study_button(self, interaction: discord.Interaction, button: Button):

        new_view = TimeTrackerView()
        await interaction.response.send_message(embed=study_embed(), view=new_view)

    @discord.ui.button(label="To do", style=discord.ButtonStyle.blurple)
    async def to_do_list(self, interaction: discord.Interaction, button: Button):
        await display_todo_list(interaction)

    @discord.ui.button(label="Math", style=discord.ButtonStyle.blurple)
    async def math_questions(self, interaction: discord.Interaction, button: Button):

        view = MathTopicView()
        await interaction.response.send_message(embed=math_embed(), view=view)
