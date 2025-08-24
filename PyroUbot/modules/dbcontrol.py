from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone


from PyroUbot import *

__MODULE__ = "ᴅʙ ᴄᴏɴᴛʀᴏʟ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴅʙ ᴄᴏɴᴛʀᴏʟ ⦫</b>

<blockquote>⎆ <code>{0}prem</code>  
⊶ Tambah user jadi premium.
</blockquote>

<blockquote>⎆ <code>{0}unprem</code>  
⊶ Hapus status premium user.
</blockquote>

<blockquote>⎆ <code>{0}getprem</code>  
⊶ Lihat daftar user premium.
</blockquote>

<blockquote>⎆ <code>{0}seles</code>  
⊶ Tambah seller bot.
</blockquote>

<blockquote>⎆ <code>{0}unseles</code>  
⊶ Hapus seller bot.
</blockquote>

<blockquote>⎆ <code>{0}getseles</code>  
⊶ Lihat daftar seller.
</blockquote>

<blockquote>⎆ <code>{0}addadmin</code>  
⊶ Tambah admin bot.
</blockquote>

<blockquote>⎆ <code>{0}unadmin</code>  
⊶ Hapus admin bot.
</blockquote>

<blockquote>⎆ <code>{0}getadmin</code>  
⊶ Lihat daftar admin.
</blockquote>

<blockquote>⎆ <code>{0}time</code> id hari  
⊶ Tambah/Kurangi masa aktif user.
</blockquote>

<blockquote>⎆ <code>{0}cek</code> id  
⊶ Lihat masa aktif user.
</blockquote>
"""


@PY.BOT("prem")
async def _(client, message):
    user = message.from_user

    # Ambil list seller, admin & superultra
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Gabungkan semua role
    allowed_users = set(seles_users + admin_users + superultra_users + [OWNER_ID])

    if message.from_user.id not in allowed_users:
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
            if dataexp:
                if dataexp.tzinfo is None:
                    dataexp = tz.localize(dataexp)
            if dataexp and dataexp > now:
                expired_date = dataexp + timedelta(days=total_days)
            else:
                expired_date = now + timedelta(days=total_days)
            expired_str = expired_date.strftime("%d-%m-%Y %H:%M")

        # Simpan expired baru
        await set_expired_date(target_user.id, expired_date)

        # Tambah ke list PREM_USERS
        await add_to_vars(bot.me.id, "PREM_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Premium Aktif
⏳ Masa Aktif: {expired_str}
🔹 Silakan buka @{bot.me.username} untuk menggunakan userbot
""")

        # Notif owner
        await bot.send_message(
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


@PY.BOT("unprem")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("⏳ Memproses...")

    # ambil target user
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
        user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error mengambil user: {e}")

    try:
        # hapus dari PREM_USERS
        await remove_from_vars(client.me.id, "PREM_USERS", user.id)
        # pastikan expired date ikut dihapus
        await rem_expired_date(user.id)

        return await msg.edit(f"""
**ɪɴғᴏʀᴍᴀᴛɪᴏɴ:**
<blockquote>
👤 Nama: <a href="tg://user?id={user.id}">{user.first_name} {user.last_name or ''}</a>
🆔 ID: <code>{user.id}</code>
📚 Keterangan: <b>Premium Dicabut</b>
</blockquote>
""", disable_web_page_preview=True)

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")
        

@PY.BOT("getprem")
@PY.OWNER
async def _(client, message):
    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")
    if not prem_users:
        return await message.reply_text("📭 Tidak ada pengguna premium yang ditemukan.")

    text = "<b>👑 Daftar Pengguna Premium:</b>\n\n"
    count = 0
    batch = []
    tz = timezone("Asia/Jakarta")

    for user_id in prem_users:
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


@PY.BOT("seles")
async def _(client, message):
    msg = await message.reply("sedang memproses...")

    # ambil list admin & superultra
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    # kalau bukan OWNER, bukan admin, bukan superultra → stop
    if (
        message.from_user.id != OWNER_ID
        and message.from_user.id not in superultra_users
        and message.from_user.id not in admin_users
    ):
        return

    user_id, get_bulan = await extract_user_and_reason(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username - bulan</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id in seles_users:
        return await msg.edit(f"""
ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
<blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>⎆ id: {user.id}</b>
<b>⎆ keterangan: sudah seller</b></blockquote>
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))

        # default kalau input bulan kosong
        if not get_bulan:
            get_bulan = 1

        # cek apakah eksekutor superultra
        if message.from_user.id in superultra_users:
            su_expired = await get_expired_date(message.from_user.id)
            if not su_expired or su_expired < now:
                return await msg.edit("⛔ SuperUltra kamu sudah expired!")

            expired = su_expired  # expired ikut superultra
        else:
            expired = now + relativedelta(months=int(get_bulan))

        await set_expired_date(user.id, expired)
        await add_to_vars(client.me.id, "SELER_USERS", user.id)

        return await msg.edit(f"""
ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
<blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>⎆ id: {user.id}</b>
<b>⎆ expired: {expired.strftime('%d-%m-%Y')}</b>
<b>⎆ keterangan: seller berhasil ditambahkan</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unseles")
async def _(client, message):
    msg = await message.reply("sedang memproses...")

    # ambil list admin & superultra
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    # kalau bukan OWNER, bukan admin, bukan superultra → langsung stop (tanpa respon)
    if (
        message.from_user.id != OWNER_ID
        and message.from_user.id not in superultra_users
        and message.from_user.id not in admin_users
    ):
        return

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id not in seles_users:
        return await msg.edit(f"""
 ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 <blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
 </b>⎆ id: {user.id}</b>
 </b>⎆ keterangan: tidak dalam daftar</b></blockquote>
"""
        )

    try:
        await remove_from_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
 ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 <blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
 </b>⎆ id: {user.id}</b>
 </b>⎆ keterangan: unseller</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getseles")
@PY.OWNER
async def _(client, message):
    Sh = await message.reply("sedang memproses...")
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if not seles_users:
        return await Sh.edit("daftar seller kosong")

    seles_list = []
    for user_id in seles_users:
        try:
            user = await client.get_users(int(user_id))
            seles_list.append(
                f"👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | {user.id}"
            )
        except:
            continue

    if seles_list:
        response = (
            "📋 Daftar Seller :\n\n"
            + "\n".join(seles_list)
            + f"\n\n<blockquote.⚜️ Total Seller: {len(seles_list)}</blockquote>"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar seller")


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
        return await Sh.edit("pengguna tidak temukan")
    try:
        get_exp = await get_expired_date(user_id)
        sh = await client.get_users(user_id)
    except Exception as error:
        return await Sh.ediit(error)
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
"""
        )


@PY.BOT("addadmin")
async def _(client, message):
    user = message.from_user

    # OWNER dan SuperUltra aja yg bisa akses
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")
    if user.id != OWNER_ID and user.id not in superultra_users:
        return

    reply = message.reply_to_message
    args = message.text.split()[1:]

    # Tentukan target_id & durasi
    if reply:
        target_id = reply.from_user.id
        duration = args[0] if args else "1b"
    else:
        if not args:
            return await message.reply("""⛔ Cara penggunaan: `/addadmin user_id/username waktu`
Contoh:
- `/addadmin 1234567890 1b`
- `/addadmin @username 2b`
- Reply ke pesan user: `/addadmin 1b`
""")
        target_id = args[0]
        duration = args[1] if len(args) > 1 else "1b"

    # Konversi durasi ke bulan
    if duration.endswith("b") and duration[:-1].isdigit():
        months = int(duration[:-1])
    else:
        months = 1  # default 1 bulan

    msg = await message.reply("⏳ Memproses...")

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if target_user.id in admin_users:
        return await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Sudah admin
""")

    try:
        now = datetime.now(timezone("Asia/Jakarta"))

        # Kalau yg nambah SuperUltra → expired ikut SU
        if user.id in superultra_users:
            su_expired = await get_expired_date(user.id)
            if not su_expired or su_expired < now:
                return await msg.edit("⛔ SuperUltra kamu sudah expired!")
            expired_date = su_expired
        else:
            expired_date = now + relativedelta(months=months)

        await set_expired_date(target_user.id, expired_date)
        await add_to_vars(client.me.id, "ADMIN_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
⏳ Expired: `{expired_date.strftime('%d-%m-%Y')}`
🔹 Berhasil dijadikan Admin
""")
        # Notif ke Owner
        await client.send_message(
            OWNER_ID,
            f"""
**👤 Owner:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Customer Addadmin:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_date.strftime('%d-%m-%Y')}`
""",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("👑 Owner", callback_data=f"profil {message.from_user.id}"),
                        InlineKeyboardButton("Customer 👤", callback_data=f"profil {target_user.id}"),
                    ],
                ]
            ),
        )

    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.BOT("unadmin")
async def _(client, message):
    msg = await message.reply("sedang memproses...")

    # ambil list superultra
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    # kalau bukan OWNER & bukan superultra → langsung stop (tanpa respon)
    if message.from_user.id != OWNER_ID and message.from_user.id not in superultra_users:
        return

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"{message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
⎆  INFORMATION
⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
⎆ id: {user.id}
⎆ keterangan: tidak dalam daftar
"""
        )

    try:
        await remove_from_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
⎆ INFORMATION
⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
⎆ id: {user.id}
⎆ keterangan: unadmin
"""
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("getadmin")
@PY.OWNER
async def _(client, message):
    Sh = await message.reply("⏳ Sedang memproses...")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<s>Daftar admin kosong</s>")

    admin_list = []
    now = datetime.now(timezone("Asia/Jakarta"))
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            expired = await get_expired_date(user.id)
            if expired:
                expired_str = expired.strftime("%d-%m-%Y")
                status = "✅ Aktif" if expired >= now else "❌ Expired"
            else:
                expired_str = "∞"
                status = "∞"
            admin_list.append(
                f"👤 [{user.first_name}](tg://user?id={user.id}) | {user.id} | ⏳ {expired_str} ({status})"
            )
        except:
            continue

    if admin_list:
        response = (
            "📋 **Daftar Admin:**\n\n"
            + "\n".join(admin_list)
            + f"\n\n⚜️ Total Admin User: {len(admin_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("Tidak dapat mengambil daftar admin")


@PY.BOT("superultra")
async def _(client, message):
    user = message.from_user
    if user.id != OWNER_ID:
        return

    reply = message.reply_to_message
    args = message.text.split()[1:]

    # target & durasi
    if reply:
        target_id = reply.from_user.id
        duration = args[0] if args else "1b"
    else:
        if not args:
            return await message.reply("""⛔ Cara penggunaan: `/superultra user_id/username waktu`
Contoh:
- `/superultra 1234567890 1b`
- `/superultra @username 2b`
- Reply ke pesan user: `/superultra 1b`
""")
        target_id = args[0]
        duration = args[1] if len(args) > 1 else "1b"

    # parsing durasi
    months = int(duration[:-1]) if duration.endswith("b") and duration[:-1].isdigit() else 1

    msg = await message.reply("⏳ Memproses...")

    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    superultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")
    if target_user.id in superultra_users:
        return await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Sudah SuperUltra
""")

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired_date = now + relativedelta(months=months)

        await set_expired_date(target_user.id, expired_date)
        await add_to_vars(bot.me.id, "ULTRA_PREM", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
⏳ Expired: `{expired_date.strftime('%d-%m-%Y')}`
🔹 Berhasil dijadikan SuperUltra
""")

        await bot.send_message(
            OWNER_ID,
            f"""
**👤 Owner:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Customer SuperUltra:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_date.strftime('%d-%m-%Y')}`
""",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("👑 Owner", callback_data=f"profil {message.from_user.id}"),
                    InlineKeyboardButton("Customer 👤", callback_data=f"profil {target_user.id}"),
                ]]
            ),
        )
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")


@PY.BOT("unsuperultra")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("⏳ Sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            "⛔ Cara penggunaan: `/unsuperultra user_id/username` atau reply user"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")

    superultra_users = await get_list_from_vars(bot.me.id, "ULTRA_PREM")

    if user.id not in superultra_users:
        return await msg.edit(f"""
**👤 Nama:** {user.first_name}
🆔 ID: `{user.id}`
📚 Keterangan: Tidak dalam daftar SuperUltra
""")

    try:
        await remove_from_vars(bot.me.id, "ULTRA_PREM", user.id)
        await rem_expired_date(user_id)

        return await msg.edit(f"""
**👤 Nama:** {user.first_name}
🆔 ID: `{user.id}`
🗑️ Berhasil dihapus dari SuperUltra
""")
    except Exception as error:
        return await msg.edit(f"❌ Error: {error}")
        

@PY.BOT("getultra")
@PY.OWNER
async def _(client, message):
    prem = await get_list_from_vars(bot.me.id, "ULTRA_PREM")
    prem_users = []

    for user_id in prem:
        try:
            user = await client.get_users(user_id)
            prem_users.append(
                f"👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | {user.id}"
            )
        except Exception as error:
            return await message.reply(str(error))

    total_prem_users = len(prem_users)
    if prem_users:
        prem_list_text = "\n".join(prem_users)
        return await message.reply(
            f"📋 Daftar SuperUltra:\n\n{prem_list_text}\n\n⚜️ Total SuperUltra User: {total_prem_users}"
        )
    else:
        return await message.reply("🚫 Tidak ada pengguna SuperUltra saat ini")


@PY.UBOT("prem")
async def _(client, message):
    user = message.from_user

    # Ambil list seller, admin & superultra
    seles_users = [int(x) for x in await get_list_from_vars(client.me.id, "SELER_USERS")]
    admin_users = [int(x) for x in await get_list_from_vars(client.me.id, "ADMIN_USERS")]
    superultra_users = [int(x) for x in await get_list_from_vars(client.me.id, "ULTRA_PREM")]

    # Gabungkan semua role
    allowed_users = set(seles_users + admin_users + superultra_users + [OWNER_ID])

    if message.from_user.id not in allowed_users:
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

    # Cek permanen
    is_permanent = duration in ["0", "perma", "permanen"]

    if is_permanent:
        if user.id != OWNER_ID:
            return await message.reply("⛔ Hanya OWNER yang bisa memberikan premium permanen.")
        total_days = None  # permanen
    else:
        # Konversi ke hari
        if duration.endswith("b"):
            total_days = int(duration[:-1]) * 30 if duration[:-1].isdigit() else 30
        elif duration.endswith("h"):
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
        now = datetime.now(timezone("Asia/Jakarta"))

        if is_permanent:
            expired_date = None
            expired_str = "♾️ PERMANEN"
        else:
            dataexp = await get_expired_date(target_user.id)
            if dataexp and dataexp > now:
                expired_date = dataexp + timedelta(days=total_days)
            else:
                expired_date = now + timedelta(days=total_days)
            expired_str = expired_date.strftime("%d-%m-%Y %H:%M")

        # Simpan expired baru
        await set_expired_date(target_user.id, expired_date)

        # Tambah ke list PREM_USERS
        await add_to_vars(bot.me.id, "PREM_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Premium Aktif
⏳ Masa Aktif: {expired_str}
🔹 Silakan buka @{bot.me.username} untuk menggunakan userbot
""")

        # Notif owner
        await bot.send_message(
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
