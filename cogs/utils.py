import json
import os
from datetime import datetime
import pytz

def get_utc_now():
    """Get timezone-aware UTC datetime"""
    return datetime.now(pytz.UTC)

def load_json_file(filename, default=None):
    """Load data from a JSON file"""
    if default is None:
        default = {}
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            return json.load(f)
    return default

def save_json_file(filename, data):
    """Save data to a JSON file"""
    with open(filename, 'w') as f:
        json.dump(data, f)

def split_into_chunks(items, chunk_size):
    """Split a list into chunks of specified size"""
    return [items[i:i + chunk_size] for i in range(0, len(items), chunk_size)] 