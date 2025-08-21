import aiohttp
import os
import filetype
from pyrogram import Client, filters
from pyrogram.types import Message
from PyroUbot import *

#__MODULE__ = "ʀᴇᴍᴏᴠᴇ ᴡᴍ"
#__HELP__ = """
#<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʀᴇᴍᴏᴠᴇ ᴡᴍ ⦫</b>
#<blockquote>⎆ perintah :
#ᚗ <code>{0}removewm</code> reply picture
#⊶ untuk menghapus watermark sebuah picture.</blockquote>
#"""

async def upload_media(m: Message):
    media = await m.reply_to_message.download()
    try:
        with open(media, "rb") as file:
            file_data = file.read()
            ext = filetype.guess_extension(file_data) or "jpg"
            
        form_data = aiohttp.FormData()
        form_data.add_field("fileToUpload", open(media, "rb"), filename=f"file.{ext}")
        form_data.add_field("reqtype", "fileupload")
        
        async with aiohttp.ClientSession() as session:
            async with session.post("https://catbox.moe/user/api.php", data=form_data) as res:
                if res.status == 200:
                    url = await res.text()
                    return url.strip()
                else:
                    return None
    finally:
        os.remove(media)

@PY.UBOT("hde")
async def remove_watermark(client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.photo:
        await message.reply_text("Reply ke foto yang ingin di HD.")
        return
    
    await message.reply_text("Proses...")

    url = await upload_media(message)
    if not url:
        await message.reply_text("Gagal mengunggah gambar.")
        return
#https://api.botcahx.eu.org/api/tools/remini-v3?url=https://telegra.ph/file/82af204d1258df1d52cac.jpg&resolusi=4&apikey=moire_mor
    api_url = f"https://api.botcahx.eu.org/api/tools/remini-v3?url={url}&resolusi=4&apikey=moire_mor"
    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as res:
            if res.status == 200:
                image_data = await res.read()
                image_path = "no_watermark.jpg"
                
                with open(image_path, "wb") as f:
                    f.write(image_data)

                await message.reply_photo(image_path, caption="✅ Image berhasil di HD.")
                os.remove(image_path)
            else:
                await message.reply_text("Terjadi kesalahan saat menghubungi API.")
