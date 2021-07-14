# What is this project
This is a personal project where I create a twitch chatbot for my own channel.  
The goal is to be completely independent from the bigger bots out there like nightbot, streamlabs, etc.  

# What is currently available:
- A decent amount of simple info commands
- Sending messages with a set interval
- Sending the current time of the host machine
- Sending a shoutout to a mentioned name. If the person with that
 name is currently live it'll add the current game. If no name is
 provided it falls back to a predetermined name

# How does all of this work?
The entire bot is based around the asyncronous Python module
[twitchio](https://pypi.org/project/twitchio/).  

# File structure
- main.py: Set up and start the bot. Is responsible for including all cogs
- cogs/ : The folder containing all sub-modules for the different functions
- authDetails.py(.template): Template file for the authentication details required for the bot to work
- usefulStuff.py: Contains functions and information that are used throughout the entire system

# Setup:
*Note*: All variables mentioned here can be found inside authDetails.py
1. Create an account on Twitch for your bot to use
2. Create an OAuth token that the bot will use at https://twitchapps.com/tmi
3. Rename `authDetails.py.template` to `authDetails.py`
4. Replace the value of the variable `OAUTH_TOKEN` with your own token
5. Create an Twitch app at https://dev.twitch.tv/ and then get the Client id of that app
6. Replace the value of the variable `CLIENT_ID` with your Client id
7. Set your bot's name as the value of `BOT_NICK`
8. Set your bot's prefix (the text that you want to be in front of commands) as the value of `BOT_PREFIX`
9. Add all channels that you want your bot to monitor to `CHANNELS`.

 (I recommend only adding channels where you have the permission from the owner)
10. Add your joincodes to the relevant variables
11. Install the required modules:
 - twitchio
 - requests


12. Done. Start it by using `python main.py` while in the root folder
