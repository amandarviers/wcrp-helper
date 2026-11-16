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
command_guide = "!herb <area> <attempts or herb>"

# load herb list
with open("./data/herbs_and_prey.json", "r") as f:
    herb_data = json.load(f)

# load valid areas
areas = list(herb_data.keys())

# load current season data
with open("./data/current_season.txt", "r") as season_file:
  current_season = (season_file.readlines()[0])
with open("./data/seasons.json", "r") as season_details_file:
  season_details = json.load(season_details_file)

class Herb(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"herb.py is ready")

  # missing required args
  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)
      return

  @commands.command()
  async def herb(self, ctx, area, attempt_or_herb):
    # normalize vars
    area = area.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "herb", area=area, attempt_or_herb=attempt_or_herb)
    # handle data errors
    if area not in areas:
      embed = error_embed(f"Invalid area. Choose from: { ', '.join(areas)}")
      await ctx.send(embed=embed)
      return

    # handle random searches
    if attempt_or_herb.isdigit():
      logger.info(f"{interaction_id} - attempt_or_herb is digit: {attempt_or_herb}")
      attempt_or_herb = int(attempt_or_herb)
      if attempt_or_herb > 5 or attempt_or_herb == 0:
        embed = error_embed(f"Attempts must be between 1 and 5")
        await ctx.send(embed=embed)
        return

      herbs_found = ""
      for _ in range(attempt_or_herb):
        herb = random.choice(herb_data[area]["herbs"])
        herbs_found += f"\n- {herb}"

      herb_embed = discord.Embed(title="Herb Finder", description=f"{herbs_found}", color=discord.Color.dark_green())
      herb_embed.set_footer(text=f"{ctx.author.display_name} made {attempt_or_herb} attempts to find herbs", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=herb_embed)
    else:
      logger.info(f"{interaction_id} - attempt_or_herb is herb: {attempt_or_herb}")
      # handle specific searches
      attempt_or_herb = attempt_or_herb.lower()

      if attempt_or_herb not in herb_data[area]["herbs"]:
          embed = error_embed(f"Invalid herb for {area}. Choose from: { ', '.join(herb_data[area]['herbs'])}")
          await ctx.send(embed=embed)
          return

      roll = random.randint(1, 20)
      logger.info(f"{interaction_id} - rolled {roll} when searching for {attempt_or_herb}")
      if roll >= 18:
        msg = f"You found 3 {attempt_or_herb} in the {area}!"
      elif roll >= 13:
        msg = f"You found 2 {attempt_or_herb} in the {area}!"
      elif roll >= 5:
        msg = f"You found 1 {attempt_or_herb} in the {area}!"
      else:
        msg = f"You found no {attempt_or_herb} in the {area}."

      herb_embed = discord.Embed(title="Herb Finder", description=f"{msg}", color=discord.Color.dark_green())
      herb_embed.set_footer(text=f"{ctx.author.display_name} looked for {attempt_or_herb} in {area}", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=herb_embed)

async def setup(bot):
  await bot.add_cog(Herb(bot))