import discord
from discord.ext import commands
import json
import random

# <required arg>
# [optional arg]
command_guide = "!encounter <area> <category>"

valid_categories = ["danger", "random", "vigil", "pos-hunt", "neg-hunt"]

with open("./data/prey_list_final.json", "r") as f:
    areadata = json.load(f)

areas = list(areadata.keys())

with open("./data/encounters.json", "r") as f:
    data = json.load(f)

error_embed = discord.Embed(title="<:error:1492739840230428829> Error", description="Error", color=discord.Color.red())

class Encounter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"encounter.py is ready")
    
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed.description = f"Missing required information: `{command_guide}`"
            await ctx.send(embed=error_embed)
            return
    
    @commands.command()
    async def encounter(self, ctx, area, category):
        if area not in areas:
            error_embed.description = f"Invalid area. Choose from: { ', '.join(areas)}"
            await ctx.send(embed=error_embed)
            return
        if category not in valid_categories:
            error_embed.description = f"Invalid category. Choose from: { ', '.join(valid_categories)}"
            await ctx.send(embed=error_embed)
            return
        if category == "vigil" and area != "camp": 
            error_embed.description = f"Vigils can only happen in camp."
            await ctx.send(embed=error_embed)
            return

        candidates = []
        roll = random.randint(1,20)

        if "hunt" in category or category == "danger":
            for candidate in data:
                if candidate["category"] != category:
                    continue
                if area not in candidate["habitat"]:
                    continue
                candidates.append(candidate)
        else:
            if roll > 5:
                for candidate in data:
                    if candidate["category"] != category:
                        continue
                    if area not in candidate["habitat"]:
                        continue
                    candidates.append(candidate)

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