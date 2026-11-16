import discord
from discord.ext import commands
import json
import random
import string
import logging

from util.logging_utils import log_command_usage
from util.error_utils import error_embed

# set up logger
logger = logging.getLogger(__name__)

# <required arg>
# [optional arg]
command_guide = "!herb <type> <area> <attempts or herb>"

# load herb list
with open("./data/herbs_and_prey.json", "r") as f:
    herb_data = json.load(f)

# load valid areas
areas = list(herb_data.keys())

class Herb(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"herb.py is ready")
  
  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)
      return

  @commands.group(name="herb", invoke_without_command=True)
  async def herb_group(self, ctx):
    # get interaction info
    interaction_id = log_command_usage(ctx, "herb")
    if ctx.invoked_subcommand is None:
      embed = error_embed(f"Invalid command. `{command_guide}`")
      await ctx.send(embed=embed)

  @herb_group.command(name="random", aliases=["Random", "RANDOM"])
  async def herb_random(self, ctx, area:str, attempts:int):
    # normalize vars
    area = area.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "herb random", area=area, attempts=attempts)
    # handle data errors
    if area not in areas:
        embed = error_embed(f"Invalid area. Choose from: { ', '.join(areas)}")
        await ctx.send(embed=embed)
        return
    if attempts > 5 or attempts == 0:
        embed = error_embed(f"Attempts must be between 1 and 5")
        await ctx.send(embed=embed)
        return

    herbs_found = ""
    for _ in range(attempts):
        herb = random.choice(herb_data[area]["herbs"])
        herbs_found += f"\n- {herb}"

    herb_embed = discord.Embed(title="Herb Finder", description=f"{herbs_found}", color=discord.Color.dark_green())
    herb_embed.set_footer(text=f"{ctx.author.display_name} made {attempts} attempts to find herbs", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=herb_embed)

  @herb_group.command(name="specific", aliases=["Specific", "SPECIFIC"])
  async def herb_specific(self, ctx, area:str, herb:str):
    # normalize vars
    area = area.lower()
    herb = herb.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "herb specific", area=area, herb=herb)
    # handle data errors
    if area not in areas:
        embed = error_embed(f"Invalid area. Choose from: { ', '.join(areas)}")
        await ctx.send(embed=embed)
        return
    if herb not in herb_data[area]["herbs"]:
        embed = error_embed(f"Invalid herb for {area}. Choose from: { ', '.join(herb_data[area]['herbs'])}")
        await ctx.send(embed=embed)
        return

    roll = random.randint(1, 20)
    if roll >= 18:
      msg = f"You found 3 {herb} in the {area}!"
    elif roll >= 13:
      msg = f"You found 2 {herb} in the {area}!"
    elif roll >= 5:
      msg = f"You found 1 {herb} in the {area}!"
    else:
      msg = f"You found no {herb} in the {area}."

    herb_embed = discord.Embed(title="Herb Finder", description=f"{msg}", color=discord.Color.dark_green())
    herb_embed.set_footer(text=f"{ctx.author.display_name} looked for {herb} in {area}", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=herb_embed)


async def setup(bot):
  await bot.add_cog(Herb(bot))