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

prcs   = emoji("PROCES")
aktf   = emoji("AKTIF")
saktf  = emoji("SAKTIF")
ttsmp  = emoji("TTERSIMPAN")
stopb  = emoji("STOPB")
scsb   = emoji("SUCSESB")
brhsl  = emoji("BERHASIL")
ggla   = emoji("GAGALA")
delayy = emoji("DELAYY")
brhsls = emoji("BERHASILS")
dlts   = emoji("DELETES")
stars  = emoji("STARS")
prem   = emoji("PREM")
put    = emoji("PUTAR")


async def run_autobc(client):
    """Loop utama AutoBC"""
    done, failed, total_round = 0, 0, 0
    AG[client.me.id] = {"status": True, "round": 0}

    while AG[client.me.id]["status"]:
        delay = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)  # menit antar putaran
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)  # detik antar grup

        blacklist = await get_list_from_vars(client.me.id, "BL_ID")
        auto_texts = await get_auto_text(client.me.id)

        if not auto_texts:
            await client.send_message(client.me.id, f"<b><i>{ttsmp} Tidak ada pesan yang disimpan.</i></b>")
            AG[client.me.id]["status"] = False
            await set_vars(client.me.id, "AUTOBCAST", "off")
            return

        message_to_forward = random.choice(auto_texts)
        group_success, failed = 0, 0
        total_round += 1
        AG[client.me.id]["round"] = total_round

        async for dialog in client.get_dialogs():
            if not AG[client.me.id]["status"]:
                await client.send_message(client.me.id, f"<b><i>{stopb} Auto Broadcast dihentikan.</i></b>")
                return

            if (
                dialog.chat.type in (ChatType.GROUP, ChatType.SUPERGROUP)
                and dialog.chat.id not in blacklist
                and dialog.chat.id not in BLACKLIST_CHAT
            ):
                try:
                    await client.forward_messages(dialog.chat.id, "me", message_to_forward)
                    group_success += 1
                except FloodWait as e:
                    await asyncio.sleep(e.value)
                except Exception as err:
                    failed += 1
                    # log error forward
                    await client.send_message(client.me.id, f"❌ Gagal forward ke {dialog.chat.id}\nError: {err}")

                await asyncio.sleep(per_group_delay)  # jeda antar grup

        await client.send_message(
            client.me.id,
            f"""
<b>⚡️ AutoBC Putaran Selesai</b>
✅ Berhasil : {group_success} Chat
❌ Gagal : {failed} Chat
⏳ Putaran Ke : {total_round}
🕒 Jeda Putaran : {delay} Menit
⏱️ Delay per Grup : {per_group_delay} Detik
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

        # set default delay kalau belum ada
        if not await get_vars(client.me.id, "DELAY_GCAST"):
            await set_vars(client.me.id, "DELAY_GCAST", "60")
        if not await get_vars(client.me.id, "PER_GROUP_DELAY"):
            await set_vars(client.me.id, "PER_GROUP_DELAY", "3")

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
        return await msg.edit(f"<b><i>{delayy} Delay antar putaran berhasil diatur ke {value} menit.</i></b>")

    elif type == "perdelay":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Format salah! Gunakan .autobc perdelay [detik]</i></b>")

        val = int(value)
        if val < 3:  # minimal 3 detik biar aman
            return await msg.edit(f"<b><i>{stopb} Minimal delay per grup adalah 3 detik.</i></b>")

        await set_vars(client.me.id, "PER_GROUP_DELAY", str(val))
        return await msg.edit(f"<b><i>{delayy} Delay per grup berhasil diatur ke {val} detik.</i></b>")

    elif type == "text":
        if not message.reply_to_message:
            return await msg.edit(f"<b><i>{stopb} Format salah! Harap reply ke pesan yang ingin disimpan.</i></b>")

        saved_msg = await message.reply_to_message.copy("me")
        await add_auto_text(client.me.id, saved_msg.id)
        return await msg.edit(f"<b><i>{brhsls} Pesan berhasil disimpan dengan ID {saved_msg.id}</i></b>")

    elif type == "list":
        auto_texts = await get_auto_text(client.me.id)
        if not auto_texts:
            return await msg.edit(f"<b><i>{ttsmp} Tidak ada pesan tersimpan.</i></b>")

        teks = "\n".join([f"{i+1}. ID: {t}" for i, t in enumerate(auto_texts)])
        return await msg.edit(f"<b><i>{stars} Daftar Pesan AutoBC:</i></b>\n\n{teks}")

    elif type == "remove":
        if not value.isdigit():
            return await msg.edit(f"<b><i>{stopb} Harap masukkan nomor urut pesan yang valid.</i></b>")

        idx = int(value) - 1
        auto_texts = await get_auto_text(client.me.id)
        if idx < 0 or idx >= len(auto_texts):
            return await msg.edit(f"<b><i>{stopb} ID tidak ditemukan.</i></b>")

        removed = auto_texts[idx]
        await remove_auto_text(client.me.id, idx)
        return await msg.edit(f"<b><i>{dlts} Pesan dengan ID {removed} berhasil dihapus.</i></b>")


async def resume_autobc(client):
    """Dipanggil otomatis pas start ubot"""
    status = await get_vars(client.me.id, "AUTOBCAST")
    if status == "on":
        delay = int(await get_vars(client.me.id, "DELAY_GCAST") or 60)
        per_group_delay = int(await get_vars(client.me.id, "PER_GROUP_DELAY") or 3)
        round_no = AG.get(client.me.id, {}).get("round", 0) + 1

        await client.send_message(
            client.me.id,
            f"""📣 AutoBC #{round_no} (Resume)
🕒 Delay antar putaran: {delay} menit
⏱️ Delay per grup: {per_group_delay} detik
📬 Broadcast akan dilanjutkan sesuai jadwal."""
        )
        asyncio.create_task(run_autobc(client))


@PY.UBOT("start")
async def start_handler(client, message):
    await resume_autobc(client)
    return await message.reply("✅ Bot sudah berjalan.")
