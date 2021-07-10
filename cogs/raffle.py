from twitchio.ext import commands

from usefulStuff import collector

@commands.cog()
class raffles:
    def __init__(self, bot):
        self.bot = bot

    _req = ()
    _opt = ("time", "min", "max")

    def _addRaffle(self, args = {"time": 5, "min": 0, "max": 0}):
        raise NotImplementedError

    @commands.command(name="raffle_new")
    async def raffle_new(self, context):
        tokens = context.message.content.split()
        args = {"time": 5, "min": 0, "max": 0}
        for i in tokens[1:]:
            tmp = i.split("=")
            if len(tmp) == 2 and tmp[0] in self._opt:
                # ignore invalid arguments
                args[tmp[0]] = tmp[1]
