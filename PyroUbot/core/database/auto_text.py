from PyroUbot.core.database import mongodb

autobc = mongodb["PyroUbot"]["autobc"]

async def add_auto_text(user_id, message_id):
    await autobc.update_one(
        {"user_id": user_id},
        {"$push": {"messages": message_id}},
        upsert=True
    )

async def get_auto_text(user_id):
    user_data = await autobc.find_one({"user_id": user_id})
    return user_data["messages"] if user_data else []

async def remove_auto_text(user_id, index=None):
    if index is None:
        await autobc.delete_one({"user_id": user_id})
    else:
        user_data = await autobc.find_one({"user_id": user_id})
        if user_data and 0 <= index < len(user_data["messages"]):
            user_data["messages"].pop(index)
            await autobc.update_one(
                {"user_id": user_id},
                {"$set": {"messages": user_data["messages"]}}
            )
            
