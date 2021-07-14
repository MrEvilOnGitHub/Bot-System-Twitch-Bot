from twitchio.ext import commands
from twitchio import dataclasses

from usefulStuff import collector

@commands.cog()
class joincodes:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lurk")
    async def lurk(self, context: dataclasses.Context):
        await context.send(f"{context.author.name} has decided to lurk in the shadows, taking care of their own business")

    @commands.command(name="unlurk")
    async def unlurk(self, context: dataclasses.Context):
        await context.send(f"{context.author.name} has returned. What will they do now?")

    @commands.command(name="town")
    @collector.cooldown
    async def townOfSalem(self, context: dataclasses.Context):
        await context.send("Add me on Town of Salem: MrEvilInSalem")

    @commands.command(name="discord")
    @collector.cooldown
    async def discord(self, context: dataclasses.Context):
        await context.send("It seems that you are interested in our Discord server. You can join over here: discord.gg/3a4ZseU")

    @commands.command(name="destiny")
    @collector.cooldown
    async def destinyJoin(self, context: dataclasses.Context):
        await context.send("If you want to join me with your guardian (and my fireteam settings are on public), you can use this joincode: 76561198078422715")

    @commands.command(name="help")
    @collector.cooldown
    async def help(self, context: dataclasses.Context):
        await context.send("This bot is selfmade and open-source. The commands can be found in the info tabs")
