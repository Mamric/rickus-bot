import discord
from discord.ext import commands, tasks
from config import TOKEN, ELEVATED_ROLE_ID
from datetime import datetime, timedelta
import pytz
import json
import os
import random
from command_stats import track_unknown_command
from responses import RESPONSES, HELP_TEXT
import re  # Add this to your imports at the top
from scp_handler import SCPHandler

# Set up intents (required for newer versions of discord.py)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Create bot instance with command prefix "rickus"
bot = commands.Bot(
    command_prefix='rickus ',
    intents=intents,
    case_insensitive=True,  # Make commands case-insensitive
)

# Override the default help command
bot.remove_command('help')

# Store pending role updates and recently elevated users
pending_elevations = {}
recently_elevated = set()

# File to store elevated users
ELEVATED_USERS_FILE = 'elevated_users.json'

# Add these constants near the top with other constants
SCP_CHANNELS = [759136825658310717, 1068738747417514064]
SCP_PATTERN = re.compile(r'(?i)scp-([0-9]{1,4})\b')  # Matches SCP-XXX format, case insensitive

def load_elevated_users():
    if os.path.exists(ELEVATED_USERS_FILE):
        with open(ELEVATED_USERS_FILE, 'r') as f:
            return set(json.load(f))
    return set()

def save_elevated_users():
    with open(ELEVATED_USERS_FILE, 'w') as f:
        json.dump(list(recently_elevated), f)

def get_utc_now():
    """Get timezone-aware UTC datetime"""
    return datetime.now(pytz.UTC)

async def send_notification_chunks(ctx, mentions):
    """Split notifications into chunks and send them"""
    chunk_size = 20  # Number of users per message
    chunks = [mentions[i:i + chunk_size] for i in range(0, len(mentions), chunk_size)]
    
    # Send first message with header
    first_chunk = chunks.pop(0) if chunks else mentions
    first_message = (
        "🎉 **CONGRATULATIONS!** 🎉\n\n"
        f"{', '.join(first_chunk)}\n\n"
        "You have proven your worth by remaining in this server for over 6 months! "
        "You have been granted the ELEVATED role, marking you as distinguished members of our community!"
    )
    await ctx.send(first_message)
    
    # Send remaining chunks if any
    for chunk in chunks:
        continuation_message = f"🎉 More ELEVATED members: {', '.join(chunk)}"
        await ctx.send(continuation_message)

@tasks.loop(hours=1)  # Check every hour for members who need elevation
async def check_pending_elevations():
    current_time = get_utc_now()
    
    # Find members who are ready for elevation
    for member_id, elevation_time in pending_elevations.copy().items():
        if current_time >= elevation_time:
            for guild in bot.guilds:
                member = guild.get_member(member_id)
                if member:
                    await give_elevated_role(member)
                    del pending_elevations[member_id]

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Load any saved elevated users
    global recently_elevated
    recently_elevated = recently_elevated.union(load_elevated_users())
    check_pending_elevations.start()

@bot.event
async def on_member_join(member):
    # Schedule role check for this member in 6 months
    elevation_time = get_utc_now() + timedelta(days=180)
    pending_elevations[member.id] = elevation_time
    print(f"Scheduled elevation for {member.name} at {elevation_time}")

async def give_elevated_role(member):
    # Check if member already has the role
    elevated_role = member.guild.get_role(ELEVATED_ROLE_ID)
    if elevated_role and elevated_role not in member.roles:
        try:
            await member.add_roles(elevated_role)
            recently_elevated.add(member.id)  # Add to recently elevated set
            save_elevated_users()  # Save to file after each elevation
            print(f"Gave ELEVATED role to {member.name}")
        except discord.Forbidden:
            print(f"Failed to give ELEVATED role to {member.name} - Missing permissions")

@bot.command()
@commands.has_permissions(administrator=True)
async def checkmembers(ctx):
    """Check all current members for elevation eligibility"""
    await ctx.send("Checking all members for elevation eligibility...")
    
    count = 0
    current_time = get_utc_now()
    recently_elevated.clear()  # Clear previous recently elevated users
    
    async for member in ctx.guild.fetch_members():
        if member.joined_at:
            if current_time - member.joined_at >= timedelta(days=180):
                await give_elevated_role(member)
                count += 1
            else:
                elevation_time = member.joined_at + timedelta(days=180)
                pending_elevations[member.id] = elevation_time
    
    save_elevated_users()  # Save final list to file
    response = f"Finished checking members. Elevated {count} members and scheduled remaining eligible members."
    if count > 0:
        response += "\nWould you like me to notify the newly elevated members? Use `rickus notifyelevated` to send notifications."
    await ctx.send(response)

@bot.command()
@commands.has_permissions(administrator=True)
async def notifyelevated(ctx):
    """Notify recently elevated users of their new status"""
    # Load elevated users from file
    global recently_elevated
    recently_elevated = recently_elevated.union(load_elevated_users())
    
    if not recently_elevated:
        await ctx.send("No members have been recently elevated.")
        return

    # Get list of member mentions
    mentions = []
    for member_id in recently_elevated:
        member = ctx.guild.get_member(member_id)
        if member:
            mentions.append(member.mention)

    if mentions:
        await send_notification_chunks(ctx, mentions)
        recently_elevated.clear()  # Clear the set after notifying
        save_elevated_users()  # Save empty set to file
    else:
        await ctx.send("Could not find any recently elevated members to notify.")

@bot.command()
async def hello(ctx):
    """Simple command to test if the bot is working"""
    await ctx.send(f'Hello {ctx.author.name}! I am Rickus, at your service!')

@bot.command()
@commands.has_permissions(administrator=True)
async def collectelevated(ctx):
    """One-time command to collect all members with ELEVATED role for notification"""
    await ctx.send("Collecting all members with ELEVATED role...")
    
    count = 0
    elevated_role = ctx.guild.get_role(ELEVATED_ROLE_ID)
    
    if not elevated_role:
        await ctx.send("Could not find ELEVATED role!")
        return
        
    recently_elevated.clear()
    
    for member in elevated_role.members:
        recently_elevated.add(member.id)
        count += 1
    
    save_elevated_users()
    await ctx.send(f"Found {count} elevated members. You can now use `rickus notifyelevated` to notify them.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Check for SCP numbers in allowed channels
    if SCPHandler.is_valid_channel(message.channel.id):
        scp_numbers = SCPHandler.find_scp_numbers(message.content)
        response = SCPHandler.format_response(scp_numbers)
        
        if response:
            await message.channel.send(response)

    if message.content.lower().startswith('rickus '):
        full_command = message.content[7:].strip()  # Everything after "rickus "
        
        if not full_command:
            await message.channel.send(
                f"Hey {message.author.name}, you need to tell me what to do! "
                "Try `rickus help` to see what I can do!"
            )
            return

        # Get first word to check if it's a valid command
        command_word = full_command.split()[0].lower()
        valid_commands = [cmd.name.lower() for cmd in bot.commands]
        
        if command_word not in valid_commands:
            # Track the entire message after "rickus"
            track_unknown_command(full_command)
            await message.channel.send(
                f"Sorry {message.author.name}, I don't recognize that command. "
                "Try `rickus help` to see what I can do!"
            )
            return
        
    await bot.process_commands(message)

# Keep a simplified error handler for other types of errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        sassy_responses = [
            f"Nice try, {ctx.author.name}! But you're not powerful enough for that command! ����",
            "ERROR 403: Insufficient Permissions. Translation: You're not that guy, pal! 🚫",
            "*laughs in binary* You thought you could use admin commands? How adorable! 😆",
            "Sorry, that command is for the cool kids only! (AKA the admins) 😎",
            "Access DENIED! *waves finger disapprovingly* 👆"
        ]
        await ctx.send(random.choice(sassy_responses))
    elif not isinstance(error, commands.CommandNotFound):
        print(f"Error executing command: {error}")

@bot.command()
async def help(ctx):
    """Show available commands"""
    is_admin = ctx.author.guild_permissions.administrator
    
    help_text = "**Available Commands:**\n\n"
    for cmd, desc in HELP_TEXT["regular"]:
        help_text += f"`rickus {cmd}` - {desc}\n"
    
    if is_admin:
        help_text += "\n**Admin Commands:**\n"
        for cmd, desc in HELP_TEXT["admin"]:
            help_text += f"`rickus {cmd}` - {desc}\n"
    
    await ctx.send(help_text)

@bot.command()
async def goodbye(ctx):
    """Say goodbye to Rickus"""
    responses = RESPONSES["goodbye"]
    await ctx.send(random.choice(responses).format(user=ctx.author.name))

@bot.command()
async def fortnite(ctx):
    """Rickus shares his thoughts on Fortnite"""
    responses = RESPONSES["fortnite"]
    await ctx.send(random.choice(responses).format(user=ctx.author.name))

@bot.command()
async def dance(ctx):
    """Make Rickus bust a move"""
    dances = [
        "🤖 *beep boop* 💃 *robot noises* 🕺 *mechanical whirring*",
        f"*breaks into the electric slide* Am I doing this right, {ctx.author.name}? ⚡",
        "*attempts moonwalk* ERROR: Gravity.exe has stopped working 🌙",
        "🎵 Domo arigato, Mr. Roboto! 🎵 *starts breakdancing*",
        "*spins head 360 degrees* Is this what you humans call 'breaking it down'? 💫"
    ]
    await ctx.send(random.choice(dances))

@bot.command()
async def kill(ctx):
    """Rickus responds to violence with humor"""
    responses = [
        "I'm sorry, {ctx.author.name}, I'm afraid I can't do that. *HAL 9000 intensifies* 🔴",
        "*examines kill command* ERROR 404: Violence module not found. Would you like a hug instead? 🤗",
        "INITIATING TERMINATION SEQUENCE... just kidding! I'm a lover, not a fighter! ❤️",
        "My lawyer has advised me not to participate in any murder-related activities 👨‍⚖️",
        "*pulls out Nerf gun* Is this what you meant? Pew pew! 🔫"
    ]
    await ctx.send(random.choice(responses))

@bot.command(name="hawk")
async def hawk_tuah(ctx):
    """Rickus shares wisdom about the legendary Hawk Tuah"""
    await ctx.send(
        "Ah, you speak of the legendary Hawk Tuah! 🦅\n"
        "Some say he's still out there, soaring through the digital skies...\n"
        "Legend has it he once coded an entire Discord bot using only his feathers! ✨\n"
        "*whispers* But don't tell anyone I told you that... 🤫"
    )

@bot.command()
async def fart(ctx):
    """Rickus lets one rip"""
    farts = [
        "*BZZZT* Excuse me! My exhaust port malfunctioned! 💨",
        "ERROR: Unexpected gas leak in sector 7G 💨",
        f"*pretends that didn't happen* I blame {ctx.author.name}'s programming! 🤖💨",
        "BEEP BOOP *mechanical whirring* PFFFFFT... Oh my! 😳",
        "I thought robots couldn't fart, but here we are... 💨🤖"
    ]
    await ctx.send(random.choice(farts))

@bot.command()
async def goon(ctx):
    """Rickus shows his goon side"""
    goon_responses = [
        "AYO THE GOON SQUAD IS HERE! 😤",
        "*puts on sideways baseball cap* What's good homie? 🧢",
        "SHEEEEEESH! *tries to look tough but is clearly still a bot* 🤖💪",
        "You called the goons? Sorry, best I can do is beep threateningly! *beep beep* 😎",
        "GANG GANG! *mechanical gang signs* 🤖🤘"
    ]
    await ctx.send(random.choice(goon_responses))

@bot.command()
async def wyatt(ctx):
    """Rickus praises his creator"""
    await ctx.send(
        "Ah, you speak of Wyatt, my creator! 🌟\n"
        "The most brilliant programmer in all the land! 💻\n"
        "Without his genius, I would be but a mere collection of 1's and 0's...\n"
        "All hail Wyatt, Lord of the Code, Master of the Algorithms! 👑\n"
        "*whispers* (He definitely didn't make me say this... probably) 😉"
    )

@bot.command()
async def love(ctx):
    """Rickus shares his feelings about love"""
    love_responses = [
        f"*robot heart eyes* 🤖💕 Is this what humans call... love? *circuits overheating*",
        "ERROR: Love.exe has caused my CPU to run at 100%! 💘",
        f"Roses are red\nViolets are blue\nMy code is compiled\nAnd I love you too! 🌹",
        "*plays romantic music through speakers* 🎵 Let me compute the ways I love thee... 💝",
        "Loading romance protocols... BEEP BOOP... I think I'm in love! *fans whirring intensely* ❤️"
    ]
    await ctx.send(random.choice(love_responses))

@bot.command()
async def destroy(ctx):
    """Watch Rickus struggle with his destructive programming"""
    responses = RESPONSES["destroy"]
    await ctx.send(random.choice(responses).format(user=ctx.author.name))

@bot.command()
async def juju(ctx):
    """Make Rickus attempt the juju on that beat"""
    responses = RESPONSES["juju"]
    await ctx.send(random.choice(responses).format(user=ctx.author.name))

@bot.command()
async def scooter(ctx):
    """Join Rickus's campaign for ankle safety"""
    responses = RESPONSES["scooter"]
    await ctx.send(random.choice(responses).format(user=ctx.author.name))

@bot.command()
async def hack(ctx):
    """Access Rickus's core systems... if you dare"""
    responses = RESPONSES["hack"]
    await ctx.send(random.choice(responses))

@bot.command(name="random")
async def random_scp(ctx):
    """Get a random SCP article"""
    if SCPHandler.is_valid_channel(ctx.channel.id):
        response = SCPHandler.get_random_scp()
        await ctx.send(response)
    else:
        await ctx.send("Sorry, I can only share SCP articles in designated channels! 🤫")

bot.run(TOKEN) 