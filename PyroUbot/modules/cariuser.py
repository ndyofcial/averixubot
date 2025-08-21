from pyrogram import Client, filters
from pyrogram import *
from PyroUbot import PY

__MODULE__ = "ᴄᴀʀɪ ᴜsᴇʀɴᴀᴍᴇ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴀʀɪ ᴜsᴇʀɴᴀᴍᴇ ⦫<b>

<blockquote>⎆ perintah :
ᚗ <code>{0}cuser</code> username
⊷ mencari username di berbagai platform sosial media.
</blockquote>
"""

@PY.UBOT("cuser")
@PY.TOP_CMD
async def cek_user_command(client, message):
    # Ambil argumen dari pesan
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.reply_text(
            "<blockquote><b>⛔ Gunakan format: cuser [username]</b></blockquote>"
        )
        return

    username = args[1]
    platforms = {
        "🔹 GitHub": f"https://github.com/{username}",
        "🔹 Instagram": f"https://www.instagram.com/{username}",
        "🔹 Facebook": f"https://www.facebook.com/{username}",
        "🔹 Twitter/X": f"https://x.com/{username}",
        "🔹 TikTok": f"https://www.tiktok.com/@{username}",
        "🔹 Telegram": f"https://t.me/{username}"
    }

    result_text = f"🔍 **Hasil Pencarian untuk Username:** `{username}`\n\n"
    result_text += "\n".join([f"{platform}: [Klik disini]({link})" for platform, link in platforms.items()])

    await message.reply_text(result_text, disable_web_page_preview=True)
