from pyrogram import Client, filters
import requests
from PyroUbot import *

__MODULE__ = "ᴛᴛ sᴇᴀʀᴄʜ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴛɪᴋᴛᴏᴋ sᴇᴀʀᴄʜ ⦫</b>
<blockquote><b>
⎆ Perintah :
ᚗ <code>{0}ttsearch</code> Text
⊶ Mencari video tiktok.</b></blockquote>
"""

API_KEY = "moire_mor"

@PY.UBOT("ttsearch")
async def tiktok_search(client, message):
    if len(message.command) < 2:
        return await message.reply("<blockquote><b>⛔ Gunakan: `.ttsearch query`</b></blockquote>")

    query = " ".join(message.command[1:])
    proses_msg = await message.reply("<blockquote><b>🌀 **Sedang mencari video TikTok...**</b></blockquote>")

    url = f"https://api.botcahx.eu.org/api/search/tiktoks?query={query}&apikey={API_KEY}"
    response = requests.get(url)

    if response.status_code != 200:
        return await proses_msg.edit("<blockquote><b>⛔ **Gagal mengambil data dari API.**</b></blockquote>")

    data = response.json()
    if not data.get("status") or not data.get("result", {}).get("data"):
        return await proses_msg.edit("<blockquote><b>⛔ **Tidak ditemukan video untuk query tersebut.**</b></blockquote>")

    video = data["result"]["data"][0]
    caption = (f"""
<blockquote>💠 Judul: {video['title']}
🌐 Wilayah: {video['region']}
🎶 **Musik: {video['music_info']['title']} - {video['music_info']['author']}
🔊 **Jumlah Putar: {video['play_count']}
🩶 Like: {video['digg_count']}
💢 Komentar: {video['comment_count']}
🔰 **[Tonton di TikTok]({video['play']})</blockquote>"
"""   )

    await proses_msg.edit("<blockquote><b>💫 **Mengunduh video...**</b></blockquote>")

    await message.reply_video(video["play"], caption=caption)

    await proses_msg.delete()
