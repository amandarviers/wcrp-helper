import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!prey <clan> <rank> "

class Prey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"prey.py is ready")
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required information: `{command_guide}`")

    @commands.command()
    async def prey(self, ctx, clan, rank):
        if clan == "thunder":
            await ctx.send(f'Hello there! ThunderClan, {rank}')
        elif clan == "river":
            await ctx.send(f'Hello there! RiverClan, {rank}')
        elif clan == "wind":
            await ctx.send(f'Hello there! WindClan, {rank}')
        elif clan == "shadow":
            await ctx.send(f'Hello there! ShadowClan, {rank}')
        elif clan == "sky":
            await ctx.send(f'Hello there! SkyClan, {rank}')
        else: 
            await ctx.send(f'Who are you? {clan}, {rank}')

async def setup(bot):
    await bot.add_cog(Prey(bot))