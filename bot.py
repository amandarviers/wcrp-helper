import discord
from discord.ext import commands, tasks
from itertools import cycle
import os
import asyncio
from dotenv import load_dotenv
import logging

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

bot.remove_command("help")
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# status
with open("data/status_list.txt", "r") as f:
    bot_status = cycle([line.strip() for line in f])

@tasks.loop(minutes=5)
async def change_status():
    await bot.change_presence(activity=discord.Game(next(bot_status)))

@bot.event
async def on_ready():
    logging.info(f'Logged in as {bot.user.name}')
    if not change_status.is_running():
        change_status.start()

# load all cogs
async def load():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
            logging.info(f"{filename[:-3]} is loaded")

async def main():
    async with bot:
        await load()
        await bot.start(BOT_TOKEN)

asyncio.run(main())
