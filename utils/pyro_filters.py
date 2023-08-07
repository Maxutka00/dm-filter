from pyrogram import filters, Client
from pyrogram.types import Message


async def empty_chat(flt, app: Client, message: Message):
    if message.chat.id == 357405415:
        return True
    if (await app.search_messages_count(message.chat.id)) == 1:
        return True
    return False

empty_chat_filter = filters.create(empty_chat)