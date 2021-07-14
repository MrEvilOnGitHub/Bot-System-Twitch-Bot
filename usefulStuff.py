import threading
import time
from requests import get

class collector:

    offlineData = {'data': [], 'pagination': {}}

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
                collector.iterateThroughDict(dictionary[key], funtionToExecute)
            else:
                funtionToExecute((key, dictionary[key]))


    async def asyncIterateThroughDict(dictionary,
                                      asyncFunction,
                                      functionIsAsync=True):
        for key in dictionary:
            if type(dictionary[key]) is dict:
                await collector.asyncIterateThroughDict(dictionary[key], asyncFunction, functionIsAsync=functionIsAsync)
            else:
                if functionIsAsync:
                    await asyncFunction((key, dictionary[key]))
                else:
                    asyncFunction((key, dictionary))

    def getStreamInfo(stream="mrevilontwitch") -> dict:
        """Optional argument:
        - stream: channel name of the twitch stream you want to pull data from

        returns:
        - Set of the json-formated data received from the twitch api endpoint used (helix)
        """
        url = f"https://api.twitch.tv/helix/streams?user_login={stream}"
        data = {
            "Client-Id": "YourClientID",
            "Authorization": "YourBearerToken"
            }
        r = get(url, headers=data)
        return r.json()
