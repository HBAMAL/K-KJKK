import os

class Config(object):
	BOT_TOKEN = os.environ.get("BOT_TOKEN")
	APP_ID = int(os.environ.get("APP_ID"))
	API_HASH = os.environ.get("API_HASH")
	DATABASE_URL = os.environ.get("DATABASE_URL")
	SUDO_USERS = list(set(int(x) for x in ''.split()))
	SUDO_USERS.append(853393439)
	SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",
        "**USE THIS COMMANDS IN GROUP \n\n /ForceSubscribe - To get the current settings\n\n /ForceSubscribe no/off/disable - To turn of ForceSubscribe\n\n/ForceSubscribe clear - To unmute all members\n\n /ForceSubscribe (channel username) - To turn on and setup the channel.**"
      ]

      START_MSG = "**HLO [π [{}](tg://user?id={})**\n\nβ I CAN FORCE MEMBERS TO JOIN YOUR CHANNEL\n\nMADE BY @TELSABOTS"
      
      ABOUT_MSG = "π€**BOT:FORCE SUB π€**\n\nπ’**CHANNEL : @TELSABOTS'\n\nπ§πΌβπ»DEVπ§πΌβπ»: @ALLUADDICT"

