from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone
from PyroUbot.config import OWNER_ID
from PyroUbot import *


@PY.UBOT("prem")
async def _(client, message):
    user = message.from_user

    # Ambil list seller, admin & superultra
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Gabungkan semua role
    allowed_users = set(seles_users + admin_users + superultra_users + [OWNER_ID])

    if user.id not in allowed_users:
        return

    # Ambil target & durasi
    reply = message.reply_to_message
    if reply:
        target_id = reply.from_user.id
        args = message.text.split(maxsplit=1)
        duration = args[1].lower() if len(args) > 1 else "1b"
    else:
        args = message.text.split()[1:]
        if not args:
            return await message.reply("""⛔ Cara penggunaan: `.prem user_id/username waktu`
Contoh:
- `.prem 1234567890 1b`
- `.prem @username 15h`
- Reply ke pesan user: `.prem 1b`
- `.prem 1234567890 0` → permanen (hanya owner)
""")
        target_id = args[0]
        duration = args[1].lower() if len(args) > 1 else "1b"

    # Normalisasi target_id
    if str(target_id).isdigit():
        target_id = int(target_id)

    # Cek permanen
    is_permanent = duration in ["0", "perma", "permanen"]

    if is_permanent:
        if user.id != OWNER_ID:
            return await message.reply("⛔ Hanya OWNER yang bisa memberikan premium permanen.")
        total_days = None  # permanen
    else:
        # Konversi ke hari
        if duration.endswith("b"):  # bulan
            total_days = int(duration[:-1]) * 30 if duration[:-1].isdigit() else 30
        elif duration.endswith("h"):  # hari
            total_days = int(duration[:-1]) if duration[:-1].isdigit() else 1
        else:
            total_days = 30

        # Tentukan maksimal hari berdasarkan role
        if user.id == OWNER_ID:
            max_days = 3650
        elif user.id in admin_users:
            max_days = 180
        elif user.id in seles_users:
            max_days = 90
        elif user.id in superultra_users:
            max_days = 365
        else:
            return await message.reply("⛔ Kamu tidak punya akses ke perintah ini.")

        if total_days > max_days:
            return await message.reply(f"⛔ Maksimal kamu hanya bisa memberikan {max_days} hari.")

    msg = await message.reply("⏳ Memproses...")

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    try:
        tz = timezone("Asia/Jakarta")
        now = datetime.now(tz)

        if is_permanent:
            expired_date = None
            expired_str = "♾️ PERMANEN"
        else:
            dataexp = await get_expired_date(target_user.id)
            if dataexp and dataexp.tzinfo is None:
                dataexp = tz.localize(dataexp)

            if dataexp and dataexp > now:
                expired_date = dataexp + timedelta(days=total_days)
            else:
                expired_date = now + timedelta(days=total_days)

            expired_str = expired_date.strftime("%d-%m-%Y %H:%M")

        # Simpan expired baru
        await set_expired_date(target_user.id, expired_date)

        # Cegah duplikat PREM_USERS
        prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")
        if str(target_user.id) not in prem_users:
            await add_to_vars(client.me.id, "PREM_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Premium Aktif
⏳ Masa Aktif: {expired_str}
🔹 Silakan buka @{client.me.username} untuk menggunakan userbot
""")

        # Notif owner
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Seller/Admin:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Customer:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_str}`
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⁉️ Seller/Admin", callback_data=f"profil {message.from_user.id}"),
                        InlineKeyboardButton("Customer ⁉️", callback_data=f"profil {target_user.id}"),
                    ],
                ]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("unprem")
async def _(client, message):
    user = message.from_user

    # Ambil list seller, admin & superultra
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Gabungkan semua role
    allowed_users = set(seles_users + admin_users + superultra_users + [OWNER_ID])

    if user.id not in allowed_users:
        return  # selain role ini, gak bisa pakai /unprem

    msg = await message.reply("⏳ Memproses...")

    # Ambil target user
    reply = message.reply_to_message
    if reply:
        target_id = reply.from_user.id
    else:
        args = message.text.split()
        if len(args) < 2:
            return await msg.edit(
                """⛔ Cara penggunaan: `.unprem user_id/username`
Contoh:
- `.unprem 1234567890`
- `.unprem @username`
- Reply ke pesan user: `.unprem`
"""
            )
        target_id = args[1]

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error mengambil user: {e}")

    try:
        # Hapus dari PREM_USERS
        await remove_from_vars(client.me.id, "PREM_USERS", target_user.id)
        # Hapus expired date
        await rem_expired_date(target_user.id)

        return await msg.edit(f"""
**ɪɴғᴏʀᴍᴀᴛɪᴏɴ:**
<blockquote>👤 Nama: <a href="tg://user?id={target_user.id}">{target_user.first_name} {target_user.last_name or ''}</a>
🆔 ID: <code>{target_user.id}</code>
📚 Keterangan: <b>Premium Dicabut</b>
</blockquote>
""", disable_web_page_preview=True)

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")
        

@PY.UBOT("getprem")
@PY.OWNER
async def _(client, message):
    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")
    if not prem_users:
        return await message.reply_text("📭 Tidak ada pengguna premium yang ditemukan.")

    text = "<b>👑 Daftar Pengguna Premium:</b>\n\n"
    count = 0
    batch = []
    tz = timezone("Asia/Jakarta")

    # Hilangkan duplikat user
    seen = set()
    for user_id in prem_users:
        if user_id in seen:
            continue
        seen.add(user_id)

        try:
            user = await client.get_users(int(user_id))
            expired = await get_expired_date(user.id)

            if expired:
                if expired.tzinfo is None:
                    expired = tz.localize(expired)
                expired_str = expired.astimezone(tz).strftime("%d-%m-%Y %H:%M")
            else:
                expired_str = "♾️ PERMANEN"

            count += 1

            user_info = (
                f"• <b>{count}.</b> <a href='tg://user?id={user.id}'>"
                f"{user.first_name} {user.last_name or ''}</a>\n"
                f"🆔 <code>{user.id}</code>\n"
                f"⏳ Expired: <code>{expired_str}</code>\n\n"
            )

            # cek limit telegram (4096)
            if len(text) + len(user_info) > 4000:
                batch.append(text)
                text = ""

            text += user_info

        except Exception:
            continue

    if text:
        batch.append(text)

    # kirim batch satu-satu
    for idx, part in enumerate(batch):
        if idx == 0:
            # tambahin total di batch pertama
            part += f"<b>Total Premium:</b> {count} user"
        await message.reply_text(part, disable_web_page_preview=True)


@PY.UBOT("seles")
async def _(client, message):
    user = message.from_user

    # Ambil role
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    allowed_users = set(admin_users + superultra_users + [OWNER_ID])
    if user.id not in allowed_users:
        return

    # Ambil target & durasi
    reply = message.reply_to_message
    if reply:
        target_id = reply.from_user.id
        args = message.text.split(maxsplit=1)
        duration = args[1].lower() if len(args) > 1 else "1b"
    else:
        args = message.text.split()[1:]
        if not args:
            return await message.reply("""⛔ Cara penggunaan: `.seles user_id/username waktu`
Contoh:
- `.seles 1234567890 1b`
- `.seles @username 15h`
- Reply ke pesan user: `.seles 1b`
- `.seles 1234567890 0` → permanen (hanya owner)
""")
        target_id = args[0]
        duration = args[1].lower() if len(args) > 1 else "1b"

    if str(target_id).isdigit():
        target_id = int(target_id)

    # === cek permanen ===
    is_permanent = duration in ["0", "perma", "permanen"]
    if is_permanent:
        if user.id != OWNER_ID:
            return await message.reply("⛔ Hanya OWNER yang bisa memberikan seller permanen.")
        total_days = None
    else:
        if duration.endswith("b"):  # bulan
            total_days = int(duration[:-1]) * 30 if duration[:-1].isdigit() else 30
        elif duration.endswith("h"):  # hari
            total_days = int(duration[:-1]) if duration[:-1].isdigit() else 1
        else:
            total_days = 30

        # Limit berdasarkan role
        if user.id == OWNER_ID:
            max_days = 3650
        elif user.id in admin_users:
            max_days = 180
        elif user.id in superultra_users:
            max_days = 365
        else:
            return await message.reply("⛔ Kamu tidak punya akses ke perintah ini.")

        if total_days > max_days:
            return await message.reply(f"⛔ Maksimal kamu hanya bisa memberikan {max_days} hari.")

    msg = await message.reply("⏳ Memproses...")

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    try:
        tz = timezone("Asia/Jakarta")
        now = datetime.now(tz)

        if is_permanent:
            expired_date = None
            expired_str = "♾️ PERMANEN"
        else:
            dataexp = await get_expired_date(target_user.id)
            if dataexp and dataexp.tzinfo is None:
                dataexp = tz.localize(dataexp)

            if dataexp and dataexp > now:
                expired_date = dataexp + timedelta(days=total_days)
            else:
                expired_date = now + timedelta(days=total_days)

            expired_str = expired_date.strftime("%d-%m-%Y %H:%M")

        # simpan expired baru
        await set_expired_date(target_user.id, expired_date)

        # tambahkan ke seller list
        seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")
        if str(target_user.id) not in seles_users:
            await add_to_vars(client.me.id, "SELER_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Seller Aktif
⏳ Masa Aktif: {expired_str}
""")

        # notif ke OWNER
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Executor:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Seller Baru:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_str}`
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⁉️ Executor", callback_data=f"profil {message.from_user.id}"),
                        InlineKeyboardButton("Seller Baru ⁉️", callback_data=f"profil {target_user.id}"),
                    ],
                ]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("unseles")
async def _(client, message):
    msg = await message.reply("⏳ Sedang memproses...")

    # Ambil list role
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    # Gabungkan role yang diizinkan
    allowed_users = set(admin_users + superultra_users + [OWNER_ID])
    if message.from_user.id not in allowed_users:
        return

    # Ambil target user
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id
    else:
        args = message.text.split()
        if len(args) < 2:
            return await msg.edit(
                "<b>⛔ Cara penggunaan:</b>\n"
                "• <code>.unseles user_id/username</code>\n"
                "• Reply ke pesan user: <code>.unseles</code>"
            )
        user_id = args[1]

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"❌ Error mengambil user: {error}")

    # Cek apakah user seller
    if str(user.id) not in seles_users:
        return await msg.edit(f"""
ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
<blockquote>⎆ name: <a href="tg://user?id={user.id}">{user.first_name} {user.last_name or ''}</a>
⎆ id: <code>{user.id}</code>
⎆ keterangan: <b>Tidak dalam daftar seller</b>
</blockquote>
""", disable_web_page_preview=True)

    try:
        # Hapus dari list seller & expired date
        await remove_from_vars(client.me.id, "SELER_USERS", user.id)
        await rem_expired_date(user.id)

        await msg.edit(f"""
ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
<blockquote>⎆ name: <a href="tg://user?id={user.id}">{user.first_name} {user.last_name or ''}</a>
⎆ id: <code>{user.id}</code>
⎆ keterangan: <b>Seller dicabut</b>
</blockquote>
""", disable_web_page_preview=True)

        # Notif ke OWNER
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Executor:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Seller Dicabut:** {user.first_name} (`{user.id}`)
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⁉️ Executor", callback_data=f"profil {message.from_user.id}"),
                        InlineKeyboardButton("Seller Dicabut ⁉️", callback_data=f"profil {user.id}"),
                    ],
                ]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("getseles")
@PY.OWNER
async def _(client, message):
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")
    if not seles_users:
        return await message.reply_text("📭 Tidak ada seller yang ditemukan.")

    text = "<b>📋 Daftar Seller:</b>\n\n"
    count = 0
    batch = []
    tz = timezone("Asia/Jakarta")

    # Hilangkan duplikat user
    seen = set()
    for user_id in seles_users:
        if user_id in seen:
            continue
        seen.add(user_id)

        try:
            user = await client.get_users(int(user_id))
            expired = await get_expired_date(user.id)

            if expired:
                if expired.tzinfo is None:
                    expired = tz.localize(expired)
                expired_str = expired.astimezone(tz).strftime("%d-%m-%Y %H:%M")
            else:
                expired_str = "♾️ PERMANEN"

            count += 1

            user_info = (
                f"• <b>{count}.</b> <a href='tg://user?id={user.id}'>"
                f"{user.first_name} {user.last_name or ''}</a>\n"
                f"🆔 <code>{user.id}</code>\n"
                f"⏳ Expired: <code>{expired_str}</code>\n\n"
            )

            # cek limit telegram (4096)
            if len(text) + len(user_info) > 4000:
                batch.append(text)
                text = ""

            text += user_info

        except Exception:
            continue

    if text:
        batch.append(text)

    # kirim batch satu-satu
    for idx, part in enumerate(batch):
        if idx == 0:
            part += f"<b>Total Seller:</b> {count} user"
        await message.reply_text(part, disable_web_page_preview=True)


@PY.UBOT("addadmin")
async def _(client, message):
    msg = await message.reply("⏳ Memproses...")

    # Ambil list SuperUltra
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # OWNER & SuperUltra aja yg bisa akses
    if message.from_user.id != OWNER_ID and message.from_user.id not in superultra_users:
        return

    # Ambil target & durasi
    reply = message.reply_to_message
    args = message.text.split()[1:]

    if reply:
        target_id = reply.from_user.id
        duration = args[0].lower() if args else "1b"
    else:
        if not args:
            return await msg.edit("""⛔ Cara penggunaan: 
`/addadmin user_id/username waktu`
Contoh:
- `/addadmin 1234567890 1b`
- `/addadmin @username 15h`
- `/addadmin @username perma`
- Reply ke pesan user: `/addadmin 2b`
""")
        target_id = args[0]
        duration = args[1].lower() if len(args) > 1 else "1b"

    # Normalisasi target_id
    if str(target_id).isdigit():
        target_id = int(target_id)

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    # Cek apakah sudah admin
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    is_new_admin = str(target_user.id) not in admin_users

    try:
        tz = timezone("Asia/Jakarta")
        now = datetime.now(tz)

        # === Cek permanen ===
        is_permanent = duration in ["0", "perma", "permanen"]

        if is_permanent:
            if message.from_user.id != OWNER_ID:
                return await msg.edit("⛔ Hanya OWNER yang bisa memberi Admin permanen!")
            expired_date = None
            expired_str = "♾️ PERMANEN"
        else:
            # Konversi ke hari
            if duration.endswith("b"):  # bulan
                total_days = int(duration[:-1]) * 30 if duration[:-1].isdigit() else 30
            elif duration.endswith("h"):  # hari
                total_days = int(duration[:-1]) if duration[:-1].isdigit() else 1
            else:
                total_days = 30  # default 1 bulan

            # Tentukan maksimal hari berdasarkan role
            if message.from_user.id == OWNER_ID:
                max_days = 3650  # 10 tahun
            elif message.from_user.id in superultra_users:
                max_days = 365  # 1 tahun
            else:
                return await msg.edit("⛔ Kamu tidak punya akses untuk perintah ini.")

            if total_days > max_days:
                return await msg.edit(f"⛔ Maksimal kamu hanya bisa memberikan {max_days} hari.")

            # === Ambil expired lama (buat extend) ===
            dataexp = await get_expired_date(target_user.id)
            if dataexp and dataexp.tzinfo is None:
                dataexp = tz.localize(dataexp)

            if dataexp and dataexp > now:
                expired_date = dataexp + timedelta(days=total_days)  # extend
            else:
                expired_date = now + timedelta(days=total_days)  # baru

            expired_str = expired_date.strftime("%d-%m-%Y %H:%M")

        # Simpan expired baru
        await set_expired_date(target_user.id, expired_date)

        # Tambahkan ke ADMIN_USERS (kalau belum ada)
        if is_new_admin:
            await add_to_vars(client.me.id, "ADMIN_USERS", target_user.id)

        await msg.edit(f"""
👤 Nama: {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Admin Aktif
⏳ Masa Aktif: {expired_str}
""")

        # === Notif ke Owner ===
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Executor:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Admin Baru:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_str}`
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("⁉️ Executor", callback_data=f"profil {message.from_user.id}"),
                        InlineKeyboardButton("Admin Baru ⁉️", callback_data=f"profil {target_user.id}"),
                    ],
                ]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("unadmin")
async def _(client, message):
    msg = await message.reply("⏳ Memproses...")

    # Ambil list superultra
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    # OWNER & SuperUltra aja yg bisa akses
    if message.from_user.id != OWNER_ID and message.from_user.id not in superultra_users:
        return await msg.edit("⛔ Kamu tidak punya akses untuk menghapus admin!")

    # Ambil target user
    reply = message.reply_to_message
    if reply:
        user_id = reply.from_user.id
    else:
        args = message.text.split()
        if len(args) < 2:
            return await msg.edit("""⛔ Cara penggunaan:
/unadmin user_id/username
Contoh:
- /unadmin 1234567890
- /unadmin @username
- Reply pesan user: /unadmin
""")
        user_id = args[1]

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
👤 Nama: {user.first_name}
🆔 ID: `{user.id}`
📚 Keterangan: Tidak dalam daftar Admin
""")

    try:
        # Hapus dari daftar admin
        await remove_from_vars(client.me.id, "ADMIN_USERS", user.id)
        # Hapus expired date (pakai rem_expired_date biar bersih total)
        await rem_expired_date(user.id)

        return await msg.edit(f"""
👤 Nama: {user.first_name}
🆔 ID: `{user.id}`
❌ Status: Bukan Admin lagi
""")
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("getadmin")
@PY.OWNER
async def _(client, message):
    Sh = await message.reply("⏳ Sedang memproses...")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("📭 Daftar admin kosong.")

    tz = timezone("Asia/Jakarta")
    now = datetime.now(tz)
    text = "<b>📋 Daftar Admin:</b>\n\n"
    count = 0
    batch = []

    # Hilangkan duplikat
    seen = set()
    for user_id in admin_users:
        if user_id in seen:
            continue
        seen.add(user_id)

        try:
            user = await client.get_users(int(user_id))
            expired = await get_expired_date(user.id)

            if expired:
                if expired.tzinfo is None:
                    expired = tz.localize(expired)
                expired_str = expired.astimezone(tz).strftime("%d-%m-%Y %H:%M")
                status = "✅ Aktif" if expired >= now else "❌ Expired"
            else:
                expired_str = "♾️ PERMANEN"
                status = "♾️"

            count += 1

            user_info = (
                f"• <b>{count}.</b> <a href='tg://user?id={user.id}'>"
                f"{user.first_name} {user.last_name or ''}</a>\n"
                f"🆔 <code>{user.id}</code>\n"
                f"⏳ {expired_str} ({status})\n\n"
            )

            if len(text) + len(user_info) > 4000:
                batch.append(text)
                text = ""
            text += user_info

        except Exception:
            text += (
                f"• <b>{count+1}.</b> Unknown User\n"
                f"🆔 <code>{user_id}</code>\n"
                f"⏳ - (❌ Tidak ditemukan)\n\n"
            )
            count += 1

    if text:
        batch.append(text)

    # Kirim batch satu-satu
    for idx, part in enumerate(batch):
        if idx == 0:
            part += f"<b>⚜️ Total Admin User:</b> {count}"
        await Sh.edit(part, disable_web_page_preview=True)


@PY.UBOT("superultra")
async def _(client, message):
    user = message.from_user

    # Hanya OWNER yang bisa eksekusi
    if user.id != OWNER_ID:
        return await message.reply("⛔ Hanya OWNER yang bisa menambahkan SuperUltra!")

    # Ambil target & durasi
    reply = message.reply_to_message
    args = message.text.split(maxsplit=2)

    if reply:
        target_id = reply.from_user.id
        duration = args[1] if len(args) > 1 else "1"
    else:
        if len(args) < 2:
            return await message.reply("""⛔ Cara penggunaan: 
`/superultra user_id/username bulan/perma`
Contoh:
- `/superultra 1234567890 1`
- `/superultra @username 2`
- `/superultra @username perma`
- Reply ke pesan user: `/superultra 1`
""")
        target_id = args[1]
        duration = args[2] if len(args) > 2 else "1"

    # Normalisasi target_id
    if str(target_id).isdigit():
        target_id = int(target_id)

    msg = await message.reply("⏳ Memproses...")

    # Ambil info user
    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    # Ambil list SuperUltra
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Cek apakah sudah SuperUltra
    if target_user.id in superultra_users:
        expired = await get_expired_date(target_user.id)
        expired_str = expired.strftime("%d-%m-%Y") if expired else "♾️ PERMANEN"
        return await msg.edit(f"""
👤 Nama: {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Sudah SuperUltra
⏳ Expired: `{expired_str}`
""")

    # Handle durasi
    try:
        tz = timezone("Asia/Jakarta")
        now = datetime.now(tz)

        is_permanent = str(duration).lower() in ["0", "perma", "permanen"]
        if is_permanent:
            expired_date = None
            expired_str = "♾️ PERMANEN"
        else:
            months = int(duration) if str(duration).isdigit() else 1
            expired_date = now + relativedelta(months=months)
            expired_str = expired_date.strftime("%d-%m-%Y")

        # Simpan expired dan add ke ULTRA_PREM
        await set_expired_date(target_user.id, expired_date)
        await add_to_vars(client.me.id, "ULTRA_PREM", target_user.id)

        # Konfirmasi ke eksekutor
        await msg.edit(f"""
👤 Nama: {target_user.first_name}
🆔 ID: `{target_user.id}`
⏳ Expired: `{expired_str}`
🔹 Berhasil dijadikan **SuperUltra**
""")

        # Notif OWNER
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Executor:** {user.first_name} (`{user.id}`)
**👤 SuperUltra Baru:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_str}`
""",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("⁉️ Executor", callback_data=f"profil {user.id}"),
                    InlineKeyboardButton("SuperUltra Baru ⁉️", callback_data=f"profil {target_user.id}"),
                ]]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.UBOT("unultra")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("⏳ Sedang memproses...")

    # ambil user dari reply atau argumen
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            "⛔ Cara penggunaan: `/unultra user_id/username` atau reply ke pesan user"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id not in superultra_users:
        return await msg.edit(f"""
**👤 Nama:** {user.first_name}
🆔 ID: `{user.id}`
📚 Keterangan: Tidak ada dalam daftar SuperUltra
""")

    try:
        # hapus dari ULTRA_PREM + expired date
        await remove_from_vars(client.me.id, "ULTRA_PREM", user.id)
        await rem_expired_date(user.id)

        return await msg.edit(f"""
**👤 Nama:** {user.first_name}
🆔 ID: `{user.id}`
🗑️ Berhasil dihapus dari SuperUltra
""")
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")
        

@PY.UBOT("getultra")
@PY.OWNER
async def _(client, message):
    ultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if not ultra_users:
        return await message.reply_text("📭 Tidak ada pengguna SuperUltra yang ditemukan.")

    text = "<b>⚡ Daftar Pengguna SuperUltra:</b>\n\n"
    count = 0
    batch = []
    tz = timezone("Asia/Jakarta")

    # Hilangkan duplikat user
    seen = set()
    for user_id in ultra_users:
        if user_id in seen:
            continue
        seen.add(user_id)

        try:
            user = await client.get_users(int(user_id))
            expired = await get_expired_date(user.id)

            if expired:
                if expired.tzinfo is None:
                    expired = tz.localize(expired)
                expired_str = expired.astimezone(tz).strftime("%d-%m-%Y %H:%M")
            else:
                expired_str = "♾️ PERMANEN"

            count += 1

            user_info = (
                f"• <b>{count}.</b> <a href='tg://user?id={user.id}'>"
                f"{user.first_name} {user.last_name or ''}</a>\n"
                f"🆔 <code>{user.id}</code>\n"
                f"⏳ Expired: <code>{expired_str}</code>\n\n"
            )

            # cek limit telegram (4096)
            if len(text) + len(user_info) > 4000:
                batch.append(text)
                text = ""

            text += user_info

        except Exception:
            continue

    if text:
        batch.append(text)

    # kirim batch satu-satu
    for idx, part in enumerate(batch):
        if idx == 0:
            part += f"<b>Total SuperUltra:</b> {count} user"
        await message.reply_text(part, disable_web_page_preview=True)


@PY.BOT("set_time")
@PY.OWNER
async def _(client, message):
    Tm = await message.reply("processing . . .")
    bajingan = message.command
    if len(bajingan) != 3:
        return await Tm.edit(f"mohon gunakan /set_time user_id hari")
    user_id = int(bajingan[1])
    get_day = int(bajingan[2])
    print(user_id , get_day)
    try:
        get_id = (await client.get_users(user_id)).id
        user = await client.get_users(user_id)
    except Exception as error:
        return await Tm.edit(error)
    if not get_day:
        get_day = 30
    now = datetime.now(timezone("Asia/Jakarta"))
    expire_date = now + timedelta(days=int(get_day))
    await set_expired_date(user_id, expire_date)
    await Tm.edit(f"""
 ⎆ ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 ⎆ name: {user.mention}
 ⎆ id: {get_id}
 ⎆ aktifkan_selama: {get_day} hari
"""
    )


@PY.BOT("cek")
@PY.SELLER
async def _(client, message):
    Sh = await message.reply("processing . . .")
    user_id = await extract_user(message)
    if not user_id:
        return await Sh.edit("pengguna tidak ditemukan")

    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.edit(f"❌ Error: {error}")

    if get_exp is None:
        await Sh.edit(f"""
⎆ INFORMATION
ᚗ name : {sh.mention}
ᚗ plan : none
ᚗ id : {user_id}
ᚗ prefix : .
ᚗ expired : nonaktif
""")
    else:
        SH = await ubot.get_prefix(user_id)
        exp = get_exp.strftime("%d-%m-%Y")
        if user_id in await get_list_from_vars(client.me.id, "ULTRA_PREM"):
            status = "SuperUltra"
        else:
            status = "Premium"

        await Sh.edit(f"""
⎆ INFORMATION
ᚗ name : {sh.mention}
ᚗ plan : {status}
ᚗ id : {user_id}
ᚗ prefix : {' '.join(SH)}
ᚗ expired : {exp}
""")
