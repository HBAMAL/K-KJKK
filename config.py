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
        "[👨‍💻] **DEVELOPED BY @doreamonfans1**"
      ]

      START_MSG = "**HLO [👋] [{}](tg://user?id={})**\n\n● I CAN FORCE MEMBERS TO JOIN YOUR CHANNEL\n\nMADE BY @TELSABOTS"
