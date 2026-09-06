import discord
from discord.ext import commands
import random
import logging
import string
import re

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

        dice_string = dice.replace(" ", "").lower()

        # Regex pattern: (number of dice)? d (number of sides) (modifier sign and value)?
        pattern = r"^(\d*)d(\d+)(?:([+-])(\d+))?$"
        match = re.match(pattern, dice_string)

        # Parse pieces of dice string; default to number of dice 1 if not specified
        num_dice_str, sides_str, mod_sign, mod_val_str = match.groups()
        num_dice = int(num_dice_str) if num_dice_str else 1
        sides = int(sides_str)
        modifier = 0
        if mod_sign and mod_val_str:
            modifier = int(mod_val_str) if mod_sign == "+" else -int(mod_val_str)

        # Perform Roll
        rolls = [random.randint(1, sides) for _ in range(num_dice)]
        dice_sum = sum(rolls)
        logging.info(f"{interaction_id} - {ctx.author.display_name} roll results: {rolls} (sum: {dice_sum}), modifier: {modifier}")
        total = dice_sum + modifier

        
        roll_embed = discord.Embed(title="Dice Roller", description=f"<:d20:1492740388371304648> **Result:** {total}", color=discord.Color.blurple())
        roll_embed.set_footer(text=f"{ctx.author.display_name} rolled {dice}", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=roll_embed)

async def setup(bot):
    await bot.add_cog(Roll(bot))