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
command_guide = "!encounter <area> <type>"

# load valid areas
with open("./data/herbs_and_prey.json", "r") as f:
  area_data = json.load(f)

areas = list(area_data.keys())

# load encounter data
with open("./data/encounters.json", "r") as f:
  encounter_data = json.load(f)

# load valid categories
valid_categories = []
for encounter in encounter_data:
  if encounter["category"] not in valid_categories:
    valid_categories.append(encounter["category"])

class Encounter(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"encounter.py is ready")
  
  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)
      return
  
  @commands.command()
  async def encounter(self, ctx, area, category):
    # normalize vars
    area = area.lower()
    category = category.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "encounter", area=area, category=category)
    # handle data errors
    if area not in areas:
      embed = error_embed(f"Invalid area. Choose from: { ', '.join(areas)}")
      await ctx.send(embed=embed)
      return
    if category not in valid_categories:
      embed = error_embed(f"Invalid category. Choose from: { ', '.join(valid_categories)}")
      await ctx.send(embed=embed)
      return
    if category == "vigil" and area != "camp": 
      embed = error_embed(f"Vigils can only happen in camp.")
      await ctx.send(embed=embed)
      return

    candidates = []
    roll = random.randint(1,20)
    count = 0

    if "hunt" in category or category == "danger":
      for candidate in encounter_data:
        if candidate["category"] != category:
          continue
        if area not in candidate["habitat"]:
          continue
        candidates.append(candidate)
        count += 1
    else:
      if roll > 8:
        for candidate in encounter_data:
          if candidate["category"] != category:
            continue
          if area not in candidate["habitat"]:
            continue
          candidates.append(candidate)
          count += 1

    logger.info(f"{interaction_id} - {count} possible encounters for {area}")

    if candidates:
      encounter = random.choice(candidates)
      title = encounter["title"]
      description = encounter["description"]
    else:
      title = "Nothing happens"
      description = "It's an uneventful day."

    encounter_embed = discord.Embed(
      title=f"Random Encounter: {title}!", 
      description=f"{description}", 
      color=discord.Color.greyple())

    encounter_embed.set_footer(text=f"{ctx.author.display_name} rolled for a random encounter!", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=encounter_embed)

async def setup(bot):
  await bot.add_cog(Encounter(bot))