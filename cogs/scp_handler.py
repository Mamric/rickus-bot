import discord
from discord.ext import commands
import random
import re

class SCPHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.scp_channels = [759136825658310717, 1068738747417514064]
        # Updated pattern to capture both normal SCPs and -ARC variants
        self.scp_pattern = re.compile(r'(?i)scp-([0-9]{1,4})(?:-ARC)?(?:\s|$)')

    async def handle_scp_mention(self, message, scp_number):
        """Handle an SCP number mention"""
        scp_num = int(scp_number)
        if 1 <= scp_num <= 7999:
            # Check if the original message contained -ARC
            is_arc = bool(re.search(rf'(?i)scp-{scp_number}-ARC', message.content))
            
            if is_arc:
                await message.channel.send(f"🔗 SCP-{scp_number.zfill(3)}-ARC: https://scp-wiki.wikidot.com/scp-{scp_number.zfill(3)}-arc")
            else:
                await message.channel.send(f"🔗 SCP-{scp_number.zfill(3)}: https://scp-wiki.wikidot.com/scp-{scp_number.zfill(3)}")
        else:
            await message.channel.send(f"❌ SCP-{scp_number} is not a valid SCP article number.")

    @commands.command(name="random")
    async def random_scp(self, ctx):
        """Get a random SCP article"""
        if ctx.channel.id in self.scp_channels:
            scp_number = str(random.randint(1, 7999)).zfill(3)
            # Small chance (5%) of getting an -ARC article
            is_arc = random.random() < 0.05
            
            if is_arc:
                await ctx.send(f"🎲 Here's a random SCP article:\nSCP-{scp_number}-ARC: https://scp-wiki.wikidot.com/scp-{scp_number}-arc")
            else:
                await ctx.send(f"🎲 Here's a random SCP article:\nSCP-{scp_number}: https://scp-wiki.wikidot.com/scp-{scp_number}")
        else:
            await ctx.send("Sorry, I can only share SCP articles in designated channels! 🤫")

async def setup(bot):
    await bot.add_cog(SCPHandler(bot)) 