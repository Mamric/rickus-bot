import discord
from discord.ext import commands, tasks
from datetime import datetime, timedelta
import os
from .utils import get_utc_now, load_json_file, save_json_file

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        elevated_role_id = os.getenv('ELEVATED_ROLE_ID')
        if not elevated_role_id:
            raise ValueError("ELEVATED_ROLE_ID must be provided through environment variables")
        self.elevated_role_id = int(elevated_role_id)
        self.pending_elevations = {}
        self.recently_elevated = set()
        self.ELEVATED_USERS_FILE = 'elevated_users.json'
        self.PENDING_FILE = 'pending_elevations.json'
        self.load_data()
        self.check_pending_elevations.start()

    def load_data(self):
        """Load saved elevation data"""
        self.recently_elevated = set(load_json_file(self.ELEVATED_USERS_FILE, []))
        pending_data = load_json_file(self.PENDING_FILE, {})
        
        # Convert string keys back to integers and string dates back to datetime
        self.pending_elevations = {}
        for k, v in pending_data.items():
            try:
                member_id = int(k)
                # Handle both ISO format strings and raw timestamps
                if isinstance(v, str):
                    elevation_time = datetime.fromisoformat(v)
                else:
                    elevation_time = datetime.fromtimestamp(v, tz=get_utc_now().tzinfo)
                self.pending_elevations[member_id] = elevation_time
            except (ValueError, TypeError) as e:
                print(f"Error loading elevation time for member {k}: {e}")

    def save_pending_elevations(self):
        """Save pending elevations to file"""
        # Convert datetime objects to ISO format strings for JSON serialization
        pending_data = {str(k): v.isoformat() for k, v in self.pending_elevations.items()}
        save_json_file(self.PENDING_FILE, pending_data)

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
        print(f"[{current_time}] Running daily elevation check...")
        
        elevated_this_check = []
        
        # Make a copy of the items since we'll be modifying the dict
        for member_id, elevation_time in list(self.pending_elevations.items()):
            print(f"Checking member {member_id}, elevation time: {elevation_time}, current time: {current_time}")
            
            if current_time >= elevation_time:
                for guild in self.bot.guilds:
                    member = guild.get_member(member_id)
                    if member:
                        if await self.give_elevated_role(member):
                            elevated_this_check.append(member)
                            print(f"[{current_time}] Elevated user: {member.name} (ID: {member.id})")
                        del self.pending_elevations[member_id]
                        self.save_pending_elevations()
        
        # Send notifications if any members were elevated
        notification_manager = self.bot.get_cog('NotificationManager')
        if notification_manager:
            if elevated_this_check:
                await notification_manager.send_elevation_announcement(elevated_this_check)
                print(f"[{current_time}] Sent elevation notifications for {len(elevated_this_check)} users")
            else:
                # Send message to the announcement channel that no new members were elevated
                for guild in self.bot.guilds:
                    channel = guild.get_channel(notification_manager.announcement_channel_id)
                    if channel:
                        await channel.send("📊 Daily elevation check complete - No new members were elevated today.")

    @check_pending_elevations.before_loop
    async def before_check_pending_elevations(self):
        """Wait until the bot is ready before starting the task"""
        await self.bot.wait_until_ready()

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
        elevated_role = ctx.guild.get_role(self.elevated_role_id)
        
        if not elevated_role:
            await ctx.send("Could not find ELEVATED role!")
            return
        
        async for member in ctx.guild.fetch_members():
            if member.joined_at:
                if current_time - member.joined_at >= timedelta(days=90) and elevated_role not in member.roles:
                    if await self.give_elevated_role(member):
                        count += 1
                else:
                    elevation_time = member.joined_at + timedelta(days=90)
                    self.pending_elevations[member.id] = elevation_time
        
        self.save_elevated_users()
        response = f"Finished checking members. Elevated {count} new members and scheduled remaining eligible members."
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