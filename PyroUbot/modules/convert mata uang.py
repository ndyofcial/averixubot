import requests
from pyrogram import Client, filters
from PyroUbot import PY
from pyrogram.types import Message

__MODULE__ = "ᴄᴏɴᴠᴇʀᴛ ᴄᴜʀʀᴇɴᴄʏ"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ᴄᴏɴᴠᴇʀᴛ ᴄᴜʀʀᴇɴᴄʏ ⦫</b>

<blockquote>⎆ perintah :
ᚗ <code>{0}convert</code> 50000 IDR USD
⊶ Mengubah 50000 IDR ke USD

ᚗ Query :
⊶ IDR Rupiah Indonesia
⊶ USD United States Dollar
⊶ MYR Malaysian Ringgit
⊶ RUB Russian Ruble
⊶ INR Indian Rupee
</blockquote>
"""
def emoji(alias):
    emojis = {
        "COIN": "<emoji id=5872804530973840220>💲</emoji>",    
        "CONV": "<emoji id=5377336227533969892>💱</emoji>",
        "ANALISIS": "<emoji id=5251569715272248625>💎</emoji>",
        "ANALISISB": "<emoji id=6154275405990727821>🔸</emoji>",                
    }
    return emojis.get(alias, "⎆")


coin = emoji("COIN")
conv = emoji("CONV")
anal = emoji("ANALISIS")
analb = emoji("ANALISISB")

API_URL = "https://api.exchangerate-api.com/v4/latest/"

@PY.UBOT("convert")
@PY.TOP_CMD
async def convert_currency(client: Client, message: Message):
    args = message.text.split()
    
    if len(args) != 4:
        return await message.reply("⛔ Format salah! Gunakan: `/convert [jumlah] [dari] [ke]`.\n\nContoh: `/convert 50000 IDR USD`")

    try:
        amount = float(args[1])
        from_currency = args[2].upper()
        to_currency = args[3].upper()

        # Ambil data nilai tukar terbaru
        response = requests.get(f"{API_URL}{from_currency}")
        data = response.json()

        if "rates" not in data:
            return await message.reply("⛔ Mata uang tidak ditemukan atau tidak didukung!")

        # Hitung konversi
        if to_currency not in data["rates"]:
            return await message.reply("⛔ Mata uang tujuan tidak tersedia!")

        converted_amount = amount * data["rates"][to_currency]
        await message.reply(f"<blockquote>{coin} **Konversi Mata Uang** {coin}\n\n{conv} {amount} {from_currency} ≈ **{converted_amount:.2f} {to_currency}**</blockquote>")

    except ValueError:
        await message.reply("⛔ Jumlah harus berupa angka!")
    except Exception as e:
        await message.reply(f"⛔ Terjadi kesalahan: {e}")
