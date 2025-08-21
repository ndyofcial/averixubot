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

@PY.UBOT("autobc")
async def _(client, message):
    msg = await message.reply(f"<b><i>{prcs} Processing...</i></b>")
    type, value = extract_type_and_text(message)
    
    if type == "on":
        if client.me.id in AG and AG[client.me.id]["status"]:
            return await msg.edit(f"<b><i>{saktf} Auto Broadcast sudah aktif.</i></b>")

        AG[client.me.id] = {"status": True}
        await msg.edit(f"<b><i>{aktf} Auto Broadcast diaktifkan.</i></b>")
        done, failed = 0, 0  

        while AG[client.me.id]["status"]:
            delay = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)  
            blacklist = await get_list_from_vars(client.me.id, "BL_ID")
            auto_texts = await get_auto_text(client.me.id)

            if not auto_texts:
                return await msg.edit(f"<b><i>{ttsmp} Tidak ada pesan yang disimpan.</i></b>")
            
            message_to_forward = random.choice(auto_texts)
            group = 0

            async for dialog in client.get_dialogs():
                if not AG[client.me.id]["status"]:
                    return await msg.reply(f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")

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

            if not AG[client.me.id]["status"]:
                return await msg.reply(f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")
            
            done += 1
            await msg.reply(
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

    elif type == "off":
        if client.me.id in AG and AG[client.me.id]["status"]:
            AG[client.me.id]["status"] = False
            return await msg.edit(f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")
        else:
            return await msg.edit(f"<b><i>{stopb} Auto Broadcast tidak sedang berjalan.</i></b>")
    
    elif type == "text":
        if not message.reply_to_message:
            return await msg.edit(f"<b><i>{stopb} Format salah! Harap reply ke pesan yang ingin disimpan.</i></b>")
        
        saved_msg = await message.reply_to_message.copy("me")
        await add_auto_text(client.me.id, saved_msg.id)
        return await msg.edit(f"<b><i>{brhsls} Pesan berhasil disimpan dengan ID {saved_msg.id}</i></b>")
    
    elif type == "list":
        auto_texts = await get_auto_text(client.me.id)
        
        if not auto_texts:
            return await msg.edit(f"<b><i>{ggla} Tidak ada pesan yang disimpan.</i></b>")
        
        txt = "<b><i>📌 Daftar Auto Broadcast Text</i></b>\n\n"
        for num, msg_id in enumerate(auto_texts, 1):
            try:
                saved_msg = await client.get_messages("me", msg_id)
                txt += f"`{num}> {saved_msg.text[:20]}...`\n"
            except:
                txt += f"`{num}> [Pesan tidak ditemukan]`\n"
        
        txt += "\n<b><i>🗑 Untuk menghapus text:\n.autobc remove [angka/all]</i></b>"
        return await msg.edit(txt)
    
    elif type == "remove":
        auto_texts = await get_auto_text(client.me.id)
        
        if not auto_texts:
            return await msg.edit(f"<b><i>{ggla} Tidak ada pesan yang disimpan.</i></b>")
        
        if value == "all":
            await remove_auto_text(client.me.id)
            return await msg.edit(f"<b><i>{dlts} Semua pesan berhasil dihapus.</i></b>")
        
        try:
            index = int(value) - 1
            if 0 <= index < len(auto_texts):
                await remove_auto_text(client.me.id, index)
                return await msg.edit(f"<b><i>{dlts} Pesan ke-{index+1} berhasil dihapus.</i></b>")
            else:
                return await msg.edit(f"<b><i>{dlts} Nomor pesan tidak valid.</i></b>")
        except ValueError:
            return await msg.edit(f"<b><i>{stopb} Gunakan angka atau 'all'.</i></b>")
    
    elif type == "delay":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Format salah! Gunakan .autobc delay [angka]</i></b>")
        await set_vars(client.me.id, "DELAY_GCAST", value)
        return await msg.edit(f"<b><i>{delayy} Delay berhasil diatur ke {value} menit.</i></b>")
    
    else:
        return await msg.edit(f"<b><i>{stopb} Format salah! Gunakan .autobc [query] - [value]</i></b>")

async def restart_autobc(client):
    if client.me.id in AG:
        await client.send_message(chat_id=client.me.id, text="Autobc sudah aktif, memulai kembali...")
        await _(client, message)  # Memanggil fungsi utama untuk memulai Auto Gcast

# Menambahkan event handler untuk memulai Auto Gcast saat bot di-restart
@PY.UBOT("start")
async def start_handler(client):
    if client.me.id in AG:
        await restart_autobc(client)
