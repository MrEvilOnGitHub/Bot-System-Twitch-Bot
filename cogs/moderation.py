from twitchio.ext import commands
from twitchio import dataclasses

@commands.cog()
class mod:
    def __init__(self, bot):
        self.bot = bot

    bannedWords = ("söojdafjiosdfjioj") # only for testing rn

    async def event_message(self, context: dataclasses.Context):
        if context.author.name == self.bot.nick:
            # don't react to own messages
            return
        if any(x in context.content for x in self.bannedWords):
            print(f"Timing out {context.author.name} b/c of of a banned word")
            await context.channel.timeout(context.author.name, duration=1,reason="Banned word detected")

    @commands.command(name="clear")
    async def clear(self, context: dataclasses.Context):
        if context.author.is_mod:
            try:
                await context.channel.clear()
            except TwitchIOBException:
                await context.send("The bot is not a mod on this channel. Unable to use the clear command")
