import csv
import aiohttp
from pyrogram import Client, filters
from PyroUbot import PY
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

__MODULE__ = "ᴅᴏxxɪɴɢ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴅᴏxxɪɴɢ ⦫</b>

<blockquote>⎆ perintah :
ᚗ <code>{0}dox</code> nama/nik/nomor telpon
⊶ mencari data sesuai query.
</blockquote>
"""

# URL ke file data CSV di GitHub
GITHUB_CSV_URL = "https://raw.githubusercontent.com/Zamssprprpk/database/refs/heads/main/bpjs.csv"

# Dictionary untuk menyimpan hasil pencarian sementara
results = {}

async def fetch_data_from_github():
    """Mengambil data CSV dari GitHub."""
    async with aiohttp.ClientSession() as session:
        async with session.get(GITHUB_CSV_URL) as response:
            if response.status == 200:
                return await response.text()
            return None

@PY.UBOT("dox")
@PY.TOP_CMD
async def cari_data(client, message):
    query = message.text.split(maxsplit=1)
    if len(query) < 2:
        await message.reply_text("❌ Silakan masukkan nama, NIK, atau nomor telepon setelah perintah dox.")
        return

    pencarian = query[1].lower()
    hasil_pencarian = []

    try:
        # Ambil data dari GitHub
        csv_data = await fetch_data_from_github()
        if not csv_data:
            await message.reply_text("❌ Gagal mengambil data.")
            return

        # Parsing CSV
        reader = csv.DictReader(csv_data.splitlines())
        for row in reader:
            if (pencarian in row.get('NAME', '').strip().lower() or 
                pencarian in row.get('NIK', '').strip() or 
                pencarian in row.get('PHONE', '').strip()):
                hasil_pencarian.append(row)

        if hasil_pencarian:
            chat_id = message.chat.id
            results[chat_id] = hasil_pencarian  # Simpan hasil di dictionary
            await tampilkan_hasil(client, chat_id, 0, message)
        else:
            await message.reply_text("🔍 Tidak ditemukan hasil untuk pencarian tersebut.")

    except Exception as e:
        await message.reply_text(f"⚠️ Terjadi kesalahan: {e}")

async def tampilkan_hasil(client, chat_id, start_index, message):
    hasil = results.get(chat_id, [])
    if not hasil:
        await message.reply_text("❌ Tidak ada data untuk ditampilkan.")
        return

    end_index = start_index + 5
    results_to_show = hasil[start_index:end_index]

    response = "🔍 **Hasil Pencarian:**\n"
    response += "===================="
    for data in results_to_show:
        response += (f"""
<blockquote>ᚗ **NIK**: `{data.get('NIK', 'Sensor')}`
ᚗ **Nama:** `{data.get('NAME', '-')}`
ᚗ **Jenis Kelamin:** `{data.get('GENDER', '-')}`
ᚗ **Tanggal Lahir:** `{data.get('BIRTHDATE', '-')}`
ᚗ **Nomor Telepon:** `{data.get('PHONE', 'Sensor')}`
ᚗ **Alamat:** `{data.get('ADDRESS', '-')}`
ᚗ **Kota:** `{data.get('CITY', '-')}`
</blockquote>""")
        response += "===================="

    keyboard = []
    if end_index < len(hasil):
        keyboard.append([InlineKeyboardButton("📜 Lihat Selanjutnya", f"next_{chat_id}_{end_index}")])

    markup = InlineKeyboardMarkup(keyboard) if keyboard else None
    await client.send_message(chat_id, response, reply_markup=markup)

@PY.UBOT("next_data")
async def next_results(client, callback_query):
    data = callback_query.data.split("_")
    chat_id = int(data[1])
    start_index = int(data[2])
    
    await tampilkan_hasil(client, chat_id, start_index, callback_query.message)
