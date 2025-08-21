from geopy.geocoders import Nominatim
from PyroUbot import *

__MODULE__ = "ɢᴘs"
__HELP__ = """
<b>⦪ ʙᴀɴᴛᴜᴀɴ ᴜɴᴛᴜᴋ ɢᴘs ⦫</b>
<blockquote><b>
⎆ Perintah :
ᚗ <code>{0}gps</code>
⊶ Mencari lokasi mengunakan GPS atau Maps.</b></blockquote>
"""


@PY.UBOT("gps|maps")
async def gps(client, message):
    input_str = message.text.split(" ", 1)
    
    if len(input_str) < 2:
        return await message.reply("Mohon berikan tempat yang dicari.")
    
    input_str = input_str[1]
    await message.reply("Menemukan lokasi ini di server map...")
   
    geolocator = Nominatim(user_agent="bot")
    geoloc = geolocator.geocode(input_str)
    
    if geoloc:
        lon = geoloc.longitude
        lat = geoloc.latitude
        await message.reply_location(latitude=lat, longitude=lon)
    else:
        await message.reply("Saya tidak dapat menemukannya.")
