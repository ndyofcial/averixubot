from gc import get_objects

from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent)

from PyroUbot import *

@PY.UBOT("msg")
@PY.TOP_CMD
async def msg_cmd(client, message):
    if not message.reply_to_message:
        return await message.reply(f"<code>{message.text}</code> [ʀᴇᴘʟʏ ᴛᴏ ᴜsᴇʀ - ᴛᴇxᴛ]")
    text = f"secret {id(message)}"
    await message.delete()
    x = await client.get_inline_bot_results(bot.me.username, text)
    await message.reply_to_message.reply_inline_bot_result(x.query_id, x.results[0].id)

@PY.INLINE("^secret")
@INLINE.QUERY
#async def _(client, inline_query):
#    await secret_inline(client, inline_query)
async def secret_inline(client, inline_query):
    m = [obj for obj in get_objects() if id(obj) == int(q.query.split()[1])][0]
    await client.answer_inline_query(
        q.id,
        cache_time=0,
        results=[
            (
                InlineQueryResultArticle(
                    title="pesan rahasia!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    text="💬 ʙᴀᴄᴀ ᴘᴇsᴀɴ ʀᴀʜᴀsɪᴀ 💬",
                                    url=f"https://t.me/{bot.me.username}?start=secretMsg_{int(q.query.split(None, 1)[1])}",
                                )
                            ],
                        ]
                    ),
                    input_message_content=InputTextMessageContent(f"<b>👉🏻 ᴀᴅᴀ ᴘᴇsᴀɴ ʀᴀʜᴀsɪᴀ ᴜɴᴛᴜᴋ ᴍᴜ ɴɪʜ:</b> <a href=tg://user?id={m.reply_to_message.from_user.id}>{m.reply_to_message.from_user.first_name} {m.reply_to_message.from_user.last_name or ''}</a>"),
                )
            )
        ],
    )


@PY.INLINE("^get_send")
async def _(client, inline_query):
    _id = int(inline_query.query.split()[1])
    m = next((obj for obj in get_objects() if id(obj) == _id), None)
    if m:
        await client.answer_inline_query(
            inline_query.id,
            cache_time=0,
            results=[
                InlineQueryResultArticle(
                    title="get send!",
                    reply_markup=m.reply_to_message.reply_markup,
                    input_message_content=InputTextMessageContent(
                        m.reply_to_message.text
                    ),
                )
            ],
        )
        
