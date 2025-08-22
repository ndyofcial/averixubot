import os
from dotenv import load_dotenv

load_dotenv(".env")

MAX_BOT = int(os.getenv("MAX_BOT", "100"))

DEVS = list(map(int, os.getenv("DEVS", "5850202522").split()))

API_ID = int(os.getenv("API_ID", "23117267"))

API_HASH = os.getenv("API_HASH", "0e3230b3f1f8c32d66b95fa1853a5b26")

BOT_TOKEN = os.getenv("BOT_TOKEN", "8076346528:AAGmUdPs-Ip7OXSkqQFZumNAKAS0Ug0cRjQ")

OWNER_ID = int(os.getenv("OWNER_ID", "5850202522"))

BLACKLIST_CHAT = list(map(int, os.getenv("BLACKLIST_CHAT", "-1002125842026 -1002053287763 -1002044997044 -1002022625433 -1002050846285 -1002400165299 -1002416419679 -1001473548283").split()))

RMBG_API = os.getenv("RMBG_API", "ybwGCgqJngeYGQLiWAjxrYoz")

MONGO_URL = os.getenv("MONGO_URL", "mongodb+srv://ndyuserbot:ndyuserbot@cluster0.wvdpaip.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

LOGS_MAKER_UBOT = os.getenv("LOGS_MAKER_UBOT", "-1002791340508")

USER_GROUP = os.getenv("USER_GROUP", "@INFORMATIONNDY")
