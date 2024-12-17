import re
import random
from typing import Set, Optional, Tuple

class SCPHandler:
    # Channels where SCP detection is enabled
    SCP_CHANNELS = [759136825658310717, 1068738747417514064]
    
    # Updated pattern to catch -J SCPs
    SCP_PATTERN = re.compile(r'(?i)scp-(\d{1,4}(?:-j)?)\b')
    
    # SCP number range
    MIN_SCP = 1
    MAX_SCP = 8000

    # Footer message
    FOOTER = "\n\n*This bot is a work in progress. Please ping scpWyatt for feedback or to report bugs!* 🤖"
    
    @classmethod
    def is_valid_channel(cls, channel_id: int) -> bool:
        """Check if channel is enabled for SCP detection"""
        return channel_id in cls.SCP_CHANNELS
    
    @classmethod
    def find_scp_numbers(cls, content: str) -> Tuple[Set[str], Set[str]]:
        """Extract valid SCP numbers and track invalid ones"""
        matches = set(cls.SCP_PATTERN.findall(content))
        valid_matches = set()
        invalid_matches = set()
        
        for scp_num in matches:
            # Handle -J SCPs separately
            if scp_num.lower().endswith('-j'):
                valid_matches.add(scp_num.lower())  # Keep -j SCPs as is
            else:
                num = int(scp_num)
                if cls.MIN_SCP <= num <= cls.MAX_SCP:
                    valid_matches.add(scp_num.zfill(3))  # Pad with zeros for consistent formatting
                else:
                    invalid_matches.add(scp_num)
                
        return valid_matches, invalid_matches
    
    @classmethod
    def format_response(cls, scp_numbers: Set[str], invalid_numbers: Set[str]) -> Optional[str]:
        """Format the response message with SCP links"""
        if not scp_numbers and not invalid_numbers:
            return None
            
        response = ""
        
        # Handle valid SCPs
        if scp_numbers:
            response += "I've detected SCPs! Here are the articles:\n"
            # Sort numbers, keeping -j SCPs at the end
            sorted_numbers = sorted(scp_numbers, key=lambda x: (not x.endswith('-j'), int(x.split('-')[0]), x))
            for scp_num in sorted_numbers:
                url = f"<https://scp-wiki.wikidot.com/scp-{scp_num}>"
                response += f"[SCP-{scp_num.upper()}]({url})\n"
        
        # Handle invalid SCPs
        if invalid_numbers:
            if response:
                response += "\n"  # Add spacing if we had valid SCPs
            response += (
                "⚠️ Note: Some SCP numbers were out of bounds!\n"
                f"I can only link SCPs between {cls.MIN_SCP} and {cls.MAX_SCP} "
                "(plus -J variants like SCP-420-J).\n"
                f"Invalid SCPs mentioned: {', '.join(f'SCP-{num}' for num in sorted(invalid_numbers, key=lambda x: int(x)))}"
            )
            
        return response.strip() + cls.FOOTER
    
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
            f"{cls.FOOTER}"
        )