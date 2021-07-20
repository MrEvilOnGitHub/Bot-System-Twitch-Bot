from twitchio.ext import commands
from twitchio import dataclasses

from usefulStuff import collector
import const_messages as m

@commands.cog()
class repeats:
    def __init__(self, bot):
        self.bot = bot

    messages = (
        {"message": "This bot is open-source and selfmade. Details can be found using g!botInfo"
        "delay": 300}
    )

    async def sendRepeatedMessage(self, message=str, delay=120):
        await asyncio.sleep(delay)
        channel_obj = self.get_channel("MrEvilOnTwitch")
        if collector.getStreamInfo(channel) != collector.offlineData:
            await channel_obj.send(message)
        loop.create_task(self.sendRepeatedMessage(message=message, delay=delay))

    async def event_ready(self):
        for i in self.messages:
            await self.sendRepeatedMessage(message=i["message"],
                                           delay=i["delay"])

    @commands.command(name="rm")
    async def rm(self, context):
        raise NotImplementedError
