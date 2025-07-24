from info import *
from utils import *
from asyncio import sleep
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.group & filters.new_chat_members)
async def new_group(bot, message):
    bot_id = (await bot.get_me()).id
    member = [u.id for u in message.new_chat_members]        
    if bot_id in member:
        await add_group(group_id=message.chat.id, 
                        group_name=message.chat.title,
                        user_name=message.from_user.first_name, 
                        user_id=message.from_user.id, 
                        channels=[],
                        f_sub=False,
                        verified=False)
        m = await message.reply(
            f"<b>☤ 𝘔𝘦𝘳𝘤𝘪 𝘥'𝘢𝘷𝘰𝘪𝘳 𝘢𝘫𝘰𝘶𝘵𝘦́ 𝘮𝘰𝘪 𝘥𝘢𝘯𝘴 {message.chat.title} 🎉\n\n"
            f"• 𝘕'𝘰𝘶𝘣𝘭𝘪𝘦 𝘱𝘢𝘴 𝘥𝘦 𝘮𝘦 𝘱𝘢𝘴𝘴𝘦𝘳 𝘢𝘥𝘮𝘪𝘯\n\n"
            f"• 𝘗𝘰𝘶𝘳 𝘢𝘤𝘵𝘪𝘷𝘦𝘳 𝘭𝘦 𝘣𝘰𝘵, 𝘶𝘵𝘪𝘭𝘪𝘴𝘦 𝘭𝘢 𝘤𝘰𝘮𝘮𝘢𝘯𝘥𝘦 /verify\n\n"
            f"• 𝘚𝘪 𝘵𝘶 𝘢𝘴 𝘥𝘦𝘴 𝘥𝘰𝘶𝘵𝘦𝘴, 𝘤𝘭𝘪𝘲𝘶𝘦 𝘴𝘶𝘳 𝘭𝘦𝘴 𝘣𝘰𝘶𝘵𝘰𝘯𝘴 𝘤𝘪-𝘥𝘦𝘴𝘴𝘰𝘶𝘴 👇</b>",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("•  𝗔𝗶𝗱𝗲  •", url="https://telegram.me/BTZF_CHAT")],
                [InlineKeyboardButton("• 𝗣𝗿𝗼𝗽𝗿𝗶𝗲́𝘁𝗮𝗶𝗿𝗲 •", url="https://telegram.me/ZeeXDevBot")]
            ])
        )

        text = (
            f"#NouveauGroupe\n\n"
            f"Groupe : {message.chat.title}\n"
            f"ID du groupe : `{message.chat.id}`\n"
            f"Ajouté par : {message.from_user.mention}\n"
            f"ID de l'utilisateur : `{message.from_user.id}`"
        )
        await bot.send_message(chat_id=LOG_CHANNEL, text=text)
        await sleep(120)
        await m.delete()