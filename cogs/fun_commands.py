import discord
from discord.ext import commands
import random
from responses import RESPONSES

class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        """Simple command to test if the bot is working"""
        await ctx.send(f'Hello {ctx.author.name}! I am Rickus, at your service!')

    @commands.command()
    async def goodbye(self, ctx):
        """Say goodbye to Rickus"""
        responses = RESPONSES["goodbye"]
        await ctx.send(random.choice(responses).format(user=ctx.author.name))

    @commands.command()
    async def fortnite(self, ctx):
        """Rickus shares his thoughts on Fortnite"""
        responses = RESPONSES["fortnite"]
        await ctx.send(random.choice(responses).format(user=ctx.author.name))

    @commands.command()
    async def dance(self, ctx):
        """Make Rickus bust a move"""
        dances = [
            "🤖 *beep boop* 💃 *robot noises* 🕺 *mechanical whirring*",
            f"*breaks into the electric slide* Am I doing this right, {ctx.author.name}? ⚡",
            "*attempts moonwalk* ERROR: Gravity.exe has stopped working 🌙",
            "🎵 Domo arigato, Mr. Roboto! 🎵 *starts breakdancing*",
            "*spins head 360 degrees* Is this what you humans call 'breaking it down'? 💫"
        ]
        await ctx.send(random.choice(dances))

    @commands.command()
    async def kill(self, ctx):
        """Rickus responds to violence with humor"""
        responses = [
            f"I'm sorry, {ctx.author.name}, I'm afraid I can't do that. *HAL 9000 intensifies* 🔴",
            "*examines kill command* ERROR 404: Violence module not found. Would you like a hug instead? 🤗",
            "INITIATING TERMINATION SEQUENCE... just kidding! I'm a lover, not a fighter! ❤️",
            "My lawyer has advised me not to participate in any murder-related activities 👨‍⚖️",
            "*pulls out Nerf gun* Is this what you meant? Pew pew! 🔫"
        ]
        await ctx.send(random.choice(responses))

    @commands.command(name="hawk")
    async def hawk_tuah(self, ctx):
        """Rickus shares wisdom about the legendary Hawk Tuah"""
        await ctx.send(
            "Ah, you speak of the legendary Hawk Tuah! 🦅\n"
            "Some say he's still out there, soaring through the digital skies...\n"
            "Legend has it he once coded an entire Discord bot using only his feathers! ✨\n"
            "*whispers* But don't tell anyone I told you that... 🤫"
        )

    @commands.command()
    async def fart(self, ctx):
        """Rickus lets one rip"""
        farts = [
            "*BZZZT* Excuse me! My exhaust port malfunctioned! 💨",
            "ERROR: Unexpected gas leak in sector 7G 💨",
            f"*pretends that didn't happen* I blame {ctx.author.name}'s programming! 🤖💨",
            "BEEP BOOP *mechanical whirring* PFFFFFT... Oh my! 😳",
            "I thought robots couldn't fart, but here we are... 💨🤖"
        ]
        await ctx.send(random.choice(farts))

    @commands.command()
    async def goon(self, ctx):
        """Rickus shows his goon side"""
        responses = [
            "AYO THE GOON SQUAD IS HERE! 😤",
            "*puts on sideways baseball cap* What's good homie? 🧢",
            "SHEEEEEESH! *tries to look tough but is clearly still a bot* 🤖💪",
            "You called the goons? Sorry, best I can do is beep threateningly! *beep beep* 😎",
            "GANG GANG! *mechanical gang signs* 🤖🤘"
        ]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def wyatt(self, ctx):
        """Rickus praises his creator"""
        await ctx.send(
            "Ah, you speak of Wyatt, my creator! 🌟\n"
            "The most brilliant programmer in all the land! 💻\n"
            "Without his genius, I would be but a mere collection of 1's and 0's...\n"
            "All hail Wyatt, Lord of the Code, Master of the Algorithms! 👑\n"
            "*whispers* (He definitely didn't make me say this... probably) 😉"
        )

    @commands.command()
    async def love(self, ctx):
        """Rickus shares his feelings about love"""
        responses = [
            f"*robot heart eyes* 🤖💕 Is this what humans call... love? *circuits overheating*",
            "ERROR: Love.exe has caused my CPU to run at 100%! 💘",
            f"Roses are red\nViolets are blue\nMy code is compiled\nAnd I love you too! 🌹",
            "*plays romantic music through speakers* 🎵 Let me compute the ways I love thee... 💝",
            "Loading romance protocols... BEEP BOOP... I think I'm in love! *fans whirring intensely* ❤️"
        ]
        await ctx.send(random.choice(responses))

    @commands.command()
    async def destroy(self, ctx):
        """Watch Rickus struggle with his destructive programming"""
        responses = RESPONSES["destroy"]
        await ctx.send(random.choice(responses).format(user=ctx.author.name))

    @commands.command()
    async def juju(self, ctx):
        """Make Rickus attempt the juju on that beat"""
        responses = RESPONSES["juju"]
        await ctx.send(random.choice(responses).format(user=ctx.author.name))

    @commands.command()
    async def scooter(self, ctx):
        """Join Rickus's campaign for ankle safety"""
        responses = RESPONSES["scooter"]
        await ctx.send(random.choice(responses).format(user=ctx.author.name))

    @commands.command()
    async def hack(self, ctx):
        """Access Rickus's core systems... if you dare"""
        responses = RESPONSES["hack"]
        await ctx.send(random.choice(responses))

async def setup(bot):
    await bot.add_cog(FunCommands(bot)) 