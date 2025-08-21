import os
import json
import asyncio
import psutil
# import speedtest
from speedtest import Speedtest
import random

from datetime import datetime
from gc import get_objects
from time import time

from pyrogram.raw import *
from pyrogram.raw.functions import Ping
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PyroUbot import *

__MODULE__ = "ʜᴀᴄᴋ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʜᴀᴄᴋ ⦫</b>

<blockquote>⎆ perintah :

ᚗ <code>{0}hack</code>

ᚗ Anim Hack just for fun</blockquote>

"""


async def _(client, message):
    start = datetime.now()
    await client.invoke(Ping(ping_id=0))
    end = datetime.now()
    uptime = await get_time((time() - start_time))
    delta_ping_formatted = round((end - start).microseconds / 10000, 2)
    pong = await EMO.PING(client)
    tion = await EMO.MENTION(client)
    yubot = await EMO.UBOT(client)
    pantek = await STR.PONG(client)
    ngentod = await STR.OWNER(client)
    kontol = await STR.UBOT(client)
    devs = await STR.DEVS(client)
    babi = client.me.is_premium
    if babi:
        _ping = f"""
<blockquote>{pong} {pantek} : {str(delta_ping_formatted).replace('.', ',')} ms
{tion} {ngentod} : <code>{client.me.mention}</code>
{yubot} {kontol} : <code>{bot.me.mention}</code></blockquote>

<blockquote><b>ᣃ࿈ ᴜsᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ࿈ᣄ</b></blockquote>"""
        await message.reply(_ping)
    else:
        _ping = f"""
<blockquote>{pantek} : {str(delta_ping_formatted).replace('.', ',')} ms
{ngentod} : <code>{client.me.mention}</code>
{kontol} : <code>{bot.me.mention}</code></blockquote>

<blockquote><b>ᣃ࿈ ᴜsᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ ࿈ᣄ</b></blockquote>"""
        await message.reply(_ping)

@PY.UBOT("hack")
@PY.TOP_CMD
async def hack(event):
    range(0, 11)
    await event.edit("Installing.")
    await event.edit("Installing..")
    await event.edit("Installing...")
    await event.edit("Installing....")
    await asyncio.sleep(3)
    await event.edit("`Installing Files To Hacked Private Server...`")
    await asyncio.sleep(3)
    await event.edit("`Target Selected.`")
    await asyncio.sleep(4)
    await event.edit("`Installing... 0%\n▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
    await asyncio.sleep(3)
    await event.edit("`Installing... 4%\n█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
    await asyncio.sleep(2)
    await event.edit("`Installing... 8%\n██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
    await asyncio.sleep(3)
    await event.edit("`lnstallig... 20%\n█████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
    await asyncio.sleep(2)
    await event.edit("`Installing... 36%\n█████████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒ `")
    await asyncio.sleep(3)
    await event.edit("`Installing... 52%\n█████████████▒▒▒▒▒▒▒▒▒▒▒▒ `")
    await asyncio.sleep(2)
    await event.edit("`Installing... 84%\n█████████████████████▒▒▒▒ `")
    await asyncio.sleep(2)
    await event.edit("`Installing... 100%\n████████Installed██████████ `")
    await asyncio.sleep(2)
    await event.edit("`Target files Uploading...\n\nDirecting To Remote  server to hack..`")
    await asyncio.sleep(3)
    await event.edit("Connecting nd getting combined token from my.telegram.org ")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~#` ")
    await asyncio.sleep(2)
    await event.edit("`root@anon:~# ls`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~#`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # S`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So L`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Le`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let'`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's `")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's H`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Ha`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hac`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack `")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack i`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it `")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it .`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ..`")
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# `")
    await asyncio.sleep(2)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py`")
    await asyncio.sleep(2)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...`")
    await asyncio.sleep(2)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@anon:~# trap whoami`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@anon:~# trap whoami\n\nwhoami=user`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...`")
    await asyncio.sleep(3)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nVictim detected in ghost ...`")
    await asyncio.sleep(2)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nVictim detected in ghost ...\n\nAll Done!`")
    await asyncio.sleep(2)
    await event.edit("`root@anon:~# ls\n\n  usr  ghost  codes  \n\nroot@aono:~# # So Let's Hack it ...\nroot@anon:~# python setup.py\n\nsetup.py deployed ...\nAuto CMD deployed ...\n\nroot@anon:~# trap whoami\n\nwhoami=user\nboost_trap on force ...\nVictim detected  in ghost ...\n\nAll Done!\nInstalling Token!\nToken=`DJ65gulO90P90nlkm65dRfc8I`")
    await asyncio.sleep(3)
    await event.edit("`starting telegram hack`")
    await asyncio.sleep(2)
    await event.edit("`Hacking... 0%completed.\nTERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (1.3) kB`")
    await asyncio.sleep(3)
    await event.edit(" `Hacking... 4% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\n Collecting Data Package`")
    await asyncio.sleep(2)
    await event.edit("`Hacking.....6% completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\n Collecting Data Package seeing target account chat\n lding chat tg-bot bruteforce finished`")
    await asyncio.sleep(2)
    await event.edit("`Hacking.....8%completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\n Collecting Data Package seeing target account chat\n lding chat tg-bot bruteforce finished\n creating pdf of chat`")
    await asyncio.sleep(3)
    await event.edit("`Hacking....15%completed\n Terminal:Chat history from telegram exporting to private database.\n Terminal 874379gvrfghhuu5tlotruhi5rbh installing`")
    await asyncio.sleep(3)
    await event.edit("`Hacking....24%completed\n TERMINAL:\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package seeing target account chat\n lding chat tg-bot bruteforce finished\nerminal:chat history from telegram exporting to private database.\n terminal 874379gvrfghhuu5tlotruhi5rbh installed\n Creating data into pdf`")
    await asyncio.sleep(2)
    await event.edit("`Hacking....32%completed\n looking for use history \n downloading-telegram -id prtggtgf . gfr (12.99 mb)\n Collecting data starting imprute attack to user account\n Chat history from telegram exporting to private database.\n Terminal 874379gvrfghhuu5tlotruhi5rbh installed\n Creted data into pdf\n Download sucessful Bruteforce-Telegram-0.1.tar.gz (1.3)`")
    await asyncio.sleep(3)
    await event.edit("Hacking....38%completed\n\nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e`")
    await asyncio.sleep(3)
    await event.edit("`Hacking....52%completed\nexterting data from telegram private server\ndone with status 36748hdeg\n checking for more data in device`")
    await asyncio.sleep(2)
    await event.edit("`Hacking....60%completed\nmore data found im target device\npreparing to download data\n process started with status 7y75hsgdt365ege56es\n status changed to up`")
    await asyncio.sleep(2)
    await event.edit("`Hacking....73% completed\n Downloading data from device\n process completed with status 884hfhjh\nDownloading-0.1.tar.gz (9.3 kB)\n Collecting Data Packageseeing target\n lding chat tg-bot bruteforce finished\n creating pdf of chat`")
    await asyncio.sleep(3)
    await event.edit("`Hacking...88%completed\nall data from telegram private server downloaded\nterminal download sucessfull--with status jh3233fdg66y yr4vv.irh\n data collected from tg-bot\n TERMINAL:\n Bruteforce-Telegram-0.1.tar.gz (1.3)downloaded`")
    await asyncio.sleep(2)
    await event.edit("`100%\n█████████HACKED███████████ `\n\n\n  TERMINAL: \nDownloading Bruteforce-Telegram-0.1.tar.gz (9.3 kB)\nCollecting Data Package\n  Downloading Telegram-Data-Sniffer-7.1.1-py2.py3-none-any.whl (82 kB)\nBuilding wheel for Tg-Bruteforcing (setup.py): finished with status 'done'\nCreated wheel for telegram: filename=Telegram-Data-Sniffer-0.0.1-py3-none-any.whl size=1306 sha256=cb224caad7fe01a6649188c62303cd4697c1869fa12d280570bb6ac6a88e6b7e\n  Stored in directory: `")
    await asyncio.sleep(3)
    await event.edit("`Accoount hacked\n Collecting all data\n converting data into PDF`")
    await asyncio.sleep(3)
    await event.edit("PDF Created Click Link Below to Download Data`\n\n`Don't Worry Only i Can Open This File 😎😎..\nIf u don't Believe try to Download 🙂")
