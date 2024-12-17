import json
import os

STATS_FILE = 'unknown_commands.json'

def load_command_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_command_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f, indent=4)

def track_unknown_command(command):
    stats = load_command_stats()
    stats[command] = stats.get(command, 0) + 1
    save_command_stats(stats) 