from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 

@Client.on_message(filters.group & filters.command("verify"))
async def _verify(bot, message):
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
    except:     
       return await bot.leave_chat(message.chat.id)  
    try:       
       user = await bot.get_users(user_id)
    except:
       return await message.reply(f"{user_name},\nDémarre-moi en message privé")
    if message.from_user.id != user_id:
       return await message.reply(f"Seul {user.mention} peut utiliser cette commande 😁")
    if verified==True:
       return await message.reply("Ce groupe est déjà vérifié !!")
    try:
       link = (await bot.get_chat(message.chat.id)).invite_link     
    except:
       return message.reply("Fais de moi un admin avec toutes les permissions")    
           
    text  = f"#NouvelleDemande\n\n"
    text += f"Utilisateur : {message.from_user.mention}\n"
    text += f"ID utilisateur : `{message.from_user.id}`\n"
    text += f"Groupe : [{message.chat.title}]({link})\n"
    text += f"ID groupe : `{message.chat.id}`\n"
   
    await bot.send_message(chat_id=LOG_CHANNEL,
                           text=text,
                           disable_web_page_preview=True,
                           reply_markup=InlineKeyboardMarkup(
                                                 [[InlineKeyboardButton("✅ Approuver", callback_data=f"verify_approve_{message.chat.id}"),
                                                   InlineKeyboardButton("❌ Refuser", callback_data=f"verify_decline_{message.chat.id}")]]))
    await message.reply("Demande de vérification envoyée ✅️\nNous vous notifierons lorsqu’elle sera approuvée.")



@Client.on_callback_query(filters.regex(r"^verify"))
async def verify_(bot, update):
    id = int(update.data.split("_")[-1])
    group = await get_group(id)
    name  = group["name"]
    user  = group["user_id"]
    if update.data.split("_")[1]=="approve":
       await update_group(id, {"verified":True})
       await bot.send_photo(
           chat_id=user,
           photo='https://telegra.ph/file/a706afc296de6da2a40c8.jpg',
           caption=f"<b>Votre demande de vérification pour {name} a été approuvée ✅</b>", 
           reply_markup=InlineKeyboardMarkup(
               [[InlineKeyboardButton("• Mises à jour •", url="https://t.me/ZeeXDev")]]
           )
       )
       await update.message.edit(update.message.text.html.replace("#NouvelleDemande", "#Approuvée"))
    else:
       await delete_group(id)
       await bot.send_message(chat_id=user, text=f"Votre demande de vérification pour {name} a été refusée 😐 Veuillez contacter un administrateur.")
       await update.message.edit(update.message.text.html.replace("#NouvelleDemande", "#Refusée"))