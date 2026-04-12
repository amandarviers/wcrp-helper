import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!herb"

class Herb(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"herb.py is ready")
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<:error:1492739840230428829> Missing required information: `{command_guide}`")
            return

    @commands.command()
    async def herb(self, ctx):
        await ctx.send("wip")

async def setup(bot):
    await bot.add_cog(Herb(bot))