import asyncio
import random
from gc import get_objects
from asyncio import sleep
from pyrogram.raw.functions.messages import DeleteHistory, StartBot
from pyrogram.errors.exceptions import *
from pyrogram.errors.exceptions.not_acceptable_406 import ChannelPrivate

from PyroUbot import *

__MODULE__ = "ᴀᴜᴛᴏ ғᴏʀᴡᴀʀᴅ"
__HELP__ = """
<b> ⦪ Bantuan untuk Auto Forward ⦫</b>

<blockquote><b>⎆ Perintah :</blockquote></b>
<blockquote>{0}autofw on [Reply chat]
⊷ <i>Mengaktifkan Broadcast Autofw.</i></blockquote>
<blockquote>{0}autofw off
⊷ <i>Menonaktifkan Broadcast Autofw.</i></blockquote>
<blockquote>{0}autofw delay [Angka]
⊷ <i>Mengatur Delay Broadcast Autofw.</i></blockquote>
"""

def emoji(alias):
    emojis = {
        "PROCES": "<emoji id=5080331039922980916>⚡️</emoji>",
        "AKTIF": "<emoji id=5080331039922980916>⚡️</emoji>",
        "SAKTIF": "<emoji id=5080331039922980916>⚡️</emoji>",        
        "TTERSIMPAN": "<emoji id=4904714384149840580>💤</emoji>",
        "STOPB": "<emoji id=4918014360267260850>⛔️</emoji>",
        "SUCSESB": "<emoji id=5355051922862653659>🤖</emoji>",
        "BERHASIL": "<emoji id=5372917041193828849>🚀</emoji>",
        "GAGALA": "<emoji id=5134457377428341766>🕸</emoji>",
        "DELAYY": "<emoji id=5123293121043497777>💦</emoji>",
        "BERHASILS": "<emoji id=5123293121043497777>✅</emoji>",
        "DELETES": "<emoji id=5902432207519093015>⚙️</emoji>",
        "STARS": "<emoji id=5080331039922980916>⚡️</emoji>",
        "PREM": "<emoji id=5893034681636491040>📱</emoji>",
        "PUTR": "<emoji id=5895770017458294953>💫</emoji>",
    }
    return emojis.get(alias, "🕸")

prcs = emoji("PROCES")
aktf = emoji("AKTIF")
saktf = emoji("SAKTIF")
ttsmp = emoji("TTERSIMPAN")
stopb = emoji("STOPB")
scsb = emoji("SUCSESB")
brhsll = emoji("BERHASIL")
ggla = emoji("GAGALA")
delayy = emoji("DELAYY")
brhsls = emoji("BERHASILS")
dlts = emoji("DELETES")
stars = emoji("STARS")
prem = emoji("PREM")
putr = emoji("PUTR")


AG = []

@PY.UBOT("autofw")
@PY.TOP_CMD
async def _(client, message):
    prs = await EMO.PROSES(client)
    brhsl = await EMO.BERHASIL(client)
    bcs = await EMO.BROADCAST(client)
    mng = await EMO.MENUNGGU(client)
    ggl = await EMO.GAGAL(client)
    msg = await message.reply(f"<blockquote><b>{prs} Proses...</blockquote></b>")
    type, value = extract_type_and_text(message)

    if type == "on":
        if not message.reply_to_message:
            return await msg.edit(f"<blockquote><b>{ggl} Harap Reply chat Yang Ingin Di Forward</blockquote></b>")
            
        if client.me.id not in AG:
            await msg.edit(f"<blockquote><b>{brhsl} Autofw Aktif</blockquote></b>")
            AG.append(client.me.id)
            
            # Simpan info pesan yang akan diforward
            source_chat = message.reply_to_message.chat.id
            source_msg = message.reply_to_message.id
            await set_vars(client.me.id, "FORWARD_INFO", {"chat_id": source_chat, "message_id": source_msg})

            done = 0
            while client.me.id in AG:
                try:
                    delay = await get_vars(client.me.id, "DELAY_GCAST") or 1
                    blacklist = await get_list_from_vars(client.me.id, "BL_ID")
                    forward_info = await get_vars(client.me.id, "FORWARD_INFO")
                    
                    if not forward_info:
                        AG.remove(client.me.id)
                        return await msg.edit(f"<blockquote><b>{ggl} Gagal : Text Forward Tidak Di Temukan</blockquote></b>")

                    group = 0
                    async for dialog in client.get_dialogs():
                        if (
                            dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
                            and dialog.chat.id not in blacklist
                        ):
                            try:
                                await client.forward_messages(
                                    dialog.chat.id,
                                    forward_info["chat_id"],
                                    forward_info["message_id"]
                                )
                                group += 1
                                await asyncio.sleep(1)
                            except FloodWait as e:
                                await asyncio.sleep(e.value)
                                await client.forward_messages(
                                    dialog.chat.id,
                                    forward_info["chat_id"],
                                    forward_info["message_id"]
                                )
                                group += 1
                            except Exception as e:
                                print(f"Error forwarding to {dialog.chat.id}: {e}")

                    if client.me.id not in AG:
                        return

                    done += 1
                    await msg.reply(
                        f"""
<blockquote><b>    {prem} Autofw Prem {prem}</blockquote></b>\n<blockquote><b><i>{scsb} • Broadcast Terkirim • {scsb}\n
{putr} • Putaran ke : {done}\n
{brhsll} • Berhasil : {group} Group\n
{delayy} • Delay : {delay} Menit</i></b></blockquote>\n<b><blockquote>{stars} ᴜsᴇʀʙᴏᴛ ᴘʀᴇᴍɪᴜᴍ {stars}</b></blockquote>
"""
,
                        quote=True
                    )
                    await asyncio.sleep(int(60 * int(delay)))

                except Exception as e:
                    print(f"Error in Autofw loop: {e}")
                    await asyncio.sleep(5)  # Delay before retrying

        else:
            await msg.delete()

    elif type == "off":
        if client.me.id in AG:
            AG.remove(client.me.id)
            await msg.edit(f"<blockquote><b>{brhsl} Autofw Dinonaktifkan</blockquote></b>")
        else:
            await msg.delete()

    elif type == "delay":
        if not value.isdigit():
            return await msg.edit(f"<blockquote><b>{ggl} Harap Berikan Angka</blockquote></b>")
        await set_vars(client.me.id, "DELAY_GCAST", value)
        await msg.edit(f"<blockquote><b>{brhsl} Delay Di Atur Ke {value} Menit</blockquote></b>")

    else:
        await msg.edit(f"<blockquote><b>{ggl} Perintah Tidak Valid</blockquote></b>")

# Fungsi untuk memulai kembali Auto Gcast saat bot di-restart
async def restart_autofw(client):
    if client.me.id in AG:
        await client.send_message(chat_id=client.me.id, text="Autofw sudah aktif, memulai kembali...")
        await _(client, message)  # Memanggil fungsi utama untuk memulai Auto Gcast

# Menambahkan event handler untuk memulai Auto Gcast saat bot di-restart
@PY.UBOT("start")
async def start_handler(client):
    if client.me.id in AG:
        await restart_autofw(client)
