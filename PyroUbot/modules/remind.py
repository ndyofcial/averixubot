from datetime import datetime
from pyrogram import Client, filters
from pytz import timezone

from PyroUbot import *

__MODULE__ = "ʀᴇᴍɪɴᴅ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ʀᴇᴍɪɴᴅ ⦫</b>

<blockquote>⎆ ᴘᴇʀɪɴᴛᴀʜ :
ᚗ <code>{0}remind</code> tanggal waktu textremind

⌭ contoh :
ᚗ <code>{0}remind</code> 23/03/2025 16:45 beli mendoan

ᚗ <code>{0}listremind</code>
ᚗ Melihat daftar list reminder yang tersimpan.

⌭ ᴘᴇɴᴊᴇʟᴀsᴀɴ:
ᚗ reminders berguna sebagai pesan pengingat diwaktu kedepan</blockquote>
"""


reminders = []

@PY.UBOT("remind")
@PY.TOP_CMD
async def reminder(client, message):
    gagal = await EMO.GAGAL(client)
    
    if len(message.command) < 3:
        await message.reply(f"**__{gagal} Penggunaan: `.remind <tanggal> <waktu> <pesan>`\n\nContoh:\n`.remind 05/03/2025 10:23 VPS habis.`__**")
        return

    date_str = message.command[1]
    time_str = message.command[2]

    if message.reply_to_message:
        text_to_remind = message.reply_to_message.text
    else:
        if len(message.command) < 4:
            await message.reply(f"**__{gagal} Harap masukkan pesan pengingat atau reply pesan untuk diingatkan.__**")
            return
        text_to_remind = " ".join(message.command[3:])
        
    try:
        reminder_datetime = datetime.strptime(f"{date_str} {time_str}", "%d/%m/%Y %H:%M")
        reminder_datetime = timezone("Asia/Jakarta").localize(reminder_datetime)
    except ValueError:
        await message.reply(f"**__{gagal} Format tanggal atau waktu salah! Gunakan `DD/MM/YYYY HH:MM`.__**")
        return

    now = datetime.now(timezone("Asia/Jakarta"))

    if reminder_datetime < now:
        await message.reply(f"**__{gagal} Waktu pengingat sudah lewat! Harap masukkan waktu yang akan datang.__**")
        return

    reminders.append((reminder_datetime, text_to_remind))
    await client.send_message(message.chat.id, text_to_remind, schedule_date=reminder_datetime)
    await message.reply(f"<blockquote>**__✅ Pengingat disimpan, akan dikirim pada {reminder_datetime.strftime('%d/%m/%Y')} pukul {reminder_datetime.strftime('%H:%M')}.__**</blockquote>")

@PY.UBOT("listremind")
@PY.TOP_CMD
async def listrem(client, message):
    if len(reminders) == 0:
        await message.reply("**__Tidak ada pengingat yang tersimpan.__**")
    else:
        response = "**• Daftar Pengingat:**\n\n"
        for i, reminder in enumerate(reminders, start=1):
            t, text = reminder
            response += f"{i}. {text} - {t.strftime('%d/%m/%Y %H:%M')}\n"
        await message.reply(response)
