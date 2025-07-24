from info import *
from utils import *
from pyrogram import Client, filters 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.command("start") & ~filters.channel)
async def start(bot, message):
    await add_user(message.from_user.id, message.from_user.first_name)
    await message.reply(
        text=script.START.format(message.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('• 𝗖𝗵𝗮𝘁 𝗱𝗲 𝘀𝗼𝘂𝘁𝗶𝗲𝗻 •', url='https://t.me/codeflixsupport')],
            [InlineKeyboardButton("𝗔𝗶𝗱𝗲", url="http://telegram.me/BTZF_CHAT"),
             InlineKeyboardButton("𝗔 𝗽𝗿𝗼𝗽𝗼𝘀", callback_data="misc_help")],
            [InlineKeyboardButton('• 𝗖𝗵𝗮𝗶̂𝗻𝗲 𝗱𝗲 𝗺𝗶𝘀𝗲 𝗮̀ 𝗷𝗼𝘂𝗿 •', url='http://telegram.me/ZeeXDev')]
        ])
    )

@Client.on_message(filters.command("help"))
async def help(bot, message):
    await message.reply(
        text=script.HELP,
        disable_web_page_preview=True
    )

@Client.on_message(filters.command("about"))
async def about(bot, message):
    await message.reply(
        text=script.ABOUT.format((await bot.get_me()).mention),
        disable_web_page_preview=True
    )

@Client.on_message(filters.command("stats") & filters.user(ADMIN))
async def stats(bot, message):
    g_count, g_list = await get_groups()
    u_count, u_list = await get_users()
    await message.reply(script.STATS.format(u_count, g_count))

@Client.on_message(filters.command("id"))
async def id(bot, message):
    text = f"<b>➲  ID du chat :</b>  `{message.chat.id}`\n"
    if message.from_user:
        text += f"<b>➲  Ton ID :</b> `{message.from_user.id}`\n"
    if message.reply_to_message:
        if message.reply_to_message.from_user:
            text += f"<b>➲  ID de l'utilisateur répondu :</b> `{message.reply_to_message.from_user.id}`\n"
        if message.reply_to_message.forward_from:
            text += f"<b>➲  ID de l'utilisateur d'origine :</b> `{message.reply_to_message.forward_from.id}`\n"
        if message.reply_to_message.forward_from_chat:
            text += f"<b>➲  ID du chat d'origine :</b> `{message.reply_to_message.forward_from_chat.id}`\n"
    await message.reply(text)

@Client.on_callback_query(filters.regex(r"^misc"))
async def misc(bot, update):
    data = update.data.split("_")[-1]
    if data == "home":
        await update.message.edit(
            text=script.START.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('• 𝗖𝗵𝗮𝘁 𝗱𝗲 𝘀𝗼𝘂𝘁𝗶𝗲𝗻 •', url='https://telegram.me/codeflixsupport')],
                [InlineKeyboardButton("𝗔𝗶𝗱𝗲", url="http://telegram.me/BTZF_CHAT"),
                 InlineKeyboardButton("𝗔 𝗽𝗿𝗼𝗽𝗼𝘀", callback_data="misc_help")],
                [InlineKeyboardButton('• 𝗖𝗵𝗮𝗶̂𝗻𝗲 𝗱𝗲 𝗺𝗶𝘀𝗲 𝗮̀ 𝗷𝗼𝘂𝗿 •', url='http://telegram.me/ZeeXDev')]
            ])
        )
    elif data == "help":
        await update.message.edit(
            text=script.HELP,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton('📞 𝗖𝗼𝗻𝘁𝗮𝗰𝘁𝗲𝗿 𝗹𝗲 𝗽𝗿𝗼𝗽𝗿𝗶𝗲́𝘁𝗮𝗶𝗿𝗲', url='https://telegram.me/ZeeXDevBot')],
                [InlineKeyboardButton("⬅️ Retour", callback_data="misc_home"),
                 InlineKeyboardButton("Suivant ➡️", url="https://t.me/Godanimes")]
            ])
        )
    elif data == "about":
        await update.message.edit(
            text=script.ABOUT.format((await bot.get_me()).mention),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("⬅️ Retour", callback_data="misc_home")]
            ])
        )

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if content.startswith("/") or content.startswith("#"):
        return  # Ignorer les commandes ou hashtags
    await message.reply_text(
        text="<b>Salut 👋\n\nSi tu veux des films ou séries, clique sur le premier bouton.\n"
             "En cas de problème avec le bot, clique sur le deuxième bouton.</b>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📝  Faire une demande", url="https://telegram.me/Godanimes")],
            [InlineKeyboardButton("👤  Propriétaire du bot", url="https://telegram.me/ZeeXDevBot")]
        ]),
        disable_web_page_preview=True
    )
    await bot.send_message(
        chat_id=LOG_CHANNEL,
        text=f"<b>#MESSAGE\n\nNom : {user}\nID : {user_id}\n\nMessage : {content}</b>"
    )