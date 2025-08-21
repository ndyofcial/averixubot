from gc import get_objects
from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent, MessageEntity, InlineKeyboardMarkup, InlineKeyboardButton
from PyroUbot import *

__MODULE__ = "ʙᴜᴛᴛᴏɴ"
__HELP__ = """
<b>⦪ ʙᴜᴛᴛᴏɴ ⦫</b>

<blockquote><b>⎆  ᴘᴇʀɪɴᴛᴀʜ:
ᚗ <code>{0}button</code> ᴛᴇxᴛ ~> ʙᴜᴛᴛᴏɴ_ᴛᴇxᴛ:ʙᴜᴛᴛᴏɴ_ʟɪɴᴋ
ᚗ ᴜɴᴛᴜᴋ ᴍᴇᴍʙᴜᴀᴛ ᴛᴏᴍʙᴏʟ ɪɴʟɪɴᴇ
ᚗ contoh :
<code>{0}button</code> text ~> name1:link1 | name2:link2 - name3:link3
</b></blockquote>
"""

def extract_formatted_text(message):
    if not message.entities:
        return message.text

    text = message.text
    entities = sorted(message.entities, key=lambda e: e.offset)
    formatted_text = ""
    last_offset = 0

    for entity in entities:
        formatted_text += text[last_offset:entity.offset]
        entity_text = text[entity.offset : entity.offset + entity.length]

        if entity.type == "bold":
            formatted_text += f"<b>{entity_text}</b>"
        elif entity.type == "italic":
            formatted_text += f"<i>{entity_text}</i>"
        elif entity.type == "code":
            formatted_text += f"<code>{entity_text}</code>"
        elif entity.type == "pre":
            formatted_text += f"<pre>{entity_text}</pre>"
        elif entity.type == "underline":
            formatted_text += f"<u>{entity_text}</u>"
        elif entity.type == "strikethrough":
            formatted_text += f"<s>{entity_text}</s>"
        elif entity.type == "custom_emoji":
            formatted_text += f"<tg-emoji emoji-id='{entity.custom_emoji_id}'></tg-emoji>"
        else:
            formatted_text += entity_text

        last_offset = entity.offset + entity.length

    formatted_text += text[last_offset:]
    return formatted_text

async def create_button(m):
    keyboard = []
    formatted_text = extract_formatted_text(m)
    
    command_text = m.text.split(" ", 1)[1] if " " in m.text else ""
    
    if "~>" not in command_text:
        return None, "Format salah! Gunakan .button text ~> name1:link1 | name2:link2 - name3:link3"
    
    text, buttons_data = command_text.split("~>", 1)
    rows = buttons_data.strip().split(" - ")
    
    for row in rows:
        buttons = []
        for button_data in row.split(" | "):
            try:
                button_text, button_url = button_data.split(":", 1)
                buttons.append(InlineKeyboardButton(button_text.strip(), url=button_url.strip()))
            except ValueError:
                return None, "Format tombol salah! Gunakan name:url"
        
        keyboard.append(buttons)
    
    return InlineKeyboardMarkup(keyboard), text.strip()

@PY.UBOT("button")
async def cmd_button(client, message):
    if len(message.command) < 2:
        return await message.reply("Format salah! Gunakan .button text ~> button_name:link_url")
    if "~>" not in message.text:
        return await message.reply(
            "Penggunaan Salah, Contoh : .button text ~> dana:t.me/hhh. Jika Ingin Membuat Tombol Berbaris :\n\n .button text ~> hi:url | pe:url - pepe: url"
        )
    await message.delete()
    try:
        x = await client.get_inline_bot_results(
            bot.me.username, f"get_button {id(message)}"
        )
        msg = message.reply_to_message or message
        await client.send_inline_bot_result(
            message.chat.id, x.query_id, x.results[0].id, reply_to_message_id=msg.id
        )
    except Exception as error:
        await message.reply(str(error))

@PY.INLINE("^get_button")
async def inline_button(client, inline_query):
    get_id = int(inline_query.query.split(None, 1)[1])
    m = next((obj for obj in get_objects() if id(obj) == get_id), None)
    if not m:
        return
    buttons, text = await create_button(m)
    await client.answer_inline_query(
        inline_query.id,
        cache_time=0,
        results=[
            InlineQueryResultArticle(
                title="Get Button!",
                reply_markup=buttons,
                input_message_content=InputTextMessageContent(text),
            )
        ],
    )