import discord

def error_embed(message: str) -> discord.Embed:
  return discord.Embed(
    title="<:error:1492739840230428829> Error",
    description=message,
    color=discord.Color.red()
  )