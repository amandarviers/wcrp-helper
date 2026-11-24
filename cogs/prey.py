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
command_guide = "!prey <area> <skill> <attempts>"

# modifiers by skill
skills_dict = {
  "kit": -2,
  "novice": -1,
  "low": 0,
  "medium": 1,
  "high": 2,
  "expert": 3
}

# load prey data
with open("./data/herbs_and_prey.json", "r") as prey_file:
  data = json.load(prey_file)

# load area data
areas = list(data.keys())

# load current season data
with open("./data/current_season.txt", "r") as season_file:
  current_season = (season_file.readlines()[0])
with open("./data/seasons.json", "r") as season_details_file:
  season_details = json.load(season_details_file)

# determine success msg by roll
def calc_success(roll):
  if roll >= 19:
    return "perfect kill"
  elif roll >= 17:
    return "clean kill"
  elif roll >= 12:
    return "messy kill"
  elif roll >= 9:
    return "hit but no kill"
  elif roll >= 5:
    return "almost hit but no kill"
  else:
    return "miss"

# find prey candidates based on season scenarios and area
def find_prey(area): 
  candidates = []

  for animal, info in data[area]["prey"].items():
    if season_details[current_season]["hibernate"] and info["hibernate"]:
      weight = info["weight"] - 5 - season_details[current_season]["prey_weight_modifier"]
    else:
      weight = info["weight"] - season_details[current_season]["prey_weight_modifier"]
    candidates.extend([animal] * weight)

  modifier_float = len(candidates) * season_details[current_season]["prey_scarcity_modifier"]
  modifier = math.ceil(modifier_float)
  candidates.extend(["none"] * modifier)

  return candidates

class Prey(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"prey.py is ready")
  
  # missing required args
  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)

  @commands.command()
  async def prey(self, ctx, area, skill, attempts: int):
    # normalize vars
    area = area.lower()
    skill = skill.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "prey", area=area, skill=skill, attempts=attempts)
    # handle data errors
    if area not in areas:
      embed = error_embed(f"Invalid area. Choose from: { ', '.join(areas)}")
      await ctx.send(embed=embed)
      return
    if skill not in skills_dict:
      embed = error_embed(f"Invalid skill level. Choose from: { ', '.join(skills_dict)}")
      await ctx.send(embed=embed)
      return
    if attempts > 3 or attempts == 0:
      embed = error_embed(f"Attempts must be between 1 and 3")
      await ctx.send(embed=embed)
      return
    if skill == "kit" and area != "camp":
      embed = error_embed(f"Kits can only hunt in camp")
      await ctx.send(embed=embed)
      return

    success_message = ""
    candidates = find_prey(area)
    logger.info(f"{interaction_id} - {len(candidates)} prey candidates")
    for _ in range(attempts):
      base_roll = random.randint(1, 20)
      if base_roll == 1:
        msg = f"- Critical failure! Run `!encounter {area} neg-hunt` to see what happened."
        logger.info(f"{interaction_id} - rolled nat {base_roll}")
      elif base_roll == 20:
        msg = f"- Critical success! Run `!encounter {area} pos-hunt` to see what happened."
        logger.info(f"{interaction_id} - rolled nat {base_roll}")
      else:
        roll = base_roll + skills_dict[skill]
        logger.info(f"{interaction_id} - rolled {roll}")
        success_msg = calc_success(roll)
        prey = random.choice(candidates)
        if prey == "none":
          msg = "- Nothing found"
        else:
          msg = f"- {success_msg.capitalize()} on a {prey}"
      success_message += f"\n{msg}"

    prey_embed = discord.Embed(title="Prey Catcher", description=f"{success_message}", color=discord.Color.dark_purple())

    prey_embed.set_footer(text=f"{ctx.author.display_name} made {attempts} hunting attempts", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=prey_embed)

async def setup(bot):
  await bot.add_cog(Prey(bot))