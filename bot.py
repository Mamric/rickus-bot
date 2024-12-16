import discord
from discord.ext import commands
from config import TOKEN

# Set up intents (required for newer versions of discord.py)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance with command prefix "rickus"
bot = commands.Bot(command_prefix='rickus ', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def hello(ctx):
    """Simple command to test if the bot is working"""
    await ctx.send(f'Hello {ctx.author.name}! I am Rickus, at your service!')

bot.run(TOKEN) 