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
command_guide = "!pile <action> <group> [item or #]"

# load data
with open("./data/herbs_and_prey.json", "r") as f:
  data = json.load(f)

# load pile-specific data
def get_file_contents(group):
  with open(f"./data/piles/{group}.txt", "r") as file:
    lines = file.readlines()
    pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "nothing"
  return pile_contents

# determine if item is valid item
def is_valid_item(item:str) -> bool:
  item = item.lower().strip()

  for habitat in data.values():
    if not isinstance(habitat, dict):
      continue
    prey = habitat.get("prey", {})
    if isinstance(prey, dict):
      if item in prey.keys():
        if item.lower() == item:
          return True
  return False

class Pile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logger.info(f"pile.py is ready")
  
  # missing required args
  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      embed = error_embed(f"Missing required information: `{command_guide}`")
      await ctx.send(embed=embed)
      return
  
  @commands.group(name="pile", invoke_without_command=True)
  async def pile_group(self, ctx):
    # get interaction info
    interaction_id = log_command_usage(ctx, "pile")
    if ctx.invoked_subcommand is None:
      embed = error_embed(f"Invalid command. `{command_guide}`")
      await ctx.send(embed=embed)

  @pile_group.command(name="view", aliases=["View", "VIEW"])
  async def pile_view(self, ctx, group):
    # normalize vars
    group = group.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "pile view", group=group)

    try:
      with open(f"./data/piles/{group}.txt", "r") as file:
        lines = file.readlines()
        pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "Empty"

      pile_view_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"{pile_contents}", color=discord.Color.green())

      pile_view_embed.set_footer(text=f"{ctx.author.display_name} viewed the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=pile_view_embed)
    except FileNotFoundError:
      embed = error_embed(f"{group.capitalize()} is not a valid group.")
      await ctx.send(embed=embed)

  @pile_group.command(name="add", aliases=["Add", "ADD"])
  async def pile_add(self, ctx, group, *, item:str):
    # normalize vars
    group = group.lower()
    item = item.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "pile add", group=group, item=item)
    # validate item
    if not is_valid_item(item):
      embed = error_embed(f"{item.capitalize()} is not a valid item")
      await ctx.send(embed=embed)
      return

    # write new item
    with open(f"./data/piles/{group}.txt", "a") as file:
      file.write(f"{item}\n")

    # read contents
    pile_contents = get_file_contents(group)

    pile_add_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"Pile now contains: {pile_contents}", color=discord.Color.green())

    pile_add_embed.set_footer(text=f"{ctx.author.display_name} added {item} to the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=pile_add_embed)
  
  @pile_group.command(name="take", aliases=["Take", "TAKE"])
  async def pile_take(self, ctx, group, *, item):
    # normalize vars
    group = group.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "pile take", group=group, item=item)

    # handle bulk removals
    if item.isdigit():
      count = int(item)

      if count <= 0:
        embed = error_embed(f"Count must be a positive integer.")
        await ctx.send(embed=embed)
        return

      try:
        with open(f"./data/piles/{group}.txt", "r") as file:
          lines = file.readlines()
      except FileNotFoundError:
        embed = error_embed(f"{group.capitalize()} is not a valid group.")
        await ctx.send(embed=embed)
        return

      if count > len(lines):
        error_embed.description = f"Cannot take {count} items from the {group.capitalize()} pile. It only contains {len(lines)} items."
        await ctx.send(embed=error_embed)
        return

      if count >= len(lines):
        remaining_lines = []
      else: 
        remaining_lines = lines[count:]

      with open(f"./data/piles/{group}.txt", "w") as file:
        file.writelines(remaining_lines)

      pile_contents = get_file_contents(group)

      pile_take_embed = discord.Embed(
        title=f"{group.capitalize()} Prey Pile",
        description=f"Pile now contains: {pile_contents}",
        color=discord.Color.green()
      )
      pile_take_embed.set_footer(
        text=f"{ctx.author.display_name} took {count} items from the {group.capitalize()} pile",
        icon_url=ctx.author.display_avatar.url
      )

      await ctx.send(embed=pile_take_embed)
      return
    else:
      # normalize var
      item = item.lower()
      if not is_valid_item(item):
        embed = error_embed(f"{item.capitalize()} is not a valid item")
        await ctx.send(embed=embed)
        return

      removed = False
      with open(f"./data/piles/{group}.txt", "r") as file:
        lines = file.readlines()
      if item not in [line.strip() for line in lines]:
        await ctx.send(f"{item} not found in {group}.")
        return
      with open(f"./data/piles/{group}.txt", "w") as file:
        for line in lines:
          if not removed and line.strip() == item:
            removed = True
            continue
          file.write(line)
      
      pile_contents = get_file_contents(group)
      
      pile_take_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"Pile now contains: {pile_contents}", color=discord.Color.green())
      pile_take_embed.set_footer(text=f"{ctx.author.display_name} took {item} from the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

      await ctx.send(embed=pile_take_embed)

  @pile_group.command(name="empty", aliases=["Empty", "EMPTY"])
  async def pile_empty(self, ctx, group):
    # normalize vars
    group = group.lower()
    # get interaction info
    interaction_id = log_command_usage(ctx, "pile empty", group=group)

    with open(f"./data/piles/{group}.txt", "w"):
      pass

    pile_contents = get_file_contents(group)
    
    pile_empty_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"Pile now contains: {pile_contents}", color=discord.Color.green())
    pile_empty_embed.set_footer(text=f"{ctx.author.display_name} emptied the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=pile_empty_embed)

async def setup(bot):
  await bot.add_cog(Pile(bot))