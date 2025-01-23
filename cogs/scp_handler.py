import discord
from discord.ext import commands
import random
import re

class SCPHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scp_channels = [759136825658310717, 1068738747417514064]
        # Updated pattern to capture normal SCPs, -ARC, and -J variants
        self.scp_pattern = re.compile(r'(?i)scp-([0-9]{1,4})(?:-(?:ARC|J))?(?:\s|$)')

    async def handle_scp_mention(self, message, scp_number):
        """Handle an SCP number mention"""
        scp_num = int(scp_number)
        if 0 <= scp_num <= 7999:
            # Check if the original message contained -ARC or -J
            is_arc = bool(re.search(rf'(?i)scp-{scp_number}-ARC', message.content))
            is_joke = bool(re.search(rf'(?i)scp-{scp_number}-J', message.content))
            
            if is_arc:
                await message.channel.send(f"🔗 SCP-{scp_number.zfill(3)}-ARC: https://scp-wiki.wikidot.com/scp-{scp_number.zfill(3)}-arc")
            elif is_joke:
                await message.channel.send(f"🔗 SCP-{scp_number.zfill(3)}-J: https://scp-wiki.wikidot.com/scp-{scp_number.zfill(3)}-j")
            else:
                await message.channel.send(f"🔗 SCP-{scp_number.zfill(3)}: https://scp-wiki.wikidot.com/scp-{scp_number.zfill(3)}")
        else:
            await message.channel.send(f"❌ SCP-{scp_number} is not a valid SCP article number.")

    @commands.command(name="random")
    async def random_scp(self, ctx):
        """Get a random SCP article (standard articles only)"""
        if ctx.channel.id in self.scp_channels:
            scp_number = str(random.randint(1, 7999)).zfill(3)
            await ctx.send(f"🎲 Here's a random SCP article:\nSCP-{scp_number}: https://scp-wiki.wikidot.com/scp-{scp_number}")
        else:
            await ctx.send("Sorry, I can only share SCP articles in designated channels! 🤫")

async def setup(bot):
    await bot.add_cog(SCPHandler(bot)) 