import discord
from discord.ext import commands
import random
import json

# <required arg>
# [optional arg]
command_guide = "!prey <area> <skill> <attempts>"
hibernate = False

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

def calc_success(skill):
    roll = (random.randint(1, 20)) + skills_dict[skill]

    if roll == 1:
        return "critical failure!"
    if roll == 20:
        return "critical success!"

    if roll >= 20:
        return "perfect kill"
    elif roll >= 17:
        return "clean kill"
    elif roll >= 11:
        return "messy kill"
    elif roll >= 8:
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
            continue
        weight = info["weight"]
        candidates.extend([animal] * weight)

    candidates.extend(["none"] * 3)

    return random.choice(candidates)

class Prey(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"prey.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed.description = f"Missing required information: `{command_guide}`"
            await ctx.send(embed=error_embed)


    @commands.command()
    async def prey(self, ctx, area, skill, attempts: int):
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
            success_msg = calc_success(skill)
            prey = find_prey(area)
            msg = f"{success_msg.capitalize()} on a {prey}"
            if prey == "none":
                msg = "Nothing found"
            success_message += f"\n{msg}"

        prey_embed = discord.Embed(title="Prey Catcher", description=f"{ctx.author.mention} ({attempts} attempts)\n{success_message}", color=discord.Color.dark_purple())

        await ctx.send(embed=prey_embed)

async def setup(bot):
    await bot.add_cog(Prey(bot))