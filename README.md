# Rickus Bot 🤖

A custom Discord bot designed to enhance server interaction with various fun commands and automated role management. Features SCP Foundation article linking, automated role elevation, and various entertaining responses.

## Features

### Role Management
- **Automatic Role Elevation**: Members receive the ELEVATED role after 6 months
- **Bulk Role Processing**: Can process all server members at once
- **Notification System**: Announces newly elevated members
- **Persistence**: Tracks pending elevations across bot restarts

### SCP Foundation Integration
- **Article Linking**: Automatically detects and links SCP articles mentioned in designated channels
- **Random SCP**: Get a random SCP article with `rickus random`
- **Support for -J Articles**: Handles joke SCPs (e.g., SCP-420-J)
- **Smart Validation**: Validates SCP numbers and provides helpful feedback for out-of-bounds numbers
- **Channel Restriction**: Only responds in designated SCP channels

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
- `rickus notifyelevated` - Notify recently elevated members
- `rickus collectelevated` - Collect current elevated members for notification

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
├── bot.py # Main bot code
├── config.py # Configuration (not in repo)
├── config.template.py # Configuration template
├── responses.py # Command responses
├── scp_handler.py # SCP functionality
├── command_stats.py # Command tracking
├── elevated_users.json # Tracks elevated users
├── requirements.txt # Dependencies
├── Procfile # Deployment configuration
└── .gitignore # Git ignore rules
```