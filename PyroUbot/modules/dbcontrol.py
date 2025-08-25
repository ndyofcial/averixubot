from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pytz import timezone


from PyroUbot import *

__MODULE__ = "ᴅʙ ᴄᴏɴᴛʀᴏʟ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴅʙ ᴄᴏɴᴛʀᴏʟ ⦫</b>
<blockquote>
⎆ perintah :
ᚗ <code>{0}prem</code> 1b
ᚗ <code>{0}unprem</code>
ᚗ <code>{0}getprem</code>

⎆ Cara Penggunaan: <code>.prem username/userid waktu</code>
ᚗ <code>.prem 161626262 1b</code> (1 bulan)
ᚗ <code>.prem @username 15h</code> (15 hari)
ᚗ <code>.prem 1b</code> (Gunakan reply ke user)

ᚗ <code>{0}addadmin</code>
ᚗ <code>{0}unadmin</code>
ᚗ <code>{0}getadmin</code>

ᚗ <code>{0}seles</code>
ᚗ <code>{0}unseles</code>
ᚗ <code>{0}getseles</code></blockquote>

ᚗ <code>{0}time</code> id hari
  ⊶ Untuk Menambah - Mengurangi Masa Aktif User

ᚗ <code>{0}cek</code> id
  ⊶ Untuk Melihat Masa Aktif User</blockquote></b>
"""

#@PY.BOT("prem")
#@PY.SELLER
async def _(client, message):
    user_id, get_bulan = await extract_user_and_reason(message)
    msg = await message.reply("memproses...")
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
<b>⎆ ᴋᴇᴛᴇʀᴀɴɢᴀɴ: ꜱᴜᴅᴀʜ ᴘʀᴇᴍɪᴜᴍ</ci></b>
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
@PY.OWNER
async def _(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/username</b>"
        )

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
@PY.ADMIN
async def _(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/username</b>"
        )

    try:
        user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(error)

    sudo_users = await get_list_from_vars(client.me.id, "SELER_USERS")

    if user.id in sudo_users:
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
@PY.OWNER
async def _(client, message):
    msg = await message.reply("sedang memproses...")
    user_id = await extract_user(message)
    if not user_id:
        return await msg.edit(
            f"<b>{message.text} user_id/username</b>"
        )

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


@PY.BOT("time")
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

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id in admin_users:
        return await msg.edit(f"""
⎆ INFORMATION
⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
id: {user.id}
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

    admin_users = await get_list_from_vars(client.me.id, "ADMIN_USERS")

    if user.id not in admin_users:
        return await msg.edit(f"""
⎆  INFORMATION
⎆ name: [{user.first_name} {user.last_name or ''}](tg://user?id={user.id})
⎆ id: {user.id}
⎆ keterangan: tidak daam daftar
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
    reseller_id = await get_list_from_vars(bot.me.id, "SELER_USERS")
    admin_id = await get_list_from_vars(bot.me.id, "ADMIN_USERS")
    if user.id not in reseller_id:
        return
    reply = message.reply_to_message
    args = message.text.split(maxsplit=2)[1:] if not reply else [str(reply.from_user.id)] + message.text.split(maxsplit=1)[1:]
    
    if not args:
        return await message.reply(f"""
<blockquote>**__⛔ Cara Penggunaan: <code>.prem username/userid waktu</code>

‼️Contoh:
- <code>.prem 161626262 1b</code> (1 bulan)
- <code>.prem @username 15h</code> (15 hari)
- <code>.prem 1b</code> (Gunakan reply ke user)__**</blockquote>""")

    user_id, duration = args[0], args[1] if len(args) > 1 else "1b"

    if duration.endswith("b"):
        duration_value = int(duration[:-1]) if duration[:-1].isdigit() else 1
        total_days = duration_value * 30
    elif duration.endswith("h"):
        duration_value = int(duration[:-1]) if duration[:-1].isdigit() else 1
        total_days = duration_value
    else:
        total_days = 30  

    if user.id in reseller_id and total_days > 30:
        return await message.reply("<b>⛔ Reseller hanya bisa memberikan maksimal 1 bulan (30 hari).</b>")
    if user.id in admin_id and total_days > 180:
        return await message.reply("<b>⛔ Admin hanya bisa memberikan maksimal 6 bulan (180 hari).</b>")
    if user.id == OWNER_ID and total_days > 3650:
        return await message.reply("<b>⛔ Maksimal premium adalah 10 tahun (3650 hari).</b>")

    msg = await message.reply("**__⏳ Memproses...__**")

    try:
        target_user = await client.get_users(user_id)
    except Exception as error:
        return await msg.edit(f"**__⛔ Error: {error}__**")

    dataexp = await get_expired_date(user.id)
    if not dataexp:
        expired = "⛔ Belum berlangganan"
    else:
        expired = dataexp.astimezone(timezone("Asia/Jakarta")).strftime("%d-%m-%Y %H:%M")
    prem_users = await get_list_from_vars(bot.me.id, "PREM_USERS")
    if target_user.id in prem_users:
        return await msg.edit(f"""
<blockquote>**__👤 Nama: <a href='tg://user?id={target_user.id}'>{target_user.first_name}</a>
🆔 ID: <code>{target_user.id}</code>
📚 Keterangan: Sudah Premium
⏳ Masa Aktif: {expired}__**</blockquote>
        """)

    try:
        now = datetime.now(timezone("Asia/Jakarta"))
        expired = now + timedelta(days=total_days)

        await set_expired_date(target_user.id, expired)
        await add_to_vars(bot.me.id, "PREM_USERS", target_user.id)

        await msg.edit(f"""
<blockquote>**__👤 Nama: <a href='tg://user?id={target_user.id}'>{target_user.first_name}</a>
🆔 ID: <code>{target_user.id}</code>
⏳ Expired: <code>{expired.strftime('%d-%m-%Y')}</code>

🔹 Silakan buka @{bot.me.username}
📚 Penggunaan:
• Ketik /start 
• Lalu Teken Tombol Buat Userbot, Dan Baca Langkah Langkahnya..__**</blockquote>
        """)

        return await bot.send_message(
            OWNER_ID,
            f"""
<blockquote>**__👤 Seller/Admin: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> (`{message.from_user.id}`)
👤 Customer: <a href='tg://user?id={target_user.id}'>{target_user.first_name}</a> (`{target_user.id}`)
⏳ Expired: <code>{expired.strftime('%d-%m-%Y')}</code>__**</blockquote>
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
        return await msg.edit(f"<b>❌ Error:</b> {error}")
