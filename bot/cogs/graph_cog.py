import discord
from discord import app_commands
from discord.ext import commands
import io

from bot.utils.plot_single_function import plot_sympy_expression
from bot.embeds.single_graph_embed import single_graph_embed
from bot.views.graph_view import GraphFeaturesView


class GraphCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="graph", description="Graph a mathematical function")
    @app_commands.describe(
        expression="The mathematical expression to graph e.g. x^3 - cos(x) * e^3",
        xmin="Set the minimum x value for the plotted graph (default: -10)",
        xmax="Set the maximum x value for the plotted graph (default: 10)",
        ymin="Set the minimum y value for the plotted graph (optional)",
        ymax="Set the maximum y value for the plotted graph (optional)"
    )
    async def graph_command(
            self,
            interaction: discord.Interaction,
            expression: str,
            xmin: app_commands.Range[int, -1000, 1000] = -10,
            xmax: app_commands.Range[int, -1000, 1000] = 10,
            ymin: app_commands.Range[int, -1000, 1000] = -10,
            ymax: app_commands.Range[int, -1000, 1000] = 10
    ):
        await interaction.response.defer()

        result = plot_sympy_expression(expr_str=expression, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
        view = GraphFeaturesView()

        if 'error' in result:
            error_embed = discord.Embed(
                title="📉 Graphing Error",
                description=f"```{result['error']}```",
                color=discord.Color.red()
            )
            error_embed.set_footer(text="Please check your input and try again.")
            await interaction.followup.send(embed=error_embed, view=view)
        else:

            embed = single_graph_embed(expression=expression, result=result)

            image_file = discord.File(io.BytesIO(result['image'].getvalue()), filename="plot.png")

            await interaction.followup.send(file=image_file, embed=embed, view=view)


async def setup(bot):
    await bot.add_cog(GraphCog(bot))
