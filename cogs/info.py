from twitchio.ext import commands
from twitchio import dataclasses
import time

from usefulStuff import collector

@commands.cog()
class infos:
    @commands.command(name="time")
    @collector.cooldown
    async def localtime(self, context: dataclasses.Context):
        t = time.localtime()
        await context.send(f"Current time for MrEvil: {t.tm_hour}:{t.tm_min}")

    @commands.command(name="so")
    @collector.cooldown
    async def shoutout(self, context: dataclasses.Context):
        message = context.content
        if len(message) > 4:
            target = message[len(generalData.BOT_PREFIX)+3:]
        else:
            target = "irepptar"
        stream = generalData.getStreamInfo(target)
        if stream != generalData.offlineData:
            string = f'{target} is currently live playing {stream["data"][0]["game_name"]}. Check them out here: twitch.tv/{target}'
            await context.send(string)
        else:
            await context.send(f"{target} is currently offline, but you might find them here: twitch.tv/{target}")

    @commands.command(name="uptime")
    @collector.cooldown
    async def uptime(self, context: dataclasses.Context):
        streamName = context.channel.name
        streamInfo = generalData.getStreamInfo(streamName.lower())
        offlineData = {'data': [], 'pagination': {}}
        if streamInfo == offlineData:
            await context.send('OI, the stream is offline, there is no uptime to be found')
        else:
            await context.send(f'The stream started at {streamInfo["data"][0]["started_at"]}')

    @commands.command(name="streamdata")
    @collector.cooldown
    async def streamdata(self, context):
        """
        Prints public information of given streamname to console
        """
        print(context.channel.name)
        await collector.asyncIterateThroughDict(
            generalData.getStreamInfo(context.channel.name.lower()),
            print, functionIsAsync=False)
        await context.send("worked")
