import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!herbs"

class Herbs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"herbs.py is ready")
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required information: `{command_guide}`")

    @commands.command()
    async def herbs(self, ctx):
        await ctx.send("wip")

async def setup(bot):
    await bot.add_cog(Herbs(bot))