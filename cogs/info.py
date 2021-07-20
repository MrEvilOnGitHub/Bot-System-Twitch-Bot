from twitchio.ext import commands
from twitchio import dataclasses
import time

from usefulStuff import collector
from authDetails import getStreamInfo

@commands.cog()
class infos:
    def __init__(self, bot):
        self.bot = bot

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
        stream = getStreamInfo(target)
        if stream != collector.offlineData:
            string = f'{target} is currently live playing {stream["data"][0]["game_name"]}. Check them out here: twitch.tv/{target}'
            await context.send(string)
        else:
            await context.send(f"{target} is currently offline, but you might find them here: twitch.tv/{target}")

    @commands.command(name="uptime")
    @collector.cooldown
    async def uptime(self, context: dataclasses.Context):
        streamName = context.channel.name
        streamInfo = getStreamInfo(streamName.lower())
        offlineData = {'data': [], 'pagination': {}}
        if streamInfo == offlineData:
            await context.send('OI, the stream is offline, there is no uptime to be found')
        else:
            tmp = streamInfo["data"][0]["started_at"].split("T")
            tokens = [tmp[0].split("-"), tmp[1].split(":")]
            del tmp
            tokens[1][2]=tokens[1][2][:-1]
            currentTime = time.gmtime()
            liveSince = {
                "days": currentTime.tm_mday - int(tokens[0][2]),
                "hours": currentTime.tm_hour - int(tokens[1][0]),
                "mins": currentTime.tm_min - int(tokens[1][1]),
                "secs": currentTime.tm_sec - int(tokens[1][2])
            }
            await context.send(f'The stream has been going on for {liveSince["days"]} days, {liveSince["hours"]} hours, {liveSince["mins"]} minutes and {liveSince["secs"]} seconds.')

    @commands.command(name="streamdata")
    @collector.cooldown
    async def streamdata(self, context):
        """
        Prints public information of given streamname to console
        """
        print(context.channel.name)
        await collector.asyncIterateThroughDict(
            getStreamInfo(context.channel.name.lower()),
            print, functionIsAsync=False)
        await context.send("worked")

    @commands.command(name="botInfo")
    @collector.cooldown
    async def botinfo(self, context: dataclasses.Context):
        if context.channel.name.lower() != "mrevilontwitch":
            await context.send("This bot has been made by MrEvil. The source-code can be found here: https://github.com/MrEvilOnGitHub/Bot-System-Twitch-Bot")
            return
        await context.send("This bot is selfmade. If you want to take a look at the source-code, go to: https://github.com/MrEvilOnGitHub/Bot-System-Twitch-Bot")
