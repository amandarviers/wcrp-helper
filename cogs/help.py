import discord
from discord.ext import commands
import json
import random
import string
import logging

from util.logging_utils import log_command_usage
from util.error_utils import error_embed
from cogs.encounter import command_guide as encounter_command
from cogs.herb import command_guide as herb_command
from cogs.pile import command_guide as pile_command
from cogs.prey import command_guide as prey_command
from cogs.roll import command_guide as roll_command
from cogs.prey import skills_dict
from cogs.encounter import valid_categories

# set up logger
logger = logging.getLogger(__name__)

# <required arg>
# [optional arg]
command_guide = "!help [command]"

# load areas
with open("./data/herbs_and_prey.json", "r") as pf:
    data = json.load(pf)
areas = list(data.keys())

# format hunting skills
skills = list(skills_dict.keys())

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"help.py is ready")

  @commands.group(name="help", invoke_without_command=True)
  async def help_group(self, ctx):
    interaction_id = log_command_usage(ctx, "help")
    help_embed = discord.Embed(title="Need Help From The Ancestors?", description="You stand in a clearing on a clear night, looking up at the glittering stars of Silverpelt. You exhale, then send a prayer to your ancestors for guidance.\n<:twinkle:1492982993667756163> <:twinkle:1492982993667756163> <:twinkle:1492982993667756163>", color=discord.Color.dark_teal())
    help_embed.add_field(name=f"`{roll_command}`", value="Use to roll dice.", inline=False)
    help_embed.add_field(name=f"`{prey_command}`", value="Use when hunting to catch prey", inline=False)
    help_embed.add_field(name=f"`{pile_command}`", value="Use when interacting with the prey piles.", inline=False)
    help_embed.add_field(name=f"`{herb_command}`", value="Use when searching for herbs", inline=False)
    help_embed.add_field(name=f"`{encounter_command}`", value="Use to get a random encounter", inline=False)
    help_embed.set_footer(text=f"Use {command_guide} for detailed assistance on any of these", icon_url=None)

    await ctx.send(embed = help_embed)
  
  @help_group.command(name="roll", aliases=["Roll", "ROLL"])
  async def help_roll(self, ctx):
    interaction_id = log_command_usage(ctx, "help roll")
    help_roll_embed = discord.Embed(title="How To: Roll", description=f"`{roll_command}`", color=discord.Color.dark_teal())
    help_roll_embed.add_field(name="Dice", value="Must be in the format of '1d20', '2d5', etc. Will return the total of all dice rolled. Can include modifiers, i.e. '1d20+2'!", inline=False)

    await ctx.send(embed = help_roll_embed)
  
  @help_group.command(name="prey", aliases=["Prey", "PREY"])
  async def help_prey(self, ctx):
    interaction_id = log_command_usage(ctx, "help prey")
    help_prey_embed = discord.Embed(title="How To: Prey Catcher", description=f"`{prey_command}`", color=discord.Color.dark_teal())
    help_prey_embed.add_field(name="Area", value=f"Refers to the habitat. Valid areas are { ', '.join(areas) }", inline=False)
    help_prey_embed.add_field(name="Skill", value=f"Adds a modifier to the roll based on skill. Valid skills are { ', '.join(skills) }", inline=False)
    help_prey_embed.add_field(name="Attempts", value="Will make the specified number of attempts to hunt and return all the results. Can only be a number between 1 and 3.", inline=False)

    await ctx.send(embed = help_prey_embed)

  @help_group.command(name="pile", aliases=["Pile", "PILE"])
  async def help_pile(self, ctx):
    interaction_id = log_command_usage(ctx, "help pile")
    help_pile_embed = discord.Embed(title="How To: Prey Pile", description=f"`{pile_command}`", color=discord.Color.dark_teal())
    help_pile_embed.add_field(name="Action", value="How you want to interact with the pile. Valid actions are view, add, take, and empty.", inline=False)
    help_pile_embed.add_field(name="Group", value="Which Clan/group's pile you want to use. Valid groups are thunder, river, wind, shadow, sky, kinship", inline=False)
    help_pile_embed.add_field(name="Item or #", value="Stating an item allows you to interact with that item in the pile via adding or taking. Providing a number instead will remove that many of the oldest pieces from the pile. *Is not needed when action is view.*", inline=False)

    await ctx.send(embed = help_pile_embed)

  @help_group.command(name="herb", aliases=["Herb", "HERB"])
  async def help_herb(self, ctx):
    interaction_id = log_command_usage(ctx, "help herb")
    help_herb_embed = discord.Embed(title="How To: Herb Finder", description=f"`{herb_command}`", color=discord.Color.dark_teal())
    help_herb_embed.add_field(name="Area", value=f"Refers to the habitat. Valid areas are { ', '.join(areas) }", inline=False)
    help_herb_embed.add_field(name="Attempts or Herb", value="Providing a *number* will make the specified number of attempts to hunt and return all the results. Can only be a number between 1 and 5. Providing a *specific herb* will search for only that and return a finding of 0-3.", inline=False)

    await ctx.send(embed = help_herb_embed)

  @help_group.command(name="encounter", aliases=["Encounter", "ENCOUNTER"])
  async def help_encounter(self, ctx):
    interaction_id = log_command_usage(ctx, "help encounter")
    help_encounter_embed = discord.Embed(title="How To: Encounters", description=f"`{encounter_command}`", color=discord.Color.dark_teal())
    help_encounter_embed.add_field(name="Area", value=f"Refers to the habitat. Valid areas are { ', '.join(areas) }", inline=False)
    help_encounter_embed.add_field(name="Type", value=f"Refers to the type of encounter. Valid types are { ', '.join(valid_categories)}", inline=False)

    await ctx.send(embed = help_encounter_embed)

async def setup(bot):
  await bot.add_cog(Help(bot))