from twitchio.ext import commands
from twitchio import dataclasses

from usefulStuff import collector
from authDetails import ol

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
        await context.send(f"Add me on Town of Salem: {ol.ToS}")

    @commands.command(name="discord")
    @collector.cooldown
    async def discord(self, context: dataclasses.Context):
        await context.send(f"It seems that you are interested in our Discord server. You can join over here: {ol.discord}")

    @commands.command(name="destiny")
    @collector.cooldown
    async def destinyJoin(self, context: dataclasses.Context):
        await context.send(f"If you want to join me with your guardian (and my fireteam settings are on public), you can use this joincode: {ol.destiny}")
