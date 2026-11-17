import discord
from discord.ext import commands
import json
import random
import math
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
  current_season = season_file.readline().strip()
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
  async def herb(self, ctx, area, *args):
    # normalize vars
    area = area.lower()
    if not args:
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)
      return

    # get interaction info
    interaction_id = log_command_usage(ctx, "herb", area=area, args=" ".join(args))
    # handle data errors
    if area not in areas:
      embed = error_embed(f"Invalid area. Choose from: { ', '.join(areas)}")
      await ctx.send(embed=embed)
      return

    # handle random searches
    if args[0].isdigit():
      attempt_or_herb = int(args[0])
      logger.info(f"{interaction_id} - attempt_or_herb is digit: {attempt_or_herb}")
      if attempt_or_herb > 5 or attempt_or_herb == 0:
        embed = error_embed(f"Attempts must be between 1 and 5")
        await ctx.send(embed=embed)
        return

      # determine the candidates with the modifiers
      candidates = herb_data[area]["herbs"].copy()
      modifier_percentage = int(season_details[current_season]["herb_modifier"])/10
      modifier_float = len(candidates) * modifier_percentage
      modifier = math.ceil(modifier_float)
      candidates.extend(["none"] * modifier)

      logger.info(f"{interaction_id} - there are {len(candidates)} herb candidates")

      herbs_found = ""
      for _ in range(attempt_or_herb):
        herb = random.choice(candidates)
        if herb == "none":
          herbs_found += "\n- nothing found"
        else:
          herbs_found += f"\n- {herb}"

      herb_embed = discord.Embed(title="Herb Finder", description=f"{herbs_found}", color=discord.Color.dark_green())
      herb_embed.set_footer(text=f"{ctx.author.display_name} made {attempt_or_herb} attempts to find herbs", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=herb_embed)
    else:
      herb_name = " ".join(args).lower()
      logger.info(f"{interaction_id} - attempt_or_herb is herb: {herb_name}")
      # handle specific searches
      if herb_name not in herb_data[area]["herbs"]:
          embed = error_embed(f"Invalid herb for {area}. Choose from: { ', '.join(herb_data[area]['herbs'])}")
          await ctx.send(embed=embed)
          return

      roll = random.randint(1, 20)
      logger.info(f"{interaction_id} - rolled {roll} when searching for {herb_name}")
      if roll >= 19:
        msg = f"You found 3 {herb_name} in the {area}!"
      elif roll >= 14:
        msg = f"You found 2 {herb_name} in the {area}!"
      elif roll >= 8:
        msg = f"You found 1 {herb_name} in the {area}!"
      else:
        msg = f"You found no {herb_name} in the {area}."

      herb_embed = discord.Embed(title="Herb Finder", description=f"{msg}", color=discord.Color.dark_green())
      herb_embed.set_footer(text=f"{ctx.author.display_name} looked for {herb_name} in {area}", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=herb_embed)

async def setup(bot):
  await bot.add_cog(Herb(bot))