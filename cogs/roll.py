import discord
from discord.ext import commands
import random
import logging
import string

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# <required arg>
# [optional arg]
command_guide = "!roll <dice>"

error_embed = discord.Embed(title="<:error:1492739840230428829> Error", description="Error", color=discord.Color.red())

class Roll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"roll.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            logging.info(f"{ctx.author.display_name} used !roll but there was an error: {error}")
            error_embed.description = f"Missing required information: `{command_guide}`"
            await ctx.send(embed=error_embed)
            return

    @commands.command()
    async def roll(self, ctx, dice):
        alphabet = string.ascii_letters + string.digits
        interaction_id = ''.join(random.choices(alphabet, k=16))
        logging.info(f"{interaction_id} - {ctx.author.display_name} used !roll {dice}")
        dice_split = dice.split("d")
        number_of_dice = dice_split[0] or 1
        type_of_dice = dice_split[1]

        rolls = [random.randint(1, int(type_of_dice)) for _ in range(int(number_of_dice))]

        logging.info(f"{interaction_id} - {ctx.author.display_name} roll results: {rolls}")

        total = sum(rolls)

        
        roll_embed = discord.Embed(title="Dice Roller", description=f"<:d20:1492740388371304648> **Result:** {total}", color=discord.Color.blurple())
        roll_embed.set_footer(text=f"{ctx.author.display_name} rolled {dice}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=roll_embed)

async def setup(bot):
    await bot.add_cog(Roll(bot))