import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!prey <area> <rank> "

areas = [ "thunder", "river", "wind", "shadow", "sky", "kinship" ]

class Prey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"prey.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required information: `{command_guide}`")

    @commands.command()
    async def prey(self, ctx, area, rank):
        if area not in areas:
            await ctx.send(f"Invalid Clan. Choose from: { ', '.join(areas)}")
        
        await ctx.send(f"Hunting in {area} as {rank}")

async def setup(bot):
    await bot.add_cog(Prey(bot))