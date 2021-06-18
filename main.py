import discord
import os
from discord.ext import commands
from keep_alive import keep_alive

client = commands.Bot(command_prefix = "t!", help_command=None)

@client.event
async def on_ready():
  await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='t!help'))

@client.command()
async def load(ctx, extension):
  client.load_extension(f"cogs.{extension}")

@client.command()
async def unload(ctx, extension):
  client.unload_extension(f"cogs.{extension}")

@client.command()
async def reload(ctx, extension):
  client.unload_extension(f"cogs.{extension}")
  client.load_extension(f"cogs.{extension}")

for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    client.load_extension(f"cogs.{filename[:-3]}")

if __name__ == "__main__":
  keep_alive()
  client.run(os.environ['enable_secret'])