import discord
from discord.ext import commands, tasks
from datetime import timedelta
from .utils import get_utc_now, load_json_file, save_json_file

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.elevated_role_id = int(discord.utils.get_environment_variable('ELEVATED_ROLE_ID'))
        self.pending_elevations = {}
        self.recently_elevated = set()
        self.ELEVATED_USERS_FILE = 'elevated_users.json'
        self.PENDING_FILE = 'pending_elevations.json'
        self.load_data()
        self.check_pending_elevations.start()

    def load_data(self):
        """Load saved elevation data"""
        self.recently_elevated = set(load_json_file(self.ELEVATED_USERS_FILE, []))
        self.pending_elevations = load_json_file(self.PENDING_FILE, {})
        # Convert string keys back to integers
        self.pending_elevations = {int(k): v for k, v in self.pending_elevations.items()}

    def save_pending_elevations(self):
        """Save pending elevations to file"""
        save_json_file(self.PENDING_FILE, self.pending_elevations)

    def save_elevated_users(self):
        """Save elevated users to file"""
        save_json_file(self.ELEVATED_USERS_FILE, list(self.recently_elevated))

    async def give_elevated_role(self, member):
        """Give member the ELEVATED role. Returns True if successful."""
        elevated_role = member.guild.get_role(self.elevated_role_id)
        if elevated_role and elevated_role not in member.roles:
            try:
                await member.add_roles(elevated_role)
                self.recently_elevated.add(member.id)
                self.save_elevated_users()
                print(f"[{get_utc_now()}] Successfully gave ELEVATED role to {member.name}")
                return True
            except discord.Forbidden:
                print(f"[{get_utc_now()}] Failed to give ELEVATED role to {member.name} - Missing permissions")
                return False
        return False

    @tasks.loop(hours=24)
    async def check_pending_elevations(self):
        current_time = get_utc_now()
        print(f"[{current_time}] Running hourly elevation check...")
        
        elevated_this_check = []
        
        for member_id, elevation_time in list(self.pending_elevations.items()):
            if current_time >= elevation_time:
                for guild in self.bot.guilds:
                    member = guild.get_member(member_id)
                    if member:
                        if await self.give_elevated_role(member):
                            elevated_this_check.append(member)
                            print(f"[{current_time}] Elevated user: {member.name} (ID: {member.id})")
                        del self.pending_elevations[member_id]
                        self.save_pending_elevations()
        
        return elevated_this_check

    @commands.Cog.listener()
    async def on_member_join(self, member):
        elevation_time = get_utc_now() + timedelta(days=90)
        self.pending_elevations[member.id] = elevation_time
        self.save_pending_elevations()
        print(f"Scheduled elevation for {member.name} at {elevation_time}")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def checkmembers(self, ctx):
        """Check all current members for elevation eligibility"""
        await ctx.send("Checking all members for elevation eligibility...")
        
        count = 0
        current_time = get_utc_now()
        self.recently_elevated.clear()
        
        async for member in ctx.guild.fetch_members():
            if member.joined_at:
                if current_time - member.joined_at >= timedelta(days=90):
                    await self.give_elevated_role(member)
                    count += 1
                else:
                    elevation_time = member.joined_at + timedelta(days=90)
                    self.pending_elevations[member.id] = elevation_time
        
        self.save_elevated_users()
        response = f"Finished checking members. Elevated {count} members and scheduled remaining eligible members."
        if count > 0:
            response += "\nWould you like me to notify the newly elevated members? Use `rickus notifyelevated` to send notifications."
        await ctx.send(response)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def collectelevated(self, ctx):
        """One-time command to collect all members with ELEVATED role for notification"""
        await ctx.send("Collecting all members with ELEVATED role...")
        
        count = 0
        elevated_role = ctx.guild.get_role(self.elevated_role_id)
        
        if not elevated_role:
            await ctx.send("Could not find ELEVATED role!")
            return
            
        self.recently_elevated.clear()
        
        for member in elevated_role.members:
            self.recently_elevated.add(member.id)
            count += 1
        
        self.save_elevated_users()
        await ctx.send(f"Collected {count} members with ELEVATED role.")

async def setup(bot):
    await bot.add_cog(RoleManager(bot)) 