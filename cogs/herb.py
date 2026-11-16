import discord
from discord.ext import commands
import json
import random
import logging
import string

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# <required arg>
# [optional arg]
command_guide = "!herb <type> <area> [attempts/herb]"

# herb list
with open("./data/herbs_and_prey.json", "r") as f:
    data = json.load(f)

areas = list(data.keys())

error_embed = discord.Embed(title="<:error:1492739840230428829> Error", description="Error", color=discord.Color.red())

class Herb(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.Cog.listener()
  async def on_ready(self):
    logging.info(f"herb.py is ready")
  
  async def cog_command_error(self, ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
      error_embed.description = f"Missing required information: `{command_guide}`"
      await ctx.send(embed=error_embed)
      return

  @commands.group(name="herb", invoke_without_command=True)
  async def herb_group(self, ctx):
    alphabet = string.ascii_letters + string.digits
    interaction_id = ''.join(random.choices(alphabet, k=16))
    logging.info(f"{interaction_id} - {ctx.author.display_name} used !herb")
    if ctx.invoked_subcommand is None:
      error_embed.description = f"Invalid command. `{command_guide}`"
      await ctx.send(embed=error_embed)

  @herb_group.command(name="random", aliases=["rand", "Random", "Rand"])
  async def herb_random(self, ctx, area:str, attempts:int):
    area = area.lower()
    alphabet = string.ascii_letters + string.digits
    interaction_id = ''.join(random.choices(alphabet, k=16))
    logging.info(f"{interaction_id} - {ctx.author.display_name} used !herb random {area} {attempts}")
    if area not in areas:
        error_embed.description = f"Invalid area. Choose from: { ', '.join(areas)}"
        await ctx.send(embed=error_embed)
        return

    if attempts > 5 or attempts == 0:
        error_embed.description = f"Attempts must be between 1 and 5"
        await ctx.send(embed=error_embed)
        return
    herbs_found = ""
    for _ in range(attempts):
        herb = random.choice(data[area]["herbs"])
        herbs_found += f"\n- {herb}"

    herb_embed = discord.Embed(title="Herb Finder", description=f"{herbs_found}", color=discord.Color.dark_green())
    herb_embed.set_footer(text=f"{ctx.author.display_name} made {attempts} attempts to find herbs", icon_url=ctx.author.display_avatar.url)

    await ctx.send(embed=herb_embed)

  @herb_group.command(name="specific", aliases=["Specific"])
  async def herb_specific(self, ctx, area:str, herb:str):
    area = area.lower()
    herb = herb.lower()
    alphabet = string.ascii_letters + string.digits
    interaction_id = ''.join(random.choices(alphabet, k=16))
    logging.info(f"{interaction_id} - {ctx.author.display_name} used !herb specific {area} {herb}")
    if area not in areas:
        error_embed.description = f"Invalid area. Choose from: { ', '.join(areas)}"
        await ctx.send(embed=error_embed)
        return

    if herb not in data[area]["herbs"]:
        error_embed.description = f"Invalid herb for {area}. Choose from: { ', '.join(data[area]['herbs'])}"
        await ctx.send(embed=error_embed)
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