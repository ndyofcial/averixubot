import asyncio
import datetime

from PyroUbot import *

__MODULE__ = "ᴅᴏɴᴇ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴅᴏɴᴇ ⦫</b>

<blockquote>
⎆ Perintah :
ᚗ <code>{0}done</code> <b>[name item],[harga], [pembayaran]</b>
⊶ konfirmasi pembayaran

ᚗ <code>{0}proses</code> <b>[name item], [status]</b>
⊶ proses

ᚗ <code>{0}donep</code> <b>[name item], [status]</b>
⊶ proses selesai</blockquote>
"""

def emoji(alias):
    emojis = {
        "BARANG": "<emoji id=5463172695132745432>📦</emoji>",
        "RUPIAH": "<emoji id=5373174941095050893>💸</emoji>",
        "WAKTU": "<emoji id=5229045747130843073>🎖</emoji>",
        "PAY": "<emoji id=5463046637842608206>🪙</emoji>",
        "OWN": "<emoji id=5080331039922980916>⚡️</emoji>",
        "DONE": "<emoji id=6334447321257874711>✔️</emoji>",
        "THX": "<emoji id=5463256910851546817>🤝</emoji>",
        "EZ": "<emoji id=5372965329511139384>😎</emoji>",
        "LOAD": "<emoji id=5226702984204797593>🔄</emoji>",
        "TOP": "<emoji id=5463071033256848094>🔝</emoji>",
    }
    return emojis.get(alias, "Emoji tidak ditemukan.")


brg = emoji("BARANG")
rupiah = emoji("RUPIAH")
wkt = emoji("WAKTU")
pay = emoji("PAY")
own = emoji("OWN")
done = emoji("DONE")
thx = emoji("THX")
ez = emoji("EZ")
load = emoji("LOAD")
top = emoji("TOP")


@PY.UBOT("done")
async def done_command(client, message):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(5)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .done name item,price,payment</blockquote>")
            return

        parts = args[1].split(",", 2)

        if len(parts) < 2:
            await message.reply_text("<blockquote>Penggunaan: .done name item,price,payment</blockquote>")
            return

        name_item = parts[0].strip()
        price = parts[1].strip()
        payment = parts[2].strip() if len(parts) > 2 else "Lainnya"
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>{done}「 𝗣𝗘𝗠𝗕𝗔𝗬𝗔𝗥𝗔𝗡 𝗗𝗜𝗧𝗘𝗥𝗜𝗠𝗔 」 {done}\n</blockquote>"
            f"<blockquote>{brg} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{rupiah} <b>ɴᴏᴍɪɴᴀʟ : {price}</b>\n"
            f"{wkt} <b>ᴡᴀᴋᴛᴜ : {time}</b>\n"
            f"{pay} <b>ᴘᴀʏᴍᴇɴᴛ : {payment}</b>\n</blockquote>"
            f"<blockquote>{thx} ᴛᴇʀɪᴍᴀᴋᴀsɪʜ ᴛᴇʟᴀʜ ᴏʀᴅᴇʀ\n {load} ᴘᴇsᴀɴᴀɴ sᴇɢᴇʀᴀ ᴅɪᴘʀᴏsᴇs\n</blockquote>"
            f"<blockquote>{own} ʙʏ : <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")

@PY.UBOT("proses")
async def donel_command(client, message):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(5)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 1 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .proses nameitem, status</blockquote>")
            return

        parts = args[1].split(",", 1)

        if len(parts) < 1:
            await message.reply_text("<blockquote>Penggunaan: .done nameitem, status</blockquote>")
            return

        name_item = parts[0].strip()
        status = parts[1].strip()
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>{ez}「 𝗣𝗥𝗢𝗦𝗘𝗦 𝗢𝗥𝗗𝗘𝗥 」 {ez}\n</blockquote>"
            f"<blockquote>{brg} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{wkt} <b>ᴡᴀᴋᴛᴜ : {time}</b>\n"
            f"{ez} <b>sᴛᴀᴛᴜs : {status}</b>\n</blockquote>"
            f"<blockquote>{own} ʙʏ : <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")
        


@PY.UBOT("donep")
async def donel_command(client, message):
    izzy_ganteng = await message.reply("<blockquote>memproses...</blockquote>")
    await asyncio.sleep(5)
    try:
        args = message.text.split(" ", 1)
        if len(args) < 1 or "," not in args[1]:
            await message.reply_text("<blockquote>Penggunaan: .donep nameitem, status</blockquote>")
            return

        parts = args[1].split(",", 1)

        if len(parts) < 1:
            await message.reply_text("<blockquote>Penggunaan: .done nameitem, status</blockquote>")
            return

        name_item = parts[0].strip()
        status = parts[1].strip()
        time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        response = (
            f"<blockquote>{ez}「 𝗣𝗥𝗢𝗦𝗘𝗦 𝗧𝗥𝗔𝗡𝗦𝗔𝗞𝗦𝗜 𝗕𝗘𝗥𝗛𝗔𝗦𝗜𝗟 」 {ez}\n</blockquote>"
            f"<blockquote>{brg} <b>ʙᴀʀᴀɴɢ : {name_item}</b>\n"
            f"{wkt} <b>ᴡᴀᴋᴛᴜ : {time}</b>\n"
            f"{ez} <b>sᴛᴀᴛᴜs : {status}</b>\n</blockquote>"
            f"<blockquote>{thx} ᴛᴇʀɪᴍᴀᴋᴀsɪʜ ᴛᴇʟᴀʜ ᴏʀᴅᴇʀ\n {top} ᴘʀᴏsᴇs ᴘᴇsᴀɴᴀɴ ᴛᴇʟᴀʜ sᴇʟᴇsᴀɪ\n</blockquote>"
            f"<blockquote>{own} ʙʏ : <a href=tg://user?id={message.from_user.id}>{message.from_user.first_name} {message.from_user.last_name or ''}</a></blockquote>"
        )
        await izzy_ganteng.edit(response)

    except Exception as e:
        await izzy_ganteng.edit(f"error: {e}")
