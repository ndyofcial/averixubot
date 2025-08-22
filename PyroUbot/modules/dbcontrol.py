from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone


from PyroUbot import *

__MODULE__ = "ᴅʙ ᴄᴏɴᴛʀᴏʟ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴅʙ ᴄᴏɴᴛʀᴏʟ ⦫</b>

<blockquote expandable>
⎆ perintah :
ᚗ <pre>.prem</pre> 1b
ᚗ <pre>.unprem</pre>
ᚗ <pre>.getprem</pre>

⎆ Cara Penggunaan: <pre>.prem username/userid waktu</pre>
ᚗ <pre>.prem 161626262 1b</pre> (1 bulan)
ᚗ <pre>.prem @username 15h</pre> (15 hari)
ᚗ <pre>.prem 1b</pre> (Gunakan reply ke user)

ᚗ <pre>.addadmin</pre>
ᚗ <pre>.unadmin</pre>
ᚗ <pre>.getadmin</pre>

ᚗ <pre>.seles</pre>
ᚗ <pre>.unseles</pre>
ᚗ <pre>.getseles</pre>

ᚗ <pre>.time</pre> id hari
  ⊶ Untuk Menambah / Mengurangi Masa Aktif User

ᚗ <pre>.cek</pre> id
  ⊶ Untuk Melihat Masa Aktif User
</blockquote>
"""

@PY.BOT("prem")
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")

    # ambil list seller, admin & superultra
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    # kalau bukan seller, bukan admin, bukan superultra → stop (tanpa respon)
    if (
        message.from_user.id not in seles_users
        and message.from_user.id not in admin_users
        and message.from_user.id not in superultra_users
        and message.from_user.id != OWNER_ID
    ):
        return

    if not user_id:
        return await msg.edit(f"<b>{message.text} ᴜsᴇʀ_ɪᴅ/ᴜsᴇʀɴᴀᴍᴇ - ʙᴜʟᴀɴ</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id in prem_users:
        return await msg.edit(f"""
<blockquote><b>⎆ ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>⎆ ɪᴅ: {user.id}</b>
<b>⎆ ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ꜱᴜᴅᴀʜ ᴘʀᴇᴍɪᴜᴍ</b>
<b>⎆ ᴇxᴘɪʀᴇᴅ: {get_bulan} ʙᴜʟᴀɴ</b></blockquote>
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "PREM_USERS", user.id)
        await msg.edit(f"""
<blockquote><b>⎆ ɴᴀᴍᴇ: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
<b>⎆ ɪᴅ: {user.id}</b>
<b>⎆ ᴇxᴘɪʀᴇᴅ: {get_bulan} ʙᴜʟᴀɴ</b>
<b>⎆ ꜱɪʟᴀʜᴋᴀɴ ʙᴜᴋᴀ @{client.me.username} ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴜꜱᴇʀʙᴏᴛ</b></blockquote>

<blockquote>⎆ sɪʟᴀʜᴋᴀɴ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ :
ᚗ /start ʙᴏᴛ @usnbot
ᚗ ᴋᴀʟᴀᴜ sᴜᴅᴀʜ sᴛᴀʀᴛ ʙᴏᴛ sɪʟᴀʜᴋᴀɴ ᴘᴇɴᴄᴇᴛ ᴛᴏᴍʙᴏʟ ʙᴜᴀᴛ ᴜsᴇʀʙᴏᴛ 
ᚗ ɴᴀʜ ɴᴀɴᴛɪ ᴀᴅᴀ ᴀʀᴀʜᴀɴ ᴅᴀʀɪ ʙᴏᴛ ɴʏᴀ</blockquote>
<blockquote><b>⎆ ɴᴏᴛᴇ : ᴊᴀɴɢᴀɴ ʟᴜᴘᴀ ʙᴀᴄᴀ ᴀʀᴀʜᴀɴ ᴅᴀʀɪ ʙᴏᴛ ɴʏᴀ</b></blockquote>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"🆔 id-seller: {message.from_user.id}\n\n🆔 id-customer: {user_id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔱 seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "customer ⚜️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("unprem")
async def _(client, message):
    msg = await message.reply("sedang memproses...")

    # ambil list seller, admin & superultra
    seles_users = await get_list_from_vars(client.me.id, "SELER_USERS")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    # kalau bukan seller, bukan admin, bukan superultra, bukan OWNER → stop (tanpa respon)
    if (
        message.from_user.id not in seles_users
        and message.from_user.id not in admin_users
        and message.from_user.id not in superultra_users
        and message.from_user.id != OWNER_ID
    ):
        return

    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(f"<b>{message.text} user_id/username</b>")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(client.me.id, "PREM_USERS")

    if user.id not in prem_users:
        return await msg.edit(f"""
 ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 <blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
 <b>⎆ id: {user.id}</b>
 <b>⎆ keterangan: tidak dalam daftar</b></blockquote>
"""
        )
    try:
        await remove_from_vars(client.me.id, "PREM_USERS", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
 ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 <blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
 <b>⎆ id: {user.id}</b>
 <b>⎆ keterangan: unpremium</b></blockquote>
"""
        )
    except Exception as error:
        return await msg.edit(error)
        

@PY.BOT("getprem")
@PY.OWNER
async def _(client, message):
    text = ""
    count = 0
    prem = await get_list_from_vars(client.me.id, "PREM_USERS")
    prem_users = []

    for user_id in prem:
        try:
            user = await bot.get_users(user_id)
            count += 1
            userlist = f"• {count}: <a href=tg://user?id={user.id}>{user.first_name} {user.last_name or ''}</a> > <code>{user.id}</code>"
        except Exception:
            continue
        text += f"<blockquote><b>{userlist}\n</blockquote></b>"
    if not text:
        await message.reply_text("ᴛɪᴅᴀᴋ ᴀᴅᴀ ᴘᴇɴɢɢᴜɴᴀ ʏᴀɴɢ ᴅɪᴛᴇᴍᴜᴋᴀɴ")
    else:
        await message.reply_text(text)


@PY.BOT("seles")
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

    if user.id in seles_users:
        return await msg.edit(f"""
 ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 <blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
 <b>⎆ id: {user.id}</b>
 <b>⎆ keterangan: sudah seller</b></blockquote>
"""
        )

    try:
        await add_to_vars(client.me.id, "SELER_USERS", user.id)
        return await msg.edit(f"""
 ɪɴғᴏʀᴍᴀᴛɪᴏɴ :
 <blockquote><b>⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})</b>
 <b>⎆ id: {user.id}</b>
 <b>⎆ keterangan: seller</b></blockquote>
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
                f"<blockquote><b>👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | <code>{user.id}</code></blockquote></b>"
            )
        except:
            continue

    if seles_list:
        response = (
            "📋 ᴅᴀғᴛᴀʀ sᴇʟʟᴇʀ:\n\n"
            + "\n".join(seles_list)
            + f"\n\n<blockquote.⚜️ total seller: {len(seles_list)}</blockquote>"
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
        return await Tm.edit(f"woi bang ! \n🗿mohon gunakan /set_time user_id hari")
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
    msg = await message.reply("sedang memproses...")

    # ambil list superultra
    superultra_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    # kalau bukan OWNER & bukan superultra → tolak
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

    if user.id in admin_users:
        return await msg.edit(f"""
⎆ INFORMATION
⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
⎆ id: {user.id}
⎆ keterangan: sudah dalam daftar
"""
        )

    try:
        await add_to_vars(client.me.id, "ADMIN_USERS", user.id)
        return await msg.edit(f"""
⎆ INFORMATION
⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
⎆ id: {user.id}
⎆ keterangan: admin
"""
        )
    except Exception as error:
        return await msg.edit(error)


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
    Sh = await message.reply("sedang memproses...")
    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if not admin_users:
        return await Sh.edit("<s>daftar admin kosong</s>")

    admin_list = []
    for user_id in admin_users:
        try:
            user = await client.get_users(int(user_id))
            admin_list.append(
                f"👤 [{user.first_name} {user.last_name or ''}](tg://user?id={user.id}) | {user.id}"
            )
        except:
            continue

    if admin_list:
        response = (
            "📋 daftar admin:\n\n"
            + "\n".join(admin_list)
            + f"\n\n⚜️ total admin: {len(admin_list)}"
        )
        return await Sh.edit(response)
    else:
        return await Sh.edit("tidak dapat mengambil daftar admin")

@PY.BOT("superultra")
@PY.OWNER
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")
    if not user_id:
        return await msg.edit(f"{message.text} user_id/username")

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)
    if not get_bulan:
        get_bulan = 1

    prem_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id in prem_users:
        return await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> {user.id}
<b>keterangan: sudah</b> <code>[SuperUltra]</code>
<b>expired:</b> <code>{get_bulan}</code> <b>bulan</b>
"""
        )

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + relativedelta(months=int(get_bulan))
        await set_expired_date(user_id, expired)
        await add_to_vars(client.me.id, "ULTRA_PREM", user.id)
        await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>expired:</b> <code>{get_bulan}</code> <b>bulan</b>
<b>ꜱilahkan buka</b> @{client.me.mention} <b>untuk membuat uꜱerbot</b>
<b>status : </b><code>[SuperUltra]</code>
"""
        )
        return await bot.send_message(
            OWNER_ID,
            f"🆔 id-seller: {message.from_user.id}\n\n🆔 id-customer: {user_id}",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "🔱 seller",
                            callback_data=f"profil {message.from_user.id}",
                        ),
                        InlineKeyboardButton(
                            "customer ⚜️", callback_data=f"profil {user_id}"
                        ),
                    ],
                ]
            ),
        )
    except Exception as error:
        return await msg.edit(error)


@PY.BOT("rmultra")
@PY.OWNER
async def _(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"{message.text} user_id/username"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    prem_users = await get_list_from_vars(client.me.id, "ULTRA_PREM")

    if user.id not in prem_users:
        return await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan: tidak dalam daftar</b>
"""
        )
    try:
        await remove_from_vars(client.me.id, "ULTRA_PREM", user.id)
        await rem_expired_date(user_id)
        return await msg.edit(f"""
<b>name:</b> [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
<b>id:</b> <code>{user.id}</code>
<b>keterangan: none superultra</b>
"""
        )
    except Exception as error:
        return await msg.edit(error)
        

@PY.BOT("getultra")
@PY.OWNER
async def _(client, message):
    prem = await get_list_from_vars(client.me.id, "ULTRA_PREM")
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
            f"📋 daftar superultra:\n\n{prem_list_text}\n\n⚜️ total superultra: {total_prem_users}"
        )
    else:
        return await message.reply("tidak ada pengguna superultra saat ini")


@PY.UBOT("prem")
async def _(client, message):
    user = message.from_user

    # Ambil semua role terbaru
    seller_id = [int(x) for x in await get_list_from_vars(bot.me.id, "SELER_USERS")]
    admin_id  = [int(x) for x in await get_list_from_vars(bot.me.id, "ADMIN_USERS")]

    # Cek akses sesuai prioritas role
    if user.id != OWNER_ID and user.id not in admin_id and user.id not in seller_id:
        return await message.reply("❌ Kamu tidak punya akses untuk menggunakan perintah ini.")

    # Ambil user_id dan durasi
    reply = message.reply_to_message
    if reply:
        target_id = reply.from_user.id
        args = message.text.split(maxsplit=1)
        duration = args[1] if len(args) > 1 else "1b"
    else:
        args = message.text.split()[1:]
        if not args:
            return await message.reply("""⛔ Cara penggunaan: `.prem user_id/username waktu`
Contoh:
- `.prem 161626262 1b` (1 bulan)
- `.prem @username 15h` (15 hari)
- Reply ke pesan user: `.prem 1b`
""")
        target_id = args[0]
        duration = args[1] if len(args) > 1 else "1b"

    # Konversi durasi ke hari
    if duration.endswith("b"):
        total_days = int(duration[:-1]) * 30 if duration[:-1].isdigit() else 30
    elif duration.endswith("h"):
        total_days = int(duration[:-1]) if duration[:-1].isdigit() else 1
    else:
        total_days = 30  # default 1 bulan

    # Tentukan maksimal hari berdasarkan role
    if user.id == OWNER_ID:
        max_days = 3650
    elif user.id in admin_id:
        max_days = 180
    elif user.id in seller_id:
        max_days = 30
    else:
        return await message.reply("⛔ Kamu tidak punya akses ke perintah ini.")

    if total_days > max_days:
        return await message.reply(f"⛔ Maksimal kamu hanya bisa memberikan {max_days} hari.")

    msg = await message.reply("⏳ Memproses...")

    # Ambil data target user
    try:
        target_user = await client.get_users(target_id)
    except Exception as e:
        return await msg.edit(f"❌ Error: {e}")

    # Cek expired target
    dataexp = await get_expired_date(target_user.id)
    expired_str = dataexp.astimezone(timezone("Asia/Jakarta")).strftime("%d-%m-%Y %H:%M") if dataexp else "⛔ Belum berlangganan"

    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS")
    if target_user.id in prem_users:
        return await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
📚 Keterangan: Sudah Premium
⏳ Masa Aktif: {expired_str}
""")

    # Set expired dan tambahkan ke PREM_USERS
    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired_date = now + timedelta(days=total_days)

        await set_expired_date(target_user.id, expired_date)
        await add_to_vars(bot.me.id, "PREM_USERS", target_user.id)

        await msg.edit(f"""
**👤 Nama:** {target_user.first_name}
🆔 ID: `{target_user.id}`
⏳ Expired: `{expired_date.strftime('%d-%m-%Y')}`
🔹 Silakan buka @{bot.me.username} untuk menggunakan userbot
""")

        # Notifikasi ke owner
        await bot.send_message(
            OWNER_ID,
            f"""
**👤 Seller/Admin:** {message.from_user.first_name} (`{message.from_user.id}`)
**👤 Customer:** {target_user.first_name} (`{target_user.id}`)
⏳ Expired: `{expired_date.strftime('%d-%m-%Y')}`
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
