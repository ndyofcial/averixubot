from PyroUbot.core.database import mongodb

prefixes = mongodb["PyroUbot"]["prefix"]

# ambil prefix user
async def get_pref(user_id: int) -> str:
    sh = await prefixes.find_one({"_id": user_id})
    if sh:
        prefix = sh.get("prefixesi")
        if prefix is None or prefix.lower() == "none":
            return ""  # kosong = tanpa prefix
        return prefix
    return "."  # fallback default

# set prefix
async def set_pref(user_id: int, prefix: str):
    await prefixes.update_one(
        {"_id": user_id}, {"$set": {"prefixesi": prefix}}, upsert=True
    )

# hapus prefix
async def rem_pref(user_id: int):
    await prefixes.update_one(
        {"_id": user_id}, {"$unset": {"prefixesi": ""}}, upsert=True
    )
