import discord
from discord.ext import commands

# <required arg>
# [optional arg]
command_guide = "!store <action> <clan> [item]"

class Store(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"store.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Missing required information: `{command_guide}`")
    
    @commands.group(name="store", invoke_without_command=True)
    async def store_group(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("WRONG")
    

    @store_group.command(name="view")
    async def store_view(self, ctx, clan):
        try:
            with open(f"./data/stores/{clan}.txt", "r") as file:
                lines = file.readlines()
                store_contents = "".join(lines).replace("\n", " ")
            await ctx.send(f"Viewing {clan} store: {store_contents}")
        except FileNotFoundError:
            await ctx.send(f"{clan} is not a valid clan/group")
    
    @store_group.command(name="add")
    async def stores_add(self, ctx, clan, item):
        with open(f"./data/stores/{clan}.txt", "a") as file:
            file.write(f"{item}\n")
        await ctx.send(f"Adding {item} to {clan} store")
    
    @store_group.command(name="take")
    async def stores_take(self, ctx, clan, item):
        removed = False
        with open(f"./data/stores/{clan}.txt", "r") as file:
            lines = file.readlines()
        with open(f"./data/stores/{clan}.txt", "w") as file:
            for line in lines:
                if not removed and line.strip() == item:
                    removed = True
                    continue
                file.write(line)
        await ctx.send(f"Taking {item} from {clan} store")

async def setup(bot):
    await bot.add_cog(Store(bot))