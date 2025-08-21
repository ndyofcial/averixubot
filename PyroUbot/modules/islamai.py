from PyroUbot import *
import random
import requests
from pyrogram.enums import ChatAction, ParseMode
from pyrogram import filters
from pyrogram.types import Message

__MODULE__ = "ɪsʟᴀᴍ ᴀɪ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɪsʟᴀᴍ ᴀɪ ⦫<b>

<blockquote>⎆ perintah :
ᚗ <code>{0}islamai</code> username
⊷ Ai khusus bertanya tentang Agama Islsam.

⎆ Contoh :
ᚗ <code>{0}islamai</code> asal usul Alquran.</blockquote>
"""

@PY.UBOT("islamai")
@PY.TOP_CMD
async def chat_gpt(client, message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji>mohon gunakan format\ncontoh : .islamai asal usul al-quran"
            )
        else:
            prs = await message.reply_text(f"<emoji id=4943239162758169437>🤩</emoji>Menjawab....")
            hai = message.text.split(' ', 1)[1]
            response = requests.get(f'https://vapis.my.id/api/islamai?q={hai}')

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
      
