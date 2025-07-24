from info import *
from utils import *
from pyrogram import Client, filters
from pyrogram.types import ChatPermissions

@Client.on_message(filters.group & filters.command("fsub"))
async def f_sub_cmd(bot, message):
    m=await message.reply("Veuillez patienter...")
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Seul {user_name} peut utiliser cette commande 😁")
    if bool(verified)==False:
       return await m.edit("Ce groupe n’est pas vérifié 🚫\nUtilisez /verify")
    try:
       f_sub = int(message.command[-1])
    except:
       return await m.edit("Format incorrect 🚫\nUtilisez `/fsub` ID_du_canal")      
    try:
       chat   = await bot.get_chat(f_sub)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link       
    except Exception as e:
       text = f"🚫  Erreur - `{str(e)}`\n\nAssurez-vous que je sois admin dans le canal et le groupe avec toutes les permissions"
       return await m.edit(text)
    await update_group(message.chat.id, {"f_sub":f_sub})
    await m.edit(f"Abonnement forcé correctement lié à [{chat.title}]({c_link}) !", disable_web_page_preview=True)
    text = f"#NewFsub\n\nUtilisateur : {message.from_user.mention}\nGroupe : [{group.title}]({g_link})\nCanal : [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("nofsub"))
async def nf_sub_cmd(bot, message):
    m=await message.reply("Détachement en cours...")
    try:
       group     = await get_group(message.chat.id)
       user_id   = group["user_id"] 
       user_name = group["user_name"]
       verified  = group["verified"]
       f_sub     = group["f_sub"]
    except :
       return await bot.leave_chat(message.chat.id)  
    if message.from_user.id!=user_id:
       return await m.edit(f"Seul {user_name} peut utiliser cette commande 😁")
    if bool(verified)==False:
       return await m.edit("Ce groupe n’est pas vérifié 🚫\nUtilisez /verify")
    if bool(f_sub)==False:
       return await m.edit("Ce groupe n’a aucun abonnement forcé\nUtilisez /fsub")        
    try:
       chat   = await bot.get_chat(f_sub)
       group  = await bot.get_chat(message.chat.id)
       c_link = chat.invite_link
       g_link = group.invite_link       
    except Exception as e:
       text = f"🚫  Erreur - `{str(e)}`\n\nAssurez-vous que je sois admin dans le canal et le groupe avec toutes les permissions"
       return await m.edit(text)
    await update_group(message.chat.id, {"f_sub":False})
    await m.edit(f"Abonnement forcé supprimé avec succès de [{chat.title}]({c_link})", disable_web_page_preview=True)
    text = f"#RemoveFsub\n\nUtilisateur : {message.from_user.mention}\nGroupe : [{group.title}]({g_link})\nCanal : [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_callback_query(filters.regex(r"^checksub"))
async def f_sub_callback(bot, update):
    user_id = int(update.data.split("_")[-1])
    group   = await get_group(update.message.chat.id)
    f_sub   = group["f_sub"]
    admin   = group["user_id"]

    if update.from_user.id!=user_id:
       return await update.answer("Ce message ne vous est pas destiné 😊", show_alert=True)
    try:
       await bot.get_chat_member(f_sub, user_id)          
    except UserNotParticipant:
       await update.answer("Veuillez d'abord rejoindre le canal de mise à jour, puis cliquez sur ce bouton", show_alert=True)
    except:       
       await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()
    else:
       await bot.restrict_chat_member(chat_id=update.message.chat.id, 
                                      user_id=user_id,
                                      permissions=ChatPermissions(can_send_messages=True,
                                                                  can_send_media_messages=True,
                                                                  can_send_other_messages=True))
       await update.message.delete()