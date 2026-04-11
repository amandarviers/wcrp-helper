import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!help"

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"help.py is ready")

    @commands.command()
    async def help(self, ctx):
        help_embed = discord.Embed(title="Need Help From The Ancestors?", description="You stand in a clearing on a clear night, looking up at the glittering stars of Silverpelt. You exhale, then send a prayer to your ancestors for guidance.\n- - - - - - - -", color=discord.Color.random())
        help_embed.add_field(name="`!roll <dice>`", value="Used to roll dice. Must be in the format of '1d20'.", inline=False)
        help_embed.add_field(name="`!prey <area> <rank>`", value="Use when hunting to catch prey. Valid areas are thunder, river, wind, shadow, sky, or kinship. Valid ranks are warrior or apprentice.", inline=False)
        help_embed.add_field(name="`!pile <action> <group> [item]`", value="Use when interacting with the prey piles. Valid actions are view, add, or take. Valid groups are thunder, river, wind, shadow, sky, or kinship. Item is not needed when action is view.", inline=False)
        help_embed.add_field(name="`!herbs`", value="wip", inline=False)

        await ctx.send(embed = help_embed)

async def setup(bot):
    await bot.add_cog(Help(bot))