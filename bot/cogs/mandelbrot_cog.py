import discord
from discord import app_commands
from discord.ext import commands
from bot.utils.mathematics.mandelbrot_fractal import MandelBrotSetUtils
import io


class MandelBrotCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="mandelbrot", description="Generate a mandelbrot set!")
    @app_commands.describe(
        width="Width of the mesh the mandelbrot set is drawn on",
        height="Height of the mesh the mandelbrot set is drawn on",
        max_iter="Number of iterations the mandelbrot set goes through"
    )
    async def mandelbrot_set(self,
                             interaction: discord.Interaction,
                             width: app_commands.Range[int, 10, 1000] = 600,
                             height: app_commands.Range[int, 10, 1000] = 800,
                             max_iter: app_commands.Range[int, 1, 100] = 50):

        await interaction.response.defer()
        mandelbrot_user = MandelBrotSetUtils.mandelbrot(width, height, max_iter)
        result = MandelBrotSetUtils.plot_mandelbrot(mandelbrot_user, "hot")

        if 'error' in result:
            error_embed = discord.Embed(
                title="📉 Graphing Error",
                description=f"```{result['error']}```",
                color=discord.Color.red()
            )
            error_embed.set_footer(text="Please check your input and try again.")
            print(result['error'])
            await interaction.followup.send(embed=error_embed)

        else:
            try:
                embed = discord.Embed(
                    title="Mandelbrot Set",
                    description=f"`Width: {width}`  `Height: {height}`  `Max Iterations: {max_iter}",
                    color=discord.Color.blue()
                )
                embed.set_image(url="attachment://mandelbrot.png")

                image_file = discord.File(io.BytesIO(result['img_buffer'].getvalue()), filename="mandelbrot.png")

                await interaction.followup.send(file=image_file, embed=embed)
            except Exception as e:
                print(f"Error: {e}")


async def setup(bot):
    await bot.add_cog(MandelBrotCog(bot))
