import random
import requests
from PyroUbot import *

__MODULE__ = "ʟᴜᴍɪɴ ᴀɪ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʟᴜᴍɪɴ ᴀɪ ⦫</b>
<blockquote>
⎆ perintah :
ᚗ <code>{0}lumin</code>
⊶ mengobrol dengan Lumin AI
</blockquote>
"""

@PY.UBOT("lumin")
async def _(client, message):
    try:
        if len(message.command) < 2:
            await message.reply_text(
                "<emoji id=5019523782004441717>❌</emoji> Mohon gunakan format yang benar.\nContoh: <code>.lumin halo</code>"
            )
            return

        prs = await message.reply_text("<emoji id=5319230516929502602>🔍</emoji> Menjawab...")
        query = message.text.split(' ', 1)[1]
        response = requests.get(f'https://api.diioffc.web.id/api/ai/luminai?query={query}')

        try:
            data = response.json()

            if "result" in data and "message" in data["result"]:
                x = data["result"]["message"]
                await prs.edit(f"<blockquote>{x}</blockquote>")
            else:
                await prs.edit("⛔ Respons API tidak memiliki data yang diharapkan.")
        except Exception as err:
            await prs.edit(f"⛔ Terjadi kesalahan saat memproses respons API: {err}")

    except Exception as e:
        await message.reply_text(f"⛔ Terjadi kesalahan: {e}")
