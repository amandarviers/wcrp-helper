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
            await ctx.send(f"Missing required information: `{command_guide}`")
            return
    
    @commands.group(name="pile", invoke_without_command=True)
    async def pile_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("WRONG")
    

    @pile_group.command(name="view")
    async def pile_view(self, ctx, group):
        try:
            with open(f"./data/piles/{group}.txt", "r") as file:
                lines = file.readlines()
                pile_contents = "".join(lines).replace("\n", " ")
            await ctx.send(f"Viewing {group} pile: {pile_contents}")
        except FileNotFoundError:
            await ctx.send(f"{group} is not a valid group")
    
    @pile_group.command(name="add")
    async def pile_add(self, ctx, group, item):
        with open(f"./data/piles/{group}.txt", "a") as file:
            file.write(f"{item}\n")
        await ctx.send(f"Adding {item} to {group} pile")
    
    @pile_group.command(name="take")
    async def pile_take(self, ctx, group, item):
        removed = False
        with open(f"./data/piles/{group}.txt", "r") as file:
            lines = file.readlines()
        with open(f"./data/piles/{group}.txt", "w") as file:
            for line in lines:
                if not removed and line.strip() == item:
                    removed = True
                    continue
                file.write(line)
        await ctx.send(f"Taking {item} from {group} pile")

async def setup(bot):
    await bot.add_cog(Pile(bot))