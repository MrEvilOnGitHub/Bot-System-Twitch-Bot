from twitchio.ext import commands
from twitchio import dataclasses

@commands.cog()
class mod:
    def __init__(self, bot):
        self.bot = bot

    async def event_message(self, context: dataclasses.Context):
        pass

    @commands.command(name="clear")
    async def clear(self, context: dataclasses.Context):
        if context.user.is_mod:
            try:
                await context.channel.clear()
            except TwitchIOBException:
                await context.send("The bot is not a mod on this channel. Unable to use the clear command")
