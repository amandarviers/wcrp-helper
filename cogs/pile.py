import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!pile <action> <group> [item]"

class Pile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"prey.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"<:error:1492739840230428829> Missing required information: `{command_guide}`")
            return
    
    @commands.group(name="pile", invoke_without_command=True)
    async def pile_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(f"<:error:1492739840230428829> Invalid command. `{command_guide}`")
    

    @pile_group.command(name="view")
    async def pile_view(self, ctx, group):
        try:
            with open(f"./data/piles/{group}.txt", "r") as file:
                lines = file.readlines()
                pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "Empty"

            pile_view_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"{pile_contents}", color=discord.Color.green())

            await ctx.send(embed=pile_view_embed)
        except FileNotFoundError:
            await ctx.send(f"{group} is not a valid group")
    
    @pile_group.command(name="add")
    async def pile_add(self, ctx, group, item):
        with open(f"./data/piles/{group}.txt", "a") as file:
            file.write(f"{item}\n")
        
        with open(f"./data/piles/{group}.txt", "r") as file:
                lines = file.readlines()
                pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "nothing"

        pile_add_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"{ctx.author.mention} added a {item} to the pile\nPile now contains {pile_contents}", color=discord.Color.green())

        await ctx.send(embed=pile_add_embed)
    
    @pile_group.command(name="take")
    async def pile_take(self, ctx, group, item):
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
        
        with open(f"./data/piles/{group}.txt", "r") as file:
                lines = file.readlines()
                pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "nothing"
        
        pile_take_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"{ctx.author.mention} took a {item} from the pile\nPile now contains {pile_contents}", color=discord.Color.green())

        await ctx.send(embed=pile_take_embed)

async def setup(bot):
    await bot.add_cog(Pile(bot))