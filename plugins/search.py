import asyncio
from info import *
from utils import *
from time import time 
from client import User
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.text & filters.group & filters.incoming & ~filters.command(["verify", "connect", "id"]))
async def search(bot, message):
    f_sub = await force_sub(bot, message)
    if f_sub == False:
        return     
    channels = (await get_group(message.chat.id))["channels"]
    if bool(channels) == False:
        return     
    if message.text.startswith("/"):
        return    
    query = message.text 
    head = "<b>⇩  𝘝𝘰𝘪𝘤𝘪 𝘷𝘰𝘴 𝘳𝘦́s𝘶𝘭𝘵𝘢𝘵𝘴  ⇩</b>\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0]
                if name in results:
                    continue 
                results += f"<b>🎬 {name}\n {msg.link} </b>\n\n"                                                      
        if bool(results) == False:
            movies = await search_imdb(query)
            buttons = []
            for movie in movies: 
                buttons.append([InlineKeyboardButton(movie['title'], callback_data=f"recheck_{movie['id']}")])
            msg = await message.reply("𝗝𝗲 𝗻'𝗮𝗶 𝗿𝗶𝗲𝗻 𝘁𝗿𝗼𝘂𝘃𝗲́ 𝗰𝗼𝗿𝗿𝗲𝘀𝗽𝗼𝗻𝗱𝗮𝗻𝘁.\n𝗩𝗼𝘂𝗹𝗶𝗲𝘇-𝘃𝗼𝘂𝘀 𝗱𝗶𝗿𝗲 𝘂𝗻 𝗱𝗲 𝗰𝗲𝘂𝘅-𝗹𝗮 ?", 
                                          reply_markup=InlineKeyboardMarkup(buttons))
        else:
            msg = await message.reply_text(text=head + results, disable_web_page_preview=True)
        _time = (int(time()) + (15 * 60))
        await save_dlt_message(msg, _time)
    except:
        pass

@Client.on_callback_query(filters.regex(r"^recheck"))
async def recheck(bot, update):
    clicked = update.from_user.id
    try:      
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete(2)       
    if clicked != typed:
        return await update.answer("𝘊𝘦 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘯'𝘦𝘴𝘵 𝘱𝘢𝘴 𝘱𝘰𝘶𝘳 𝘵𝘰𝘪", show_alert=True)

    m = await update.message.edit("<b>🔎 𝘙𝘦𝘤𝘩𝘦𝘳𝘤𝘩𝘦 𝘦𝘯 𝘤𝘰𝘶𝘳𝘴, 𝘱𝘢𝘵𝘪𝘦𝘯𝘵𝘦𝘻 ♻️</b>")
    id = update.data.split("_")[-1]
    query = await search_imdb(id)
    channels = (await get_group(update.message.chat.id))["channels"]
    head = "<b>𝘑'𝘢𝘪 𝘳𝘦𝘤𝘩𝘦𝘳𝘤𝘩𝘦́ 𝘭𝘦 𝘧𝘪𝘭𝘮 𝘢𝘷𝘦𝘤 𝘵𝘢 𝘮𝘢𝘶𝘷𝘢𝘪𝘴𝘦 𝘰𝘳𝘵𝘩𝘰𝘨𝘳𝘢𝘱𝘩𝘦...\n𝘔𝘢𝘪𝘴 𝘧𝘢𝘪𝘴 𝘢𝘵𝘵𝘦𝘯𝘵𝘪𝘰𝘯 𝘭𝘢 𝘱𝘳𝘰𝘤𝘩𝘢𝘪𝘯𝘦 𝘧𝘰𝘪𝘴 😋</b>\n\n"
    results = ""
    try:
        for channel in channels:
            async for msg in User.search_messages(chat_id=channel, query=query):
                name = (msg.text or msg.caption).split("\n")[0]
                if name in results:
                    continue 
                results += f"<b>🎬 {name}\n {msg.link} </b>\n\n"
        if bool(results) == False:          
            return await update.message.edit(
                "<b>⚠️ 𝘈𝘶𝘤𝘶𝘯 𝘳𝘦́s𝘶𝘭𝘵𝘢𝘵 𝘵𝘳𝘰𝘶𝘷𝘦́ !!\n𝘝𝘦𝘶𝘪𝘭𝘭𝘦𝘻 𝘦𝘯 𝘧𝘢𝘪𝘳𝘦 𝘭𝘢 𝘥𝘦𝘮𝘢𝘯𝘥𝘦 𝘢̀ 𝘭'𝘢𝘥𝘮𝘪𝘯 👇🏻</b>",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("•  Demander à l'admin  •", callback_data=f"request_{id}")]]
                )
            )
        await update.message.edit(text=head + results, disable_web_page_preview=True)
    except Exception as e:
        await update.message.edit(f"Erreur - `{e}`")

@Client.on_callback_query(filters.regex(r"^request"))
async def request(bot, update):
    clicked = update.from_user.id
    try:      
        typed = update.message.reply_to_message.from_user.id
    except:
        return await update.message.delete()       
    if clicked != typed:
        return await update.answer("𝘊𝘦 𝘮𝘦𝘴𝘴𝘢𝘨𝘦 𝘯'𝘦𝘴𝘵 𝘱𝘢𝘴 𝘱𝘰𝘶𝘳 𝘵𝘰𝘪", show_alert=True)

    admin = (await get_group(update.message.chat.id))["user_id"]
    id = update.data.split("_")[1]
    name = await search_imdb(id)
    url = "https://www.imdb.com/title/tt" + id
    text = f"#Demande\n\nNom : {name}\nIMDb : {url}"
    await bot.send_message(chat_id=admin, text=text, disable_web_page_preview=True)
    await update.answer("Demande envoyée à l’admin ✅", show_alert=True)
    await update.message.delete(60)