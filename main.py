from twitchio.ext import commands
from twitchio.errors import *
from twitchio import dataclasses
import time
import asyncio
import requests
import threading
import types
import inspect
import json
import os

# import the data.py file storing all the tokens and other neccessary info
import authDetails
from usefulStuff import collector

import const_messages as messages

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
    for i in authDetails.CHANNELS:
        if i.lower() == channel.lower():
            raise ValueError
    loop = asyncio.get_event_loop()
    loop.create_task(Bot.get_channel(channel).send(message))


class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=authDetails.OAUTH_TOKEN,
                         client_id=authDetails.CLIENT_ID,
                         nick=authDetails.BOT_NICK,
                         prefix=authDetails.BOT_PREFIX,
                         initial_channels=authDetails.CHANNELS)

    async def sendRepeatedMessage(self,
                                  channel="MrEvilOnTwitch",
                                  message=str, delay=120,
                                  loop=asyncio.get_event_loop()):
        channel_obj = self.get_channel(channel)
        await asyncio.sleep(delay)
        if collector.getStreamInfo(channel) != collector.offlineData:
            await channel_obj.send(message)
        loop.create_task(self.sendRepeatedMessage(channel=channel, message=message, delay=delay, loop=loop))

    async def event_ready(self):
        print(f'Bot ready | {self.nick}')
        await self.sendRepeatedMessage("MrEvilOnTwitch", messages.commands, delay=30)

#    async def event_message(self, message):
#        # remove messages with blacklisted words first, then execute the command if it isn't removed
#        # ^ yet to be implemented
#        await self.handle_commands(message)

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
        apiData["name"] = data.user.name
        apiData["id"] = data.user.id
        apiData["channel"] = data.channel.name
        if data.streak_months != 0:
            await data.channel.send(f'{data.user.name} has extended their sub-streak on tier {apiData["tier"]} by one month. It\'s now at {data.streak_months} months!')
        else:
            await data.channel.send(f'{data.user.name} has just subscribed on tier {apiData["tier"]}')

if __name__ == "__main__":
    bot = Bot()
    for i in [j[:-3] for j in os.listdir("./cogs") if j[-2:] == "py"]:
        bot.load_module("cogs." + i)
    bot.run()
