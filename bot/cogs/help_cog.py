import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get a quick overview of available commands")
    async def help(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Bot Commands Overview", color=discord.Color.blue())

        for cog in self.bot.cogs.values():
            cog_commands = cog.get_app_commands()
            if cog_commands:
                command_list = [f"/{cmd.name}" for cmd in cog_commands]
                embed.add_field(name=cog.__class__.__name__, value=", ".join(command_list), inline=False)

        embed.set_footer(text="Use /help all for detailed information on each command.")
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="help_all", description="Get detailed information about all available commands")
    async def help_all(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Detailed Bot Commands", color=discord.Color.green())

        for cog in self.bot.cogs.values():
            cog_commands = cog.get_app_commands()
            if cog_commands:
                command_list = []
                for cmd in cog_commands:
                    command_info = self.get_command_info(cmd)
                    command_list.append(command_info)

                embed.add_field(name=cog.__class__.__name__, value="\n\n".join(command_list), inline=False)

        await interaction.response.send_message(embed=embed)

    def get_command_info(self, cmd):
        if isinstance(cmd, app_commands.Group):
            return self.get_group_info(cmd)
        else:
            return self.get_regular_command_info(cmd)

    def get_group_info(self, group):
        group_info = f"/{group.name}: {group.description}"
        subcommands = [self.get_regular_command_info(subcmd, is_subcommand=True) for subcmd in group.commands]
        group_info += f"\n  Subcommands:\n" + "\n".join(subcommands)
        return group_info

    def get_regular_command_info(self, cmd, is_subcommand=False):
        prefix = "  " if is_subcommand else "/"
        command_info = f"{prefix}{cmd.name}: {cmd.description}"

        if cmd.parameters:
            params = [f"{param.name}: {param.description}" for param in cmd.parameters]
            command_info += f"\n    Parameters:\n      " + "\n      ".join(params)

        return command_info

async def setup(bot):
    await bot.add_cog(HelpCog(bot))