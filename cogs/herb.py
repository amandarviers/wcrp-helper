import discord
from discord.ext import commands
import json
import random
import logging
import string

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# <required arg>
# [optional arg]
command_guide = "!herb <area> <attempts>"

with open("./data/herbs.json", "r") as f:
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

    @commands.command()
    async def herb(self, ctx, area, attempts: int):
        alphabet = string.ascii_letters + string.digits
        interaction_id = ''.join(random.choices(alphabet, k=16))
        logging.info(f"{interaction_id} - {ctx.author.display_name} used !herb {area} {attempts}")
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
            herb = random.choice(data[area])
            herbs_found += f"\n- {herb}"
        
        herb_embed = discord.Embed(title="Herb Finder", description=f"{herbs_found}", color=discord.Color.dark_green())
        herb_embed.set_footer(text=f"{ctx.author.display_name} made {attempts} attempts to find herbs", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=herb_embed)


async def setup(bot):
    await bot.add_cog(Herb(bot))