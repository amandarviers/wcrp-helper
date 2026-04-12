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
            await ctx.send(f"<:error:1492739840230428829> Missing required information: `{command_guide}`")
            return

    @commands.command()
    async def roll(self, ctx, dice):
        dice_split = dice.split("d")
        number_of_dice = int(dice_split[0])
        type_of_dice = int(dice_split[1])

        rolls = [random.randint(1, type_of_dice) for _ in range(number_of_dice)]

        total = sum(rolls)

        roll_embed = discord.Embed(title="Dice Roller", description=f"<:d20:1492740388371304648> {ctx.author.mention} rolled {dice}\n**Result:** {total}", color=discord.Color.blurple())

        await ctx.send(embed=roll_embed)

async def setup(bot):
    await bot.add_cog(Roll(bot))