import asyncio
import random
from pyrogram.enums import ChatType
from pyrogram.errors import FloodWait
from PyroUbot import *

AG = {}

def emoji(alias):
    emojis = {
        "PROCES": "<emoji id=5080331039922980916>⚡️</emoji>",
        "AKTIF": "<emoji id=5080331039922980916>⚡️</emoji>",
        "SAKTIF": "<emoji id=5080331039922980916>⚡️</emoji>",
        "TTERSIMPAN": "<emoji id=4904714384149840580>💤</emoji>",
        "STOPB": "<emoji id=4918014360267260850>⛔️</emoji>",
        "SUCSESB": "<emoji id=5355051922862653659>🤖</emoji>",
        "BERHASIL": "<emoji id=5372917041193828849>🚀</emoji>",
        "GAGALA": "<emoji id=5332296662142434561>⛔️</emoji>",
        "DELAYY": "<emoji id=5438274168422409988>😐</emoji>",
        "BERHASILS": "<emoji id=5123293121043497777>✅</emoji>",
        "DELETES": "<emoji id=5902432207519093015>⚙️</emoji>",
        "STARS": "<emoji id=5080331039922980916>⚡️</emoji>",
        "PREM": "<emoji id=5893034681636491040>📱</emoji>",
        "PUTAR": "<emoji id=5372849966689566579>✈️</emoji>",
    }
    return emojis.get(alias, "🕸")


prcs = emoji("PROCES")
aktf = emoji("AKTIF")
saktf = emoji("SAKTIF")
ttsmp = emoji("TTERSIMPAN")
stopb = emoji("STOPB")
scsb = emoji("SUCSESB")
brhsl = emoji("BERHASIL")
ggla = emoji("GAGALA")
delayy = emoji("DELAYY")
brhsls = emoji("BERHASILS")
dlts = emoji("DELETES")
stars = emoji("STARS")
prem = emoji("PREM")
put = emoji("PUTAR")

async def run_autobc(client):
    """Loop utama AutoBC"""
    done, failed = 0, 0
    AG[client.me.id] = {"status": True}

    while AG[client.me.id]["status"]:
        delay = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)
        blacklist = await get_list_from_vars(client.me.id, "BL_ID")
        auto_texts = await get_auto_text(client.me.id)

        if not auto_texts:
            await client.send_message(client.me.id, f"<b><i>{ttsmp} Tidak ada pesan yang disimpan.</i></b>")
            AG[client.me.id]["status"] = False
            await set_vars(client.me.id, "AUTOBCAST", "off")
            return
        
        message_to_forward = random.choice(auto_texts)
        group = 0

        async for dialog in client.get_dialogs():
            if not AG[client.me.id]["status"]:
                await client.send_message(client.me.id, f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")
                return

            if (dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP) and 
                dialog.chat.id not in blacklist and 
                dialog.chat.id not in BLACKLIST_CHAT):
                try:
                    await client.forward_messages(dialog.chat.id, "me", message_to_forward)
                    group += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception:
                    failed += 1

        done += 1
        await client.send_message(
            client.me.id,
            f"""
<blockquote><b><i>
    {prem} ᴀᴜᴛᴏʙᴄ ᴘʀᴇᴍɪᴜᴍ {prem}\n
{scsb} • Broadcast Terkirim • {scsb}\n
{put} • Putaran ke : {done}\n
{brhsl} • Berhasil : {group} Chat\n
{ggla} • Gagal : {failed} Chat\n
{delayy} • Delay : {delay} Menit\n
{stars} ᴜsᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ {stars}</i></b></blockquote>
"""
        )
        await asyncio.sleep(60 * delay)


@PY.UBOT("autobc")
async def _(client, message):
    msg = await message.reply(f"<b><i>{prcs} Processing...</i></b>")
    type, value = extract_type_and_text(message)
    
    if type == "on":
        if AG.get(client.me.id, {}).get("status"):
            return await msg.edit(f"<b><i>{saktf} Auto Broadcast sudah aktif.</i></b>")

        await set_vars(client.me.id, "AUTOBCAST", "on")
        await msg.edit(f"<b><i>{aktf} Auto Broadcast diaktifkan.</i></b>")
        asyncio.create_task(run_autobc(client))

    elif type == "off":
        AG[client.me.id] = {"status": False}
        await set_vars(client.me.id, "AUTOBCAST", "off")
        return await msg.edit(f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")

    elif type == "delay":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Format salah! Gunakan .autobc delay [angka]</i></b>")
        await set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(f"<b><i>{delayy} Delay berhasil diatur ke {value} menit.</i></b>")

    # sisanya tetap sama (text, list, remove)


async def resume_autobc(client):
    """Dipanggil otomatis pas start ubot"""
    status = await get_vars(client.me.id, "AUTOBCAST")
    if status == "on":
        await client.send_message(client.me.id, f"📣 AutoBC aktif sebelum restart.\nMelanjutkan kembali...")
        asyncio.create_task(run_autobc(client))


@PY.UBOT("start")
async def start_handler(client, message):
    await resume_autobc(client)
    return await message.reply("✅ Bot sudah berjalan.")
