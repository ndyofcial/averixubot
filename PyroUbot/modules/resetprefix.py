from PyroUbot import *

@PY.UBOT("resetprefix")
@PY.TOP_CMD
async def reset_prefixes(client, ubot):
    ub_prefix = ["."]
    _my_id = await get_list_from_vars(bot.me.id, "PREM_USERS")
    prs = await EMO.PROSES(client)
    if message.from_user.id not in ubot._my_id:
        return await prs.edit(
            "<b>ANAK DAJJAL !! SADAR DIRI LAG GOBLOK. LO TUH BUKAN PENGGUNA GW, DASAR MMG GA TAU DIRI LO . BAJINGAN, DAJJAL.</b>"
        )
    client.set_prefix(message.from_user.id, ub_prefix)
    await set_pref(message.from_user.id, ub_prefix)
  
    await prs.delete()
    return await message.reply(
        f"<b>Prefix lo berhasil direset menjadi {' '.join(ub_prefix)} .</b>",
        reply_markup=key,
    )
