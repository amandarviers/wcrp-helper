import discord
from discord.ext import commands
import json
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# <required arg>
# [optional arg]
command_guide = "!pile <action> <group> [item]"

with open("./data/prey_list_final.json", "r") as f:
    data = json.load(f)

error_embed = discord.Embed(title="<:error:1492739840230428829> Error", description="Error", color=discord.Color.red())

def get_file_contents(group):
    with open(f"./data/piles/{group}.txt", "r") as file:
            lines = file.readlines()
            pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "nothing"

    return pile_contents

class Pile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    @commands.Cog.listener()
    async def on_ready(self):
        logging.info(f"pile.py is ready")
    
    # missing required args
    async def cog_command_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            error_embed.description = f"Missing required information: `{command_guide}`"
            await ctx.send(embed=error_embed)
            return
    
    @commands.group(name="pile", invoke_without_command=True)
    async def pile_group(self, ctx):
        logging.info(f"{ctx.author.display_name} used !pile")
        if ctx.invoked_subcommand is None:
            error_embed.description = f"Invalid command. `{command_guide}`"
            await ctx.send(embed=error_embed)
    

    @pile_group.command(name="view")
    async def pile_view(self, ctx, group):
        logging.info(f"{ctx.author.display_name} used !pile view {group}")
        try:
            with open(f"./data/piles/{group}.txt", "r") as file:
                lines = file.readlines()
                pile_contents = "".join(lines).replace("\n", ", ")[:-2] or "Empty"

            pile_view_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"{pile_contents}", color=discord.Color.green())

            pile_view_embed.set_footer(text=f"{ctx.author.display_name} viewed the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

            await ctx.send(embed=pile_view_embed)
        except FileNotFoundError:
            error_embed.description = f"{group.capitalize()} is not a valid group."
            await ctx.send(embed=error_embed)
    
    @pile_group.command(name="add")
    async def pile_add(self, ctx, group, *, item:str):
        logging.info(f"{ctx.author.display_name} used !pile add {group} {item}")
        valid_item = False
        for _, animals in data.items():
            for animal in animals:
                if item == animal:
                    valid_item = True
                    break
            if valid_item:
                break

        if not valid_item: 
            error_embed.description = f"{item.capitalize()} is not a valid item"
            await ctx.send(embed=error_embed)
            return
        with open(f"./data/piles/{group}.txt", "a") as file:
            file.write(f"{item}\n")
        
        pile_contents = get_file_contents(group)

        pile_add_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"Pile now contains: {pile_contents}", color=discord.Color.green())

        pile_add_embed.set_footer(text=f"{ctx.author.display_name} added {item} to the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=pile_add_embed)
    
    @pile_group.command(name="take")
    async def pile_take(self, ctx, group, *, item:str):
        logging.info(f"{ctx.author.display_name} used !pile take {group} {item}")
        valid_item = False
        for _, animals in data.items():
            for animal in animals:
                if item == animal:
                    valid_item = True
                    break
            if valid_item:
                break

        if not valid_item: 
            error_embed.description = f"{item.capitalize()} is not a valid item"
            await ctx.send(embed=error_embed)
            return

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
        
        pile_contents = get_file_contents(group)
        
        pile_take_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"Pile now contains: {pile_contents}", color=discord.Color.green())
        pile_take_embed.set_footer(text=f"{ctx.author.display_name} took {item} from the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=pile_take_embed)

    @pile_group.command(name="empty")
    async def pile_empty(self, ctx, group):
        logging.info(f"{ctx.author.display_name} used !pile empty {group}")

        with open(f"./data/piles/{group}.txt", "w"):
            pass

        pile_contents = get_file_contents(group)
        
        pile_empty_embed = discord.Embed(title=f"{group.capitalize()} Prey Pile", description=f"Pile now contains: {pile_contents}", color=discord.Color.green())
        pile_empty_embed.set_footer(text=f"{ctx.author.display_name} emptied the {group.capitalize()} pile", icon_url=ctx.author.display_avatar.url)

        await ctx.send(embed=pile_empty_embed)

async def setup(bot):
    await bot.add_cog(Pile(bot))