from twitchio.ext import commands
import time
import json
import asyncio
import requests
import threading
import types

# import the data.py file storing all the tokens and other neccessary info
import data

def cooldown(function, duration = int(30)) -> types.FunctionType:
    """
    Decorator for command functions.
    It adds a cooldown feature to the command decorated 
    which prevents it from being executed before a specified time has passed.
    The cooldown is implemented by launching a seperate thread with a sleep call 
    after the command is executed while not on cooldown, 
    which is stored in an internal variable of the command function
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

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(irc_token=data.OAUTH_TOKEN, 
            client_id=data.CLIENT_ID, 
            nick=data.BOT_NICK, 
            prefix=data.BOT_PREFIX, 
            initial_channels=data.CHANNELS)

    async def event_ready(self):
        print(f'Bot ready | {self.nick}')

    async def event_message(self, message):
        # remove messages with blacklisted words first, then execute the command if it isn't removed
        # ^ yet to be implemented
        await self.handle_commands(message)

    async def event_usernotice_subscription(self, data):
        if data.streak_months != 0:
            await data.channel.send(f"{data.user.name} has extended their sub-streak by one month. It's now at {data.streak_months} months!")

    @commands.command(name="test")
    @cooldown
    async def test(self, context):
        await context.send(f'Hello {context.author.name}')

    @commands.command(name="info")
    @cooldown
    async def info(self, context):
        await context.send("Following authentication problems this command is currently unavailable")
        #channel = bot.get_channel(data.CHANNELS[0])
        #if channel is not None:
        #    print(channel)
        #    stream = await channel.get_stream()
        #    for key, value in stream:
        #        await ctx.send(f'{key} : {value}')

    @commands.command(name="so")
    @cooldown
    async def shoutout(self, context):
        await context.send(f"{context.content}")
        message = context.content
        if len(message) > 4:
            target = message[3:]
            await context.send(f"Shoutout to {target}, who you might be able to find at https://twitch.tv/{target}!")


def check_user(name):
    # Example from twitch docs on how to get user info using userid
    """
    curl -X GET 'https://api.twitch.tv/helix/users?id=141981764' 
    -H 'Authorization: Bearer cfabdegwdoklmawdzdo98xt2fo512y' 
    -H 'Client-Id: uo6dggojyb8d6soh92zknwmi5ej1q2'
    """
    headers = {
        'Authorization' : data.OAUTH_TOKEN,
        'Client-Id' : data.CLIENT_ID
    }
    uid = None # get the user id coresponding to the name
    link = 'https://api.twitch.tv/helix/users?id='
    response =  requests.get(link+uid, headers=headers)
    del response

if __name__ == "__main__":
    bot = Bot()
    bot.run()