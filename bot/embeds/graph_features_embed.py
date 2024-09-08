import discord

def create_graph_function_showcase():
    embed = discord.Embed(
        title="📚 Graph Function Reference",
        description="Here's a guide to the mathematical functions and terms you can use with the /graph command:",
        color=discord.Color.blue()
    )

    embed.add_field(
        name="Basic Operations",
        value="• Addition: `+`\n• Subtraction: `-`\n• Multiplication: `*`\n• Division: `/`\n• Exponentiation: `^` or `**`",
        inline=False
    )

    embed.add_field(
        name="Trigonometric Functions",
        value="• Sine: `sin(x)`\n• Cosine: `cos(x)`\n• Tangent: `tan(x)`",
        inline=False
    )

    embed.add_field(
        name="Logarithmic and Exponential Functions",
        value="• Natural logarithm: `ln(x)` or `log(x)`\n• Base-10 logarithm: `log10(x)`\n• Exponential function: `e^x` or `exp(x)`",
        inline=False
    )

    embed.add_field(
        name="Other Functions",
        value="• Square root: `sqrt(x)`\n• Absolute value: `abs(x)`",
        inline=False
    )

    embed.add_field(
        name="Constants",
        value="• Pi: `π` or `pi`\n• Euler's number: `e`",
        inline=False
    )

    embed.add_field(
        name="Expression Examples",
        value="1. `x^2 + 2*x + 1`\n2. `sin(x) + cos(x)`\n3. `e^x - ln(x)`\n4. `sqrt(x^2 + 1)`",
        inline=False
    )

    embed.set_footer(text="Use these functions and terms to create your mathematical expressions for graphing! Example: sin(x) + log(x) - x^2")

    return embed

# Usage:
# embed = create_graph_function_showcase()
# await interaction.followup.send(embed=embed)
