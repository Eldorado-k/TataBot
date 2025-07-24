from info import *
from utils import *
from client import User 
from pyrogram import Client, filters

@Client.on_message(filters.group & filters.command("connect"))
async def connect(bot, message):
    m = await message.reply("<b>Connexion en cours...</b>")
    user = await User.get_me()
    try:
        group = await get_group(message.chat.id)
        user_id = group["user_id"] 
        user_name = group["user_name"]
        verified = group["verified"]
        channels = group["channels"].copy()
    except:
        return await bot.leave_chat(message.chat.id)
    
    if message.from_user.id != user_id:
        return await m.edit(f"Seul {user_name} peut utiliser cette commande 😁")
    
    if not bool(verified):
        return await m.edit("Ce groupe n'est pas vérifié 🚫\nUtilise /verify")

    try:
        channel = int(message.command[-1])
        if channel in channels:
            return await message.reply("Ce canal est déjà connecté.")
        channels.append(channel)
    except:
        return await m.edit("Format incorrect 🚫\nUtilise `/connect` ID_du_canal")

    try:
        chat = await bot.get_chat(channel)
        group = await bot.get_chat(message.chat.id)
        c_link = chat.invite_link
        g_link = group.invite_link
        await User.join_chat(c_link)
    except Exception as e:
        if "The user is already a participant" in str(e):
            pass
        else:
            text = f"🚫 Erreur - `{str(e)}`\nAssure-toi que je suis administrateur du canal et du groupe, avec toutes les autorisations, et que {(user.username or user.mention)} n'est pas banni."
            return await m.edit(text)

    await update_group(message.chat.id, {"channels": channels})
    await m.edit(f"Connecté avec succès à\n[{chat.title}]({c_link})", disable_web_page_preview=True)
    text = f"#NouvelleConnexion\n\nUtilisateur : {message.from_user.mention}\nGroupe : [{group.title}]({g_link})\nCanal : [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("disconnect"))
async def disconnect(bot, message):
    m = await message.reply("<b>Veuillez patienter...</b>")
    try:
        group = await get_group(message.chat.id)
        user_id = group["user_id"] 
        user_name = group["user_name"]
        verified = group["verified"]
        channels = group["channels"].copy()
    except:
        return await bot.leave_chat(message.chat.id)

    if message.from_user.id != user_id:
        return await m.edit(f"Seul {user_name} peut utiliser cette commande 😁")
    
    if not bool(verified):
        return await m.edit("Ce groupe n'est pas vérifié 🚫\nUtilise /verify")

    try:
        channel = int(message.command[-1])
        if channel not in channels:
            return await m.edit("Tu n'as pas encore ajouté ce canal.")
        channels.remove(channel)
    except:
        return await m.edit("Format incorrect 🚫\nUtilise `/disconnect` ID_du_canal")

    try:
        chat = await bot.get_chat(channel)
        group = await bot.get_chat(message.chat.id)
        c_link = chat.invite_link
        g_link = group.invite_link
        await User.leave_chat(channel)
    except Exception as e:
        text = f"🚫 Erreur - `{str(e)}`\nAssure-toi que je suis administrateur du canal et du groupe avec toutes les autorisations, et que {(user.username or user.mention)} n'est pas banni."
        return await m.edit(text)

    await update_group(message.chat.id, {"channels": channels})
    await m.edit(f"Déconnecté avec succès de [{chat.title}]({c_link})", disable_web_page_preview=True)
    text = f"#Déconnexion\n\nUtilisateur : {message.from_user.mention}\nGroupe : [{group.title}]({g_link})\nCanal : [{chat.title}]({c_link})"
    await bot.send_message(chat_id=LOG_CHANNEL, text=text)


@Client.on_message(filters.group & filters.command("connections"))
async def connections(bot, message):
    group = await get_group(message.chat.id)
    user_id = group["user_id"]
    user_name = group["user_name"]
    channels = group["channels"]
    f_sub = group["f_sub"]

    if message.from_user.id != user_id:
        return await message.reply(f"Seul {user_name} peut utiliser cette commande 😁")

    if not bool(channels):
        return await message.reply("Ce groupe n'est actuellement connecté à aucun canal.\nConnecte-en un avec /connect")

    text = "Ce groupe est connecté aux canaux suivants :\n\n"
    for channel in channels:
        try:
            chat = await bot.get_chat(channel)
            name = chat.title
            link = chat.invite_link
            text += f"• [{name}]({link})\n"
        except Exception as e:
            await message.reply(f"🚫 Erreur pour le canal `{channel}` :\n`{e}`")

    if bool(f_sub):
        try:
            f_chat = await bot.get_chat(f_sub)
            f_title = f_chat.title
            f_link = f_chat.invite_link
            text += f"\n🔒 Abonnement forcé : [{f_title}]({f_link})"
        except Exception as e:
            await message.reply(f"❌ Erreur dans le canal d'abonnement forcé (`{f_sub}`)\n`{e}`")

    await message.reply(text=text, disable_web_page_preview=True)