from twitchio.ext import commands
import time
import json
import asyncio
import requests
import threading
import types

# import the data.py file storing all the tokens and other neccessary info
import data as authData

def cooldown(function, duration = int(30)) -> types.FunctionType:
    """
    Cooldown decorator for command functions

    Optional argument: duration = integer

    How it works: Launches a timing thread utilizing sleep when the command is called.
    And until that thread finishes the internal on_cooldown variable will prevent another call of the function
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

def receiveBannedWordList():
    try:
        request = requests.get("http://localhost:5000/api/alpha/get/bannedWords")
    except requests.exceptions.ConnectionError:
        return set()
    if request.status_code != 200:
        return set()
    data = request.json()
    returner = set(data)
    return returner

def iterateThroughDict(dictionary, funtionToExecute):
    for key in dictionary:
        if type(dictionary[key]) is dict:
            iterateThroughDict(dictionary[key], funtionToExecute)
        else:
            funtionToExecute((key, dictionary[key]))

async def asyncIterateThroughDict(dictionary, asyncFunction, *, functionIsAsync=True):
    for key in dictionary:
        if type(dictionary[key]) is dict:
            await asyncIterateThroughDict(dictionary[key], asyncFunction, functionIsAsync=functionIsAsync)
        else:
            if functionIsAsync:
                await asyncFunction((key, dictionary[key]))
            else:
                asyncFunction((key, dictionary))
class Bot(commands.Bot):

    bannedWords = set()

    def __init__(self):
        super().__init__(irc_token=authData.OAUTH_TOKEN,
            client_id=authData.CLIENT_ID,
            nick=authData.BOT_NICK,
            prefix=authData.BOT_PREFIX,
            initial_channels=authData.CHANNELS)
        self.bannedWords = receiveBannedWordList()

    async def event_ready(self):
        print(f'Bot ready | {self.nick}')

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
        if data.streak_months != None:
            apiData["streak"] = data.streak_months
        else:
            apiData["streak"] = 0
        if data.streak_months != 0:
            await data.channel.send(f'{data.user.name} has extended their sub-streak on tier {apiData["tier"]} by one month. It\'s now at {data.streak_months} months!')
        else:
            await data.channel.send(f'{data.user.name} has just subscribed on tier {apiData["tier"]}')

    @commands.command(name="test")
    #@cooldown
    async def test(self, context):
        await context.send(f'Hello {context.author.name}')

    @commands.command(name="info")
    #@cooldown
    async def info(self, context):
        """
        Grabs the publicly available information of the stream chat is has been called from and prints it to console output
        """
        #stream = authData.getStreamInfo()
        #print(stream)
        #print("----------------------------")
        print(context.channel.name)
        await asyncIterateThroughDict(authData.getStreamInfo(context.channel.name.lower()), print, functionIsAsync=False)
        await context.send("worked")

    @commands.command(name="so")
    #@cooldown
    async def shoutout(self, context):
        await context.send(f"{context.content}")
        message = context.content
        if len(message) > 4:
            target = message[4:]
            print(target)
            await context.send(f"Shoutout to {target}, who you might be able to find at https://twitch.tv/{target}!")
            await context.send("Also, blame the helix api for no last game checking")

    @commands.command(name="Discord")
    #@cooldown
    async def discord(self, context):
        await context.send("It seems that you are interested in our Discord server. You can join over here: discord.gg/3a4ZseU")

    @commands.command(name="DestinyJoin")
    #@cooldown
    async def destinyJoin(self, context):
        await context.send("If you want to join me with your guardian (and my fireteam settings are on public), you can use this joincode: 76561198078422715")

    @commands.command(name="TownOfSalem")
    #@cooldown
    async def townOfSalem(self, context):
        await context.send("Add me on Town of Salem: MrEvilInSalem")

    @commands.command(name="clear")
    async def clear(self, context):
        if context.user.is_mod:
            await context.channel.clear()

if __name__ == "__main__":
    bot = Bot()
    bot.run()
