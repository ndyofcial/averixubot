from PyroUbot import *
import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

__MODULE__ = "ᴄʟᴀᴜᴅᴇ ᴀɪ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄʟᴀᴜᴅᴇ ᴀɪ ⦫</b>
<blockquote>⎆ perintah :
ᚗ <code>{0}claude</code> text
⊶ buat pertanyaan contoh <code>{0}claude</code> bagaimana cuaca besok?</blockquote>
"""

@PY.UBOT("claude")
@PY.TOP_CMD
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .claude hai"
            )
        else:
            prs = await message.reply_text(f"<emoji id=5316770651720137011>🔘</emoji> Menjawab....")
            hai = message.text.split(' ', 1)[1]
            response = requests.get(f'https://vapis.my.id/api/claude?q={hai}')

            try:
                if "result" in response.json():
                    x = response.json()["result"]                  
                    await prs.edit(
                      f"<blockquote>{x}</blockquote>"
                    )
                else:
                    await message.reply_text("No 'results' key found in the response.")
            except KeyError:
                await message.reply_text("Error accessing the response.")
    except Exception as e:
        await message.reply_text(f"{e}")
      
