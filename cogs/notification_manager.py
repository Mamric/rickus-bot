import discord
from discord.ext import commands
from .utils import split_into_chunks

class NotificationManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.announcement_channel_id = 1029222292393312297  # big-chat channel
        self.color_role_channel_id = 1029217641077940284  # color role channel

    async def send_notification_chunks(self, ctx, mentions, is_announcement=False):
        """Split notifications into chunks and send them"""
        chunk_size = 20
        chunks = split_into_chunks(mentions, chunk_size)
        
        if not chunks:
            return
        
        # Send first message with header
        first_chunk = chunks.pop(0)
        
        if is_announcement:
            first_message = (
                "🎉 **CONGRATULATIONS NEW ELEVATED MEMBERS!** 🎉\n\n"
                f"{', '.join(first_chunk)}\n\n"
                "You have proven your worth by remaining in this server for over 3 months!\n"
                "You have been granted the ELEVATED role! 🎊\n"
                f"Head over to <#{self.color_role_channel_id}> to choose your favorite color for your username! 🎨"
            )
        else:
            first_message = (
                "🎉 **CONGRATULATIONS!** 🎉\n\n"
                f"{', '.join(first_chunk)}\n\n"
                "You have proven your worth by remaining in this server for over 3 months! "
                "You have been granted the ELEVATED role, marking you as distinguished members of our community!"
            )
        
        await ctx.send(first_message)
        
        # Send remaining chunks if any
        for chunk in chunks:
            if is_announcement:
                continuation_message = (
                    "🎉 More newly ELEVATED members: "
                    f"{', '.join(chunk)}\n"
                    f"Don't forget to visit <#{self.color_role_channel_id}> to pick your color! 🎨"
                )
            else:
                continuation_message = f"🎉 More ELEVATED members: {', '.join(chunk)}"
            await ctx.send(continuation_message)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def notifyelevated(self, ctx):
        """Notify recently elevated users of their new status"""
        role_manager = self.bot.get_cog('RoleManager')
        if not role_manager or not role_manager.recently_elevated:
            await ctx.send("No members have been recently elevated.")
            return

        # Get list of member mentions
        mentions = []
        for member_id in role_manager.recently_elevated:
            member = ctx.guild.get_member(member_id)
            if member:
                mentions.append(member.mention)

        if mentions:
            await self.send_notification_chunks(ctx, mentions)
            role_manager.recently_elevated.clear()
            role_manager.save_elevated_users()
        else:
            await ctx.send("Could not find any recently elevated members to notify.")

    async def send_elevation_announcement(self, elevated_members):
        """Send announcement for newly elevated members"""
        if not elevated_members:
            return
            
        for guild in self.bot.guilds:
            channel = guild.get_channel(self.announcement_channel_id)
            if channel:
                mentions = [member.mention for member in elevated_members]
                await self.send_notification_chunks(channel, mentions, is_announcement=True)

async def setup(bot):
    await bot.add_cog(NotificationManager(bot)) 