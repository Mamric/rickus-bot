# Rickus Bot 🤖

A custom Discord bot designed to enhance server interaction with various fun commands and automated role management. Features SCP Foundation article linking, automated role elevation, and various entertaining responses.

## Features

### Role Management
- **Automatic Role Elevation**: Members receive the ELEVATED role after 3 months
- **Persistent Tracking**: Maintains elevation schedule through bot restarts
- **Automatic Notifications**: Announces newly elevated members in designated channel
- **Color Selection**: Guides new ELEVATED members to color selection channel
- **Bulk Processing**: Can process all server members at once
- **Manual Scanning**: Can scan for recently joined members to ensure none are missed

### SCP Foundation Integration
- **Article Linking**: Automatically detects and links SCP articles mentioned in designated channels
- **Random SCP**: Get a random SCP article with `rickus random`
- **Support for Special Articles**: Handles both -J (joke) and -ARC (archived) SCPs
- **Smart Validation**: Validates SCP numbers and provides helpful feedback for out-of-bounds numbers
- **Channel Restriction**: Only responds in designated SCP channels
- **Link Formatting**: Prevents Discord embeds while maintaining clickable links

### Fun Commands
- `rickus hello` - Get a friendly greeting
- `rickus goodbye` - Say farewell
- `rickus dance` - Make Rickus bust a move
- `rickus fortnite` - Get Rickus' thoughts on Fortnite
- `rickus kill` - Watch Rickus avoid violence
- `rickus hawk` - Learn about the legendary Hawk Tuah
- `rickus fart` - Experience a mechanical malfunction
- `rickus goon` - See Rickus' tough side
- `rickus wyatt` - Learn about the creator
- `rickus love` - Make Rickus feel warm and fuzzy
- `rickus destroy` - Watch Rickus struggle with destructive programming
- `rickus juju` - Watch Rickus attempt the juju
- `rickus scooter` - Join the ankle safety campaign
- `rickus hack` - Access Rickus's core systems... if you dare

### Administrative Commands
- `rickus checkmembers` - Check and elevate eligible members
- `rickus scanrecent` - Scan for recently joined members
- `rickus notifyelevated` - Manually trigger notifications for elevated members
- `rickus collectelevated` - Collect current elevated members for notification

## Technical Features
- **Persistent Storage**: Uses JSON files to maintain data across restarts
  - `elevated_users.json`: Tracks elevated members
  - `pending_elevations.json`: Maintains elevation schedule
  - `unknown_commands.json`: Tracks attempted unknown commands
- **Hourly Checks**: Automatically checks for members due for elevation
- **Console Logging**: Detailed logging of all elevation activities
- **Error Handling**: Graceful handling of permissions and invalid commands
- **Command Tracking**: Tracks unknown command attempts to guide feature development
- **Modular Design**: Uses Discord.py's cog system for organized, maintainable code

## Setup

### Prerequisites
- Python 3.8 or higher
- Discord.py library
- pytz library

### Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/rickus-bot.git
cd rickus-bot
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a config.py file from the template:
```bash
cp config.template.py config.py
```

4. Update config.py with your:
- Bot token (from Discord Developer Portal)
- ELEVATED role ID (from your Discord server)

### Configuration Files
- `config.py`: Bot token and role IDs
- `responses.py`: Command responses and help text
- `scp_handler.py`: SCP functionality
- `command_stats.py`: Tracks unknown command attempts

### Running the Bot
```bash
python bot.py
```

## File Structure
```
rickus-bot/
├── bot.py              # Main bot code
├── cogs/              # Bot components
│   ├── fun_commands.py   # Entertainment commands
│   ├── notification_manager.py  # Notification handling
│   ├── role_manager.py  # Role elevation system
│   ├── scp_handler.py   # SCP functionality
│   └── utils.py         # Utility functions
├── config.py           # Configuration (not in repo)
├── config.template.py  # Configuration template
├── responses.py        # Command responses
├── command_stats.py    # Command tracking
├── requirements.txt    # Dependencies
├── Procfile           # Deployment configuration
└── .gitignore         # Git ignore rules
```

## Support
For support, feedback, or bug reports:
- Contact scpWyatt on Discord
- Submit an issue on GitHub
- The bot includes a feedback message in SCP-related responses

## License
[Your chosen license]