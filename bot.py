import discord
from discord.ext import commands
import os
import re
from command_stats import track_unknown_command
from responses import RESPONSES, HELP_TEXT

# Set up intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance
bot = commands.Bot(
    command_prefix='rickus ',
    intents=intents,
    case_insensitive=True,
)

# Override the default help command
bot.remove_command('help')

# Constants
SCP_CHANNELS = [759136825658310717, 1068738747417514064]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Load cogs
    await load_cogs()

async def load_cogs():
    """Load all cogs from the cogs directory"""
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and not filename.startswith('__'):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Loaded cog: {filename[:-3]}')
            except Exception as e:
                print(f'Failed to load cog {filename[:-3]}: {str(e)}')

@bot.event
async def on_message(message):
    # Don't respond to ourselves
    if message.author == bot.user:
        return

    # Process commands first
    await bot.process_commands(message)

    # Check for SCP mentions in appropriate channels
    if message.channel.id in SCP_CHANNELS:
        scp_handler = bot.get_cog('SCPHandler')
        if scp_handler:
            matches = scp_handler.scp_pattern.finditer(message.content)
            for match in matches:
                scp_number = match.group(1)
                await scp_handler.handle_scp_mention(message, scp_number)

    # Check for keyword responses
    lower_content = message.content.lower()
    for trigger, response in RESPONSES.items():
        if trigger in lower_content:
            await message.channel.send(response)
            return

@bot.command()
async def help(ctx):
    """Display help information"""
    await ctx.send(HELP_TEXT)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        command = ctx.message.content.split()[1]  # Get the attempted command
        track_unknown_command(command)
        await ctx.send(f"Sorry, I don't know that command. Type 'rickus help' for a list of available commands.")
    else:
        print(f"Error: {str(error)}")
        await ctx.send(f"An error occurred: {str(error)}")

def main():
    # Get token from environment variable
    token = os.getenv('TOKEN')
    if not token:
        raise ValueError("Bot token must be provided through environment variable TOKEN")
    
    # Run the bot
    bot.run(token)

if __name__ == "__main__":
    main() 