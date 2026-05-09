import discord
from discord.ext import commands
import json

# <required arg>
# [optional arg]
command_guide = "!help"

with open("./data/prey_list_final.json", "r") as pf:
    prey_data = json.load(pf)

prey_areas = list(prey_data.keys())

with open("./data/herbs.json", "r") as hf:
    herb_data = json.load(hf)

herb_areas = list(herb_data.keys())

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"help.py is ready")

    @commands.group(name="help", invoke_without_command=True)
    async def help_group(self, ctx):
        help_embed = discord.Embed(title="Need Help From The Ancestors?", description="You stand in a clearing on a clear night, looking up at the glittering stars of Silverpelt. You exhale, then send a prayer to your ancestors for guidance.\n<:twinkle:1492982993667756163> <:twinkle:1492982993667756163> <:twinkle:1492982993667756163>", color=discord.Color.dark_teal())
        help_embed.add_field(name="`!roll <dice>`", value="Use to roll dice.", inline=False)
        help_embed.add_field(name="`!prey <area> <skill> <attempts>`", value="Use when hunting to catch prey", inline=False)
        help_embed.add_field(name="`!pile <action> <group> [item]`", value="Use when interacting with the prey piles.", inline=False)
        help_embed.add_field(name="`!herb <area> <attempts>`", value="Use when searching for herbs", inline=False)
        help_embed.add_field(name="`!encounter <area> <type>`", value="Use to get a random encounter", inline=False)
        help_embed.set_footer(text="Use !help <command> for detailed assistance on any of these", icon_url=None)

        await ctx.send(embed = help_embed)
    
    @help_group.command(name="roll")
    async def help_roll(self, ctx):
        help_roll_embed = discord.Embed(title="How To: Roll", description="`!roll <dice>`", color=discord.Color.dark_teal())
        help_roll_embed.add_field(name="Dice", value="Must be in the format of '1d20', '2d5', etc. Will return the total of all dice rolled.", inline=False)

        await ctx.send(embed = help_roll_embed)
    
    @help_group.command(name="prey")
    async def help_prey(self, ctx):
        help_prey_embed = discord.Embed(title="How To: Prey Catcher", description="`!prey <area> <skill> <attempts>`", color=discord.Color.dark_teal())
        help_prey_embed.add_field(name="Area", value=f"Refers to the habitat. Valid areas are { ', '.join(prey_areas) }", inline=False)
        help_prey_embed.add_field(name="Skill", value="Adds a modifier to the roll based on skill. Valid skills are kit, novice, low, medium, high, and expert.", inline=False)
        help_prey_embed.add_field(name="Attempts", value="Will make the specified number of attempts to hunt and return all the results. Can only be a number between 1 and 3.", inline=False)

        await ctx.send(embed = help_prey_embed)

    @help_group.command(name="pile")
    async def help_pile(self, ctx):
        help_pile_embed = discord.Embed(title="How To: Prey Pile", description="`!pile <action> <group> [item]`", color=discord.Color.dark_teal())
        help_pile_embed.add_field(name="Action", value="How you want to interact with the pile. Valid actions are view, add, and take.", inline=False)
        help_pile_embed.add_field(name="Group", value="Which Clan/group's pile you want to use. Valid groups are thunder, river, wind, shadow, sky, and kinship.", inline=False)
        help_pile_embed.add_field(name="Item", value="The piece of prey you want to use. *Is not needed when action is view.*", inline=False)

        await ctx.send(embed = help_pile_embed)

    @help_group.command(name="herb")
    async def help_herb(self, ctx):
        help_herb_embed = discord.Embed(title="How To: Herb Finder", description="`!herb <area> <attempts>`", color=discord.Color.dark_teal())
        help_herb_embed.add_field(name="Area", value=f"Refers to the habitat. Valid areas are { ', '.join(herb_areas) }", inline=False)
        help_herb_embed.add_field(name="Attempts", value="Will make the specified number of attempts to hunt and return all the results. Can only be a number between 1 and 5.", inline=False)

        await ctx.send(embed = help_herb_embed)
    
    @help_group.command(name="encounter")
    async def help_encounter(self, ctx):
        help_encounter_embed = discord.Embed(title="How To: Encounters", description="`!encounter <area> <type>`", color=discord.Color.dark_teal())
        help_encounter_embed.add_field(name="Area", value=f"Refers to the habitat. Valid areas are { ', '.join(prey_areas) }", inline=False)
        help_encounter_embed.add_field(name="Type", value="Refers to the type of encounter. Valid types are danger (requires approval from Crew), random (could be positive, neutral, or negative events), vigil, pos-hunt (only for crit success on hunting), neg-hunt (only for crit fail on hunting)", inline=False)

        await ctx.send(embed = help_encounter_embed)

async def setup(bot):
    await bot.add_cog(Help(bot))