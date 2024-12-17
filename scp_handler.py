import re
import random
from typing import Set, Optional

class SCPHandler:
    # Channels where SCP detection is enabled
    SCP_CHANNELS = [759136825658310717, 1068738747417514064]
    
    # Regex pattern for matching SCP numbers
    SCP_PATTERN = re.compile(r'(?i)scp-([0-9]{1,4})\b')
    
    # SCP number range
    MIN_SCP = 1
    MAX_SCP = 8000
    
    @classmethod
    def is_valid_channel(cls, channel_id: int) -> bool:
        """Check if channel is enabled for SCP detection"""
        return channel_id in cls.SCP_CHANNELS
    
    @classmethod
    def find_scp_numbers(cls, content: str) -> Set[str]:
        """Extract valid SCP numbers from message content"""
        matches = set(cls.SCP_PATTERN.findall(content))
        valid_matches = set()
        
        for scp_num in matches:
            num = int(scp_num)
            if cls.MIN_SCP <= num <= cls.MAX_SCP:
                valid_matches.add(scp_num.zfill(3))  # Pad with zeros for consistent formatting
                
        return valid_matches
    
    @classmethod
    def format_response(cls, scp_numbers: Set[str]) -> Optional[str]:
        """Format the response message with SCP links"""
        if not scp_numbers:
            return None
            
        response = "I've detected SCPs! Here are the articles:\n"
        # Convert to list and sort numerically
        sorted_numbers = sorted(scp_numbers, key=lambda x: int(x))
        for scp_num in sorted_numbers:
            url = f"<https://scp-wiki.wikidot.com/scp-{scp_num}>"
            response += f"[SCP-{scp_num}]({url})\n"
            
        return response.strip()
    
    @classmethod
    def get_random_scp(cls) -> str:
        """Generate a response with a random SCP"""
        random_num = random.randint(cls.MIN_SCP, cls.MAX_SCP)
        scp_num = str(random_num).zfill(3)
        url = f"<https://scp-wiki.wikidot.com/scp-{scp_num}>"
        return (
            f"🎲 I've selected a random SCP for you!\n"
            f"[SCP-{scp_num}]({url})\n"
            f"*Good luck, and remember your amnestics!* 💊"
        )