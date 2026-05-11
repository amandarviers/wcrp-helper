import discord
from discord.ext import commands
import random
import json
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# <required arg>
# [optional arg]
command_guide = "!prey <area> <skill> <attempts>"
hibernate = False
global_modifier = 5
prey_scarcity = 15

error_embed = discord.Embed(title="<:error:1492739840230428829> Error", description="Error", color=discord.Color.red())

skills_dict = {
    "kit": -2,
    "novice": -1,
    "low": 0,
    "medium": 1,
    "high": 2,
    "expert": 3
}

with open("./data/prey_list_final.json", "r") as f:
    data = json.load(f)

areas = list(data.keys())

def calc_success(roll, area):
    if roll == 1:
        return f"Critical failure! Run `!encounter {area} neg-hunt` to see what happened."
    if roll == 20:
        return f"Critical success! Run `!encounter {area} pos-hunt` to see what happened."

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
    elif roll >= 2:
        return "miss"
    else:
        return "total miss"

def find_prey(area): 
    candidates = []

    for animal, info in data[area].items():
        if hibernate and info["hibernate"]:
            weight = info["weight"] - 5 - global_modifier
        else:
            weight = info["weight"] - global_modifier
        
        candidates.extend([animal] * weight)

    candidates.extend(["none"] * prey_scarcity)

    return random.choice(candidates)

class Prey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"prey.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed.description = f"Missing required information: `{command_guide}`"
            await ctx.send(embed=error_embed)


    @commands.command()
    async def prey(self, ctx, area, skill, attempts: int):
        logging.info(f"{ctx.author.display_name} used !prey {area} {skill} {attempts}")
        if area not in areas:
            error_embed.description = f"Invalid area. Choose from: { ', '.join(areas)}"
            await ctx.send(embed=error_embed)
            return
        if skill not in skills_dict:
            error_embed.description = f"Invalid skill level. Choose from: { ', '.join(skills_dict)}"
            await ctx.send(embed=error_embed)
            return
        if attempts > 3 or attempts == 0:
            error_embed.description = f"Attempts must be between 1 and 3"
            await ctx.send(embed=error_embed)
            return
        if skill == "kit" and area != "camp":
            error_embed.description = f"Kits can only hunt in camp"
            await ctx.send(embed=error_embed)
            return

        success_message = ""
        for _ in range(attempts):
            roll = (random.randint(1, 20)) + skills_dict[skill]
            success_msg = calc_success(roll, area)
            prey = find_prey(area)
            if roll == 1 or roll == 20:
                msg = f"- {success_msg}"
            elif prey == "none":
                msg = "- Nothing found"
            else:
                msg = f"- {success_msg.capitalize()} on a {prey}"
            success_message += f"\n{msg}"

        prey_embed = discord.Embed(title="Prey Catcher", description=f"{success_message}", color=discord.Color.dark_purple())

        prey_embed.set_footer(text=f"{ctx.author.display_name} made {attempts} hunting attempts", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=prey_embed)

async def setup(bot):
    await bot.add_cog(Prey(bot))