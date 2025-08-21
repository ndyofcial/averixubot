from pyrogram import Client, filters
from PyroUbot import PY

__MODULE__ = "ᴀᴜᴛᴏʀᴇᴘᴏʀᴛ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴀᴜᴛᴏʀᴇᴘᴏʀᴛ ⦫<b>

<blockquote>⎆ perintah :
ᚗ <code>{0}report</code> Query
⊷ Report Telegram, Group dan Chanel secara otomatis.

⎆ Contoh :
ᚗ <code>{0}report</code> target_username
ᚗ <code>{0}report</code> https://t.me/channel_link
ᚗ <code>{0}report</code> https://t.me/group_link
</blockquote>
"""

@PY.UBOT("report")
@PY.TOP_CMD
async def _(client, message):
    msg = await message.reply("🔍 Memproses laporan otomatis...")
    
    try:
        args = message.text.split(" ", 1)
        if len(args) < 2:
            return await msg.edit("⛔ Masukkan username atau link channel/grup!\nContoh:report target_username")

        target = args[1]

        # 🔹 Kirim laporan ke Grup Privat
        private_group = "https://t.me/+H9rN1IkjPi0wMTI1"  # Ganti dengan link grup privat
        report_text = f"""
<blockquote><b>⚠️ LAPORAN OTOMATIS ⚠️</b>
🔹 Target: {target}
🔹 Alasan: Spam, Penipuan, atau Konten Berbahaya
🔹 Dilaporkan oleh: {message.from_user.mention}

⚠️ Silakan cek dan tindak lanjut jika diperlukan.</blockquote>
        """
        await client.send_message(private_group, report_text)

        # 🔹 Kirim laporan ke Channel (jika ada)
        report_channel = "@storeberrish"  # Ganti dengan channel report
        await client.send_message(report_channel, report_text)

        # 🔹 Kirim laporan ke Telegram @NoToScam (Official Scam Report)
        await client.send_message("@NoToScam", f"/report {target} Penipuan, Spam, atau Konten Berbahaya.")

        await msg.edit(f"<blockquote>✅ Laporan berhasil dikirim ke:\n- **Grup Privat**\n- **Channel Report**\n- **@NoToScam Telegram**</blockquote>")

    except Exception as e:
        await msg.edit(f"❌ Gagal mengirim laporan:\n<code>{str(e)}</code>")
