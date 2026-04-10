import discord
from discord.ext import commands
import random

# <required arg>
# [optional arg]
command_guide = "!roll <dice>"

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"roll.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required information: `{command_guide}`")

    @commands.command()
    async def roll(self, ctx, dice):
        dice_split = dice.split("d")
        number_of_dice = int(dice_split[0])
        type_of_dice = int(dice_split[1])

        rolls = [random.randint(1, type_of_dice) for _ in range(number_of_dice)]

        total = sum(rolls)

        await ctx.send(f"Total: {total}")

async def setup(bot):
    await bot.add_cog(Roll(bot))