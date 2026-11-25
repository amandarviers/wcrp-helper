import discord
from discord.ext import commands
import json 
import logging

from util.logging_utils import log_command_usage
from util.error_utils import error_embed

# set up logger
logger = logging.getLogger(__name__)

# <required arg>
# [optional arg]
command_guide = "!season <action> <season>"

# load seasons data
with open("./data/current_season.txt", "r") as season_file:
  current_season = season_file.readline().strip()
with open("./data/seasons.json", "r") as season_details_file:
  season_details = json.load(season_details_file)
valid_seasons = list(season_details.keys())

actions = ["set", "view"]

class Season(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"season.py is ready")

  # missing required args
  async def cog_command_error(self, ctx, error):
    if isinstance(error.commands.MissingRequiredArgument):
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)
      return

  @commands.group(name="season", invoke_without_command=True)
  async def season_group(self, ctx):
    #get interaction info
    interaction_id = log_command_usage(ctx, "season")
    if ctx.invoked_subcommand is None:
      embed = error_embed(f"Invalid command. `{command_guide}`")
      await ctx.send(embed=embed)
      return

  @season_group.command(name="set", aliases=["Set", "SET"])
  async def season_set(self, ctx, season):
    global current_season

    # normalize vars
    season = season.lower()

    #get interaction info
    interaction_id = log_command_usage(ctx, "season set", season=season)

    if season not in valid_seasons:
      embed = error_embed(f"Invalid season. Choose from: { ', '.join(valid_seasons)}")
      await ctx.send(embed=embed)
      return

    with open(f"./data/current_season.txt", "w") as file:
      file.write(f"{season}")

    current_season = season
    for cog in ("prey", "herb"):
      try:
        await self.bot.reload_extension(f"cogs.{cog}")
        logger.info(f"{interaction_id} - cogs.{cog} reloaded")
      except commands.ExtensionError:
        logger.info(f"{interaction_id} - Failed to reload cogs.{cog}")
        embed = error_embed(f"Season changed but `cogs.{cog}` failed to reload. Check logs.")
        await ctx.send(embed=embed)
        return

    season_set_embed = discord.Embed(title=f"Season Changed", description=f"Season changed to: {season}", color=discord.Color.gold())

    season_set_embed.set_footer(text=f"{ctx.author.display_name} changed the current season", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=season_set_embed)

  @season_group.command(name="view", aliases=["View", "VIEW"])
  async def season_view(self, ctx, season):
    # normalize vars
    season = season.lower()

    #get interaction info
    interaction_id = log_command_usage(ctx, "season view", season=season)

    if season != "current":
      if season not in valid_seasons:
        embed = error_embed(f"Invalid season. Choose from: { ', '.join(valid_seasons)}")
        await ctx.send(embed=embed)
        return

      hibernate = season_details[season]["hibernate"]
      prey_weight = season_details[season]["prey_weight_modifier"]
      prey_scarcity = season_details[season]["prey_scarcity_modifier"]
      herb_modifier = season_details[season]["herb_modifier"]

      season_view_embed = discord.Embed(
        title=f"Season Details: {season.capitalize()}", 
        description=f"**Prey Hibernation:** {hibernate}\n**Prey Type Modifier:** {prey_weight}\n**Prey Scarcity Modifier:** {prey_scarcity}\n**Herb Modifier:** {herb_modifier}", 
        color=discord.Color.gold())

      season_view_embed.set_footer(text=f"{ctx.author.display_name} viewed {season} details", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=season_view_embed)
    else:
      season = current_season
      hibernate = season_details[season]["hibernate"]
      prey_weight = season_details[season]["prey_weight_modifier"]
      prey_scarcity = season_details[season]["prey_scarcity_modifier"]
      herb_modifier = season_details[season]["herb_modifier"]
      season_view_embed = discord.Embed(
        title=f"Current Season: {season.capitalize()}", 
        description=f"**Prey Hibernation:** {hibernate}\n**Prey Type Modifier:** {prey_weight}\n**Prey Scarcity Modifier:** {prey_scarcity}\n**Herb Modifier:** {herb_modifier}", 
        color=discord.Color.gold())
      
      season_view_embed.set_footer(text=f"{ctx.author.display_name} viewed {season} details", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=season_view_embed)

async def setup(bot):
  await bot.add_cog(Season(bot))