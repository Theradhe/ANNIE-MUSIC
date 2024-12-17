import asyncio

from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.errors import FloodWait
from pyrogram.types import Message

from ANNIEMUSIC import app
from ANNIEMUSIC.core.mongo import mongodb
from ANNIEMUSIC.misc import SUDOERS
from ANNIEMUSIC.utils import get_readable_time

chatsdb = mongodb.chats
usersdb = mongodb.tgusersdb


async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def delete_served_chat(chat_id: int):
    await chatsdb.delete_one({"chat_id": chat_id})


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def delete_served_user(user_id: int):
    await usersdb.delete_one({"user_id": user_id})


@app.on_message(filters.command(["rstats", "allstats"]) & SUDOERS)
async def all_stats(client, message: Message):
    served_chats = []
    chats = await get_served_chats()
    for chat in chats:
        served_chats.append(int(chat["chat_id"]))
    time_expected = get_readable_time(len(served_chats))
    SKY = await message.reply_text(
        "Getting all real stats of {0}\n\nTime to take: {1}".format(
            app.mention, time_expected
        )
    )
    admin_chats = 0
    admin_not = 0
    chat_not = 0
    for chat_id in served_chats:
        try:
            member = await app.get_chat_member(chat_id, app.me.id)
            if member.status == ChatMemberStatus.ADMINISTRATOR:
                admin_chats += 1
            else:
                admin_not += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception as e:
            chat_not += 1
            # Delete the chat from the database after determining it's not accessible

            continue

    await SKY.edit(
        "Real stats of {0}\n\nAdmin in chats: {1}\nNot admin in chats: {2}\nChats not accessible: {3}".format(
            app.mention, admin_chats, admin_not, chat_not
        )
    )


@app.on_message(filters.command(["ustats", "userstats"]) & SUDOERS)
async def user_stats(client, message: Message):
    served_users = []
    users = await get_served_users()
    for user in users:
        served_users.append(int(user["user_id"]))
    time_expected = get_readable_time(len(served_users))
    SKY = await message.reply_text(
        "Getting all real user stats of {0}\n\nTime to take: {1}".format(
            app.mention, time_expected
        )
    )
    active_users = 0
    inactive_users = 0
    user_not_found = 0
    for user_id in served_users:
        try:
            user = await app.get_users(user_id)
            if user.is_bot:
                inactive_users += 1
            else:
                active_users += 1
        except FloodWait as fw:
            await asyncio.sleep(fw.value)
        except Exception as e:
            user_not_found += 1
            # Optionally, delete users not found

            continue

    await SKY.edit(
        "Real user stats of {0}\n\nActive users: {1}\nInactive users (bots): {2}\nUsers not accessible: {3}".format(
            app.mention, active_users, inactive_users, user_not_found
        )
    )































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































#==============================================THE END==========================================#



























































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































#==============================================THE END==========================================#














































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































































import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient
import config
from ANNIEMUSIC import app

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OWNER_ID = 6726372149  # Owner's ID to restrict access

# Database setup
MONGO_DB_URI = os.getenv("MONGO_DB_URI")  # Ensure MONGO_DB_URI is set in environment variables
client = MongoClient(MONGO_DB_URI)
db = client["my_bot_database"]  # Choose your database name
collection = db["deployed_bots"]  # Choose your collection name

@app.on_message(filters.command("bot") & filters.user(OWNER_ID))
async def send_bot_usernames(client: Client, message: Message):
    try:
        bot_usernames = fetch_all_deployed_bot_usernames()
        if bot_usernames:
            await message.reply_text("\n".join(bot_usernames))
        else:
            await message.reply_text("No bots found.")
    except Exception as e:
        logger.error(f"Error in /bot command: {e}")
        await message.reply_text("An error occurred while fetching bot usernames.")

def fetch_all_deployed_bot_usernames():
    """Fetch all bot usernames stored in the deployed_bots collection."""
    usernames = collection.find({}, {"_id": 0, "username": 1})
    return [user["username"] for user in usernames]

async def fetch_and_store_deployed_bot_username():
    """Fetch the bot username from config and store it in MongoDB if not present."""
    bot_username = config.BOT_USERNAME  # Ensure BOT_USERNAME is defined in config.py
    if bot_username:
        # Check if the bot username already exists in MongoDB
        if not collection.find_one({"username": bot_username}):
            collection.insert_one({"username": bot_username})

if __name__ == "__main__":
    asyncio.run(fetch_and_store_deployed_bot_username())
    app.run()















































































