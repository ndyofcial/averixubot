import os
from PIL import Image, ImageDraw, ImageFont, ImageOps
from pyrogram import Client
from pyrogram.types import Message, User, Chat
from PyroUbot import *
from io import BytesIO

__MODULE__ = "ᴄᴇᴋ ɪᴅ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴇᴋ ɪᴅ ⦫</b>
<blockquote>⎆ perintah :
ᚗ <code>{0}cekid</code>
⊶ Untuk Mengambil Data User/Channel/Grup.
</blockquote>
<blockquote>⎆ perintah :
ᚗ <code>{0}id</code>
⊶ Untuk Mengambil Data User
</blockquote>
"""

@PY.UBOT("id|cekid")
async def cekidte(client, message):
    user = message.from_user
    target_user = user

    # Kalau reply ke orang, ambil user dari reply
    if message.reply_to_message and message.reply_to_message.from_user:
        target_user = message.reply_to_message.from_user

    # Kalau ada argumen username/ID di perintah
    elif len(message.command) > 1:
        try:
            target_user = await client.get_users(message.command[1])
        except:
            return await message.reply("<b>❌ Pengguna tidak ditemukan</b>")

    # Nama chat untuk group/channel
    chat_title = message.chat.title if isinstance(message.chat, Chat) else "Private Chat"
    username_text = f"@{target_user.username}" if target_user.username else "Tidak ada"

    digit_info = f"({len(str(target_user.id))} digit)"
    msg_id_text = f"<code>{message.id}</code>"  # Tambahan Msg ID

    msg = f"""
</blockquote><b>✉️ Msg ID:</b> {msg_id_text}
<b>👤 Nama:</b> {target_user.first_name}
<b>🔗 Username:</b> {username_text}
<b>🆔 User ID:</b> <code>{target_user.id}</code> {digit_info}
<b>💬 Chat ID:</b> <code>{message.chat.id}</code> ({chat_title})</blockquote>
"""

    await message.reply(msg, quote=True)