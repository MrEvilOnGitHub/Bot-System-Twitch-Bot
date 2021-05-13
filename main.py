from twitchio.ext import commands
from twitchio.errors import *
from twitchio import dataclasses
import time
import asyncio
import requests
import threading
import types
import inspect

# import the data.py file storing all the tokens and other neccessary info
import data as generalData

import const_messages as messages

def cooldown(function, duration=int(30)):
    """
    Cooldown decorator for command functions

    Optional argument: duration = integer

    How it works
        Launches a timing thread utilizing sleep when the command is called.
        And until that thread finishes the internal on_cooldown variable
        will prevent another call of the function
    """
    function.on_cooldown = False

    def sleeper():
        function.on_cooldown = True
        time.sleep(duration)
        function.on_cooldown = False

    async def wrapper(*args, **kwargs):
        if function.on_cooldown:
            print(f"Function {function.__name__} on cooldown")
        else:
            timer = threading.Thread(target=sleeper)
            await function(*args, **kwargs)
            timer.start()
    return wrapper


def iterateThroughDict(dictionary, funtionToExecute):
    for key in dictionary:
        if type(dictionary[key]) is dict:
            iterateThroughDict(dictionary[key], funtionToExecute)
        else:
            funtionToExecute((key, dictionary[key]))


async def asyncIterateThroughDict(dictionary,
                                  asyncFunction,
                                  functionIsAsync=True):
    for key in dictionary:
        if type(dictionary[key]) is dict:
            await asyncIterateThroughDict(dictionary[key], asyncFunction, functionIsAsync=functionIsAsync)
        else:
            if functionIsAsync:
                await asyncFunction((key, dictionary[key]))
            else:
                asyncFunction((key, dictionary))

# Could be useful:
#
# add_listener(func, name: str = None)
# Method which adds a coroutine as an extra listener.
# This can be used to add extra event listeners to the bot.
# Parameters:
#     func (coro [Required]) – The coroutine to assign as a listener.
#     name (str [Required]) – The event to register. E.g “event_message”.
#
# Add async func to async loop
#
# chan = bot.get_channel("channelname")
# loop = asyncio.get_event_loop()
# loop.create_task(chan.send("Send this message"))

def sendMessageToChannel(channel: str, message: str):
    for i in generalData.CHANNELS:
        if i.lower() == channel.lower():
            raise ValueError
    loop = asyncio.get_event_loop()
    loop.create_task(Bot.get_channel(channel).send(message))


class api:
    """
    Wrapper class for interacting with the localy hosted web-API
    """

    apiURL = "http://localhost:5000/api/alpha/"

    def interact(service, action="get", data=None):
        if action != "get" or action != "set":
            raise TypeError(message="action must be get or set")
        try:
            r = requests.get(apiURL+service, headers=data)
        except requests.exceptions.ConnectionError:
            return None
        return r

    def receiveBannedWordList(self):
        try:
            request = self.interact("bannedWords")
            if request is None:
                return
            if request.status_code != 200:
                return
            data = request.json()
            returner = tuple(data)
        except:
            returner = tuple
        return returner


def receiveBannedWordList():
    request = requests.get(api.apiURL+"bannedWords")
    if request is None:
        return
    if request.status_code != 200:
        return
    data = request.json()
    returner = tuple(data)
    return returner

class Bot(commands.Bot):

    bannedWords = tuple

    def __init__(self):
        super().__init__(irc_token=generalData.OAUTH_TOKEN,
                         client_id=generalData.CLIENT_ID,
                         nick=generalData.BOT_NICK,
                         prefix=generalData.BOT_PREFIX,
                         initial_channels=generalData.CHANNELS)
        # self.bannedWords = receiveBannedWordList()

    async def sendRepeatedMessage(self,
                                  channel="MrEvilOnTwitch",
                                  message=str, delay=120,
                                  loop=asyncio.get_event_loop()):
        channel_obj = self.get_channel(channel)
        await asyncio.sleep(delay)
        # if generalData.getStreamInfo(channel) != generalData.offlineData:
        await channel_obj.send(message)
        loop.create_task(self.sendRepeatedMessage(channel=channel, message=message, delay=delay, loop=loop))

    async def event_ready(self):
        print(f'Bot ready | {self.nick}')
        await self.sendRepeatedMessage("MrEvilOnTwitch", messages.commands, delay=30)

    async def event_message(self, message):
        # remove messages with blacklisted words first, then execute the command if it isn't removed
        # ^ yet to be implemented
        await self.handle_commands(message)

    async def event_usernotice_subscription(self, data):
        apiData = {}
        if data.sub_plan == "Prime":
            apiData["tier"] = 4
        elif data.sub_plan == "1000":
            apiData["tier"] = 1
        elif data.sub_plan == "2000":
            apiData["tier"] = 2
        elif data.sub_plan == "3000":
            apiData["tier"] = 3
        if data.streak_months is not None:
            apiData["streak"] = data.streak_months
        else:
            apiData["streak"] = 0
        if data.streak_months != 0:
            await data.channel.send(f'{data.user.name} has extended their sub-streak on tier {apiData["tier"]} by one month. It\'s now at {data.streak_months} months!')
        else:
            await data.channel.send(f'{data.user.name} has just subscribed on tier {apiData["tier"]}')

    @commands.command(name="test")
    @cooldown
    async def test(self, context):
        await context.send(f'Hello {context.author.name}')

    @commands.command(name="streamdata")
    @cooldown
    async def streamdata(self, context):
        """
        Grabs the publicly available information of the stream chat is has been called from and prints it to console output
        """
        print(context.channel.name)
        await asyncIterateThroughDict(generalData.getStreamInfo(context.channel.name.lower()), print, functionIsAsync=False)
        await context.send("worked")

    @commands.command(name="so")
    @cooldown
    async def shoutout(self, context):
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

    @commands.command(name="help")
    @cooldown
    async def help(self, context):
        if context.channel.name == "mrevilontwitch":
            await context.send("This bot is selfmade and open-source. The commands can be found in the info tabs")
        else:
            await context.send("This bot has been made by twitch.tv/MrEvilOnTwitch. The commands are available in his info tabs")

    @commands.command(name="uptime")
    @cooldown
    async def uptime(self, context):
        streamName = context.channel.name
        streamInfo = generalData.getStreamInfo(streamName.lower())
        offlineData = {'data': [], 'pagination': {}}
        if streamInfo == offlineData:
            await context.send('OI, the stream is offline, there is no uptime to be found')
        else:
            await context.send(f'The stream started at {streamInfo["data"][0]["started_at"]}')

    @commands.command(name="discord")
    @cooldown
    async def discord(self, context):
        if context.channel.name == "mrevilontwitch":
            await context.send("It seems that you are interested in our Discord server. You can join over here: discord.gg/3a4ZseU")

    @commands.command(name="destiny")
    @cooldown
    async def destinyJoin(self, context):
        if context.channel.name == "mrevilontwitch":
            await context.send("If you want to join me with your guardian (and my fireteam settings are on public), you can use this joincode: 76561198078422715")

    @commands.command(name="town")
    @cooldown
    async def townOfSalem(self, context):
        if context.channel.name == "mrevilontwitch":
            await context.send("Add me on Town of Salem: MrEvilInSalem")

    @commands.command(name="clear")
    async def clear(self, context):
        if context.user.is_mod:
            try:
                await context.channel.clear()
            except TwitchIOBException:
                await context.send("The bot is not a mod on this channel. Unable to use the clear command")


if __name__ == "__main__":
    bot = Bot()
    bot.run()
