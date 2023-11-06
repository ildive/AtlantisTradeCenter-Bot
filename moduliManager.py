import os
import random

import re
import requests
import telebot

import fileManager
import funzioniManager
import markupManager
import markupManager as mrkp

from secrets import *

bot = telebot.TeleBot(token)

moduloAsta1 = "🐬 Asta @AtlantisTradeCenter 🐬\nModulo #"
moduloAsta2 = "\n\n📦 Oggetto: \n\n📄 Descrizione: \n\n🪙 Base asta: \n\n💵 Rilancio: \n\n🏦 Compra ora: \n\n🗡 Legalità: \n"

moduloCercasi1 = "🐬 Cercasi @AtlantisTradeCenter 🐬\nModulo #"
moduloCercasi2 = "\n\n📦 Oggetto: \n\n🪙 Offerti: "

def asta():
    codice = ''.join(random.choice("ABCDEFGHIKLMNOPQRSTUVXYZ0123456789") for _ in range(5))
    modulo = str(moduloAsta1 + random.choice("ABCDEFGHIKLMNOPQRSTUVXYZ") + str(codice) + moduloAsta2)
    return modulo

def cercasi():
    codice = ''.join(random.choice("ABCDEFGHIKLMNOPQRSTUVXYZ0123456789") for _ in range(5))
    modulo = str(moduloCercasi1 + random.choice("ABCDEFGHIKLMNOPQRSTUVXYZ") + str(codice) + moduloCercasi2)
    return modulo

def controllaSpazi(text, parametroDaControllare):
    #aggiungo un \n a 'text' perchè va per ogni parametro, il programma va a cercare quando va a capo per capire quando passare al prossimo parametro.
    text = str(text) + str("\n")
    linee = text.splitlines()
    new_text = False
    parametro_start = text.find(str(parametroDaControllare))
    if parametro_start != -1:
        # Trova l'indice della prima occorrenza di "\n" dopo l'etichetta "📄 Descrizione:" (cambiato da "oggetto_end" a "parametro_end")
        parametro_end = text.find("\n", parametro_start)
        if parametro_end != -1:
            # Estrai il testo compreso tra "📄 Descrizione:" e il primo "\n" successivo
            parametro_text = text[parametro_start:parametro_end]
            # Dividi il testo in base al carattere ":"
            parametro_parts = parametro_text.split(":")
            if len(parametro_parts) > 1:
                # Estrai il valore della descrizione eliminando eventuali spazi iniziali e finali
                parametro_value = parametro_parts[1]
                # Conta quanti spazi ci sono nel valore della descrizione
                num_spaces = parametro_value.count(" ")
                # Sostituisci il testo originale con "📄 Descrizione: valore_descrizione"
                if not parametro_parts[1].startswith(" ") or num_spaces != 1:
                    # Se non inizia per spazio o gli spazi non sono 1, aggiungi uno spazio e aggiorna il testo
                    new_text = f"{parametroDaControllare} {parametro_value.strip()}"
                else:
                    for linea in linee:
                        if str(parametroDaControllare) in linea:
                            new_text = linea
    return new_text

def componiModulo(call):
    parametriAsta = ["📦 Oggetto:", "📄 Descrizione:", "🪙 Base asta:", "💵 Rilancio:", "🏦 Compra ora:", "🗡 Legalità:"]
    parametriCercasi = ["📦 Oggetto:", "🪙 Offerti:"]
    moduloQuasiCompleto = ""
    moduloCompleto = ""
    try:
        tipoModulo = call.message.text.split("🐬")[1].strip().split(" ")[0].lower()
        text = call.message.text
    except:
        tipoModulo = call.message.caption.split("🐬")[1].strip().split(" ")[0].lower()
        text = call.message.caption

    if tipoModulo == "asta":
        for parametro in parametriAsta:
            moduloQuasiCompleto += str("\n\n") + str(controllaSpazi(text, parametro))
        moduloCompleto = str(text.splitlines()[0]) + "\n" + str(text.splitlines()[1]) + str(moduloQuasiCompleto) + str("\n\nPer offrire clicca qui sotto 👇")

    elif tipoModulo == "cercasi":
        for parametro in parametriCercasi:
            moduloQuasiCompleto += str("\n\n") + str(controllaSpazi(text, parametro))
        moduloCompleto = str(text.splitlines()[0]) + "\n" + str(text.splitlines()[1]) + str(moduloQuasiCompleto) + str("\n\nSe hai l'oggetto clicca qui sotto 👇")
    else:
        bot.answer_callback_query(call.id, "⚠️ Attenzione ⚠️\n\nModifica il tipo di modulo in alto (asta o cercasi) e controlla che si presenti così:\n\n🐬 Asta\no\n🐬 Cercasi\n\n(con uno spazio solo tra l'emoji e il testo)", show_alert=True)

    return moduloCompleto


def inviaModulo(call):
    messaggioAttesa = bot.send_message(call.message.chat.id, "⏳")
    if call.message.photo:
        #se messaggio contiene una foto
        photo = call.message.photo[-1]
        #ottiene l'URL diretto dell'immagine
        file_info = bot.get_file(photo.file_id)
        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        #la scarica
        response = requests.get(photo_url)
        photo_data = response.content
        bot.send_photo(chat_id=groupModuliChat_id, photo=photo_data, caption=call.message.caption, reply_markup=mrkp.tastiEsitoModulo(call.message.chat.id))
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=call.message.caption, reply_markup=mrkp.moduloInviatoMarkup())
    else:
        bot.send_message(chat_id=groupModuliChat_id, text=call.message.text, reply_markup=mrkp.tastiEsitoModulo(call.message.chat.id))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=call.message.text, reply_markup=mrkp.moduloInviatoMarkup())


    #controllo moduliDaCancellare (messageX.from_user.chat.id == call.message.chat.id: bot.delete_message(messageX.id)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=messaggioAttesa.id, text="Il tuo modulo è in fase di valutazione!", reply_markup=mrkp.tastoBackToHome())


def postaModulo(call, moduloCompleto, editBool):
    userUrl = call.message.reply_markup.keyboard[0][0].url
    userChat_id = userUrl.split("=")[1]
    stafferModulo = call.from_user

    if call.message.photo is not None:
        tipoModulo = call.message.caption.split("🐬")[1].strip().split(" ")[0].lower()
        photoBool = True
        #se messaggio contiene una foto
        photo = call.message.photo[-1]
        #ottiene l'URL diretto dell'immagine
        file_info = bot.get_file(photo.file_id)
        photo_url = f"https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}"
        #la scarica
        response = requests.get(photo_url)
        photo_data = response.content

        if tipoModulo == "cercasi":
            if moduloCompleto == "" or str(moduloCompleto).__contains__("False"):
                post = bot.send_photo(canaleAste, photo=photo_data, caption=call.message.caption, reply_markup=mrkp.offriCustomStartUrlCercasi(funzioniManager.messageTextToModuloID(call.message.caption)))
            else:
                #il moduloCompleto è venuto bene
                post = bot.send_photo(canaleAste, photo=photo_data, caption=moduloCompleto, reply_markup=mrkp.offriCustomStartUrlCercasi(funzioniManager.messageTextToModuloID(call.message.caption)))
        elif tipoModulo == "asta":
            if moduloCompleto == "" or str(moduloCompleto).__contains__("False"):
                post = bot.send_photo(canaleAste, photo=photo_data, caption=call.message.caption, reply_markup=mrkp.offriCustomStartUrlAsta(funzioniManager.messageTextToModuloID(call.message.caption)))
            else:
                post = bot.send_photo(canaleAste, photo=photo_data, caption=moduloCompleto, reply_markup=mrkp.offriCustomStartUrlAsta(funzioniManager.messageTextToModuloID(call.message.caption)))
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=call.message.caption + "\n\nApprovata da: " + str(stafferModulo.first_name), reply_markup=mrkp.showUser(userUrl))
        if moduloCompleto == "":
            testoPost = post.caption
        else:
            testoPost = moduloCompleto
    else:
        tipoModulo = call.message.text.split("🐬")[1].strip().split(" ")[0].lower()
        photoBool = False
        if tipoModulo == "cercasi":
            if moduloCompleto == "" or str(moduloCompleto).__contains__("False"):
                post = bot.send_message(canaleAste, text=str(call.message.text) + str("\n\nSe hai l'oggetto clicca qui sotto 👇"), reply_markup=mrkp.offriCustomStartUrlCercasi(funzioniManager.messageTextToModuloID(call.message.text)))
            else:
                #il moduloCompleto è venuto bene
                post = bot.send_message(canaleAste, text=moduloCompleto, reply_markup=mrkp.offriCustomStartUrlCercasi(funzioniManager.messageTextToModuloID(call.message.text)))
        elif tipoModulo == "asta":
            if moduloCompleto == "" or str(moduloCompleto).__contains__("False"):
                post = bot.send_message(canaleAste, text=str(call.message.text) + str("\n\nPer offrire clicca qui sotto 👇"), reply_markup=mrkp.offriCustomStartUrlAsta(funzioniManager.messageTextToModuloID(call.message.text)))
            else:
                post = bot.send_message(canaleAste, text=moduloCompleto, reply_markup=mrkp.offriCustomStartUrlAsta(funzioniManager.messageTextToModuloID(call.message.text)))
        #if moduloCompleto == "":
        #    post = bot.send_message(canaleAste, text=call.message.text, reply_markup=mrkp.offriCustomStartUrlAsta(funzioniManager.messageTextToModuloID(call.message.text)))
        #else:
        #    post = bot.send_message(canaleAste, text=moduloCompleto, reply_markup=mrkp.offriCustomStartUrlAsta(funzioniManager.messageTextToModuloID(call.message.text)))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=call.message.text + "\n\nApprovata da: " + str(stafferModulo.first_name), reply_markup=mrkp.showUser(userUrl))
        if moduloCompleto == "":
            testoPost = post.text
        else:
            testoPost = moduloCompleto
    #bot invia messaggio "la tua asta è stata postata, guardala cliccando qui..."
    if editBool:
        bot.send_message(userChat_id, "Il tuo modulo è stato modificato e postato sul canale, premi il tasto qui sotto per vedere il messaggio 👇👇👇", reply_markup=mrkp.redirectPostCanale(post.message_id))
    else:
        bot.send_message(userChat_id, "Il tuo modulo è stato approvato e postato sul canale, premi il tasto qui sotto per vedere il messaggio 👇👇👇", reply_markup=mrkp.redirectPostCanale(post.message_id))
    fileManager.salvaModulo(testoPost, None, None, post.message_id, photoBool, False, userChat_id, stafferModulo.id)

def moficaModuloOfferta(moduloID, offerta):
    postMessageID = funzioniManager.getMessageID(moduloID)
    if offerta is None:
        bot.edit_message_reply_markup(chat_id=canaleAste, message_id=postMessageID, reply_markup=markupManager.offriCustomStartUrlAsta(moduloID))
    else:
        bot.edit_message_reply_markup(chat_id=canaleAste, message_id=postMessageID, reply_markup=markupManager.setOffertaMarkup(offerta, moduloID, True))

def avvisaTermineAsta(moduloID, file_path):
    bot.send_message(groupStafferChat_id, f"⏳ L'asta #{moduloID} è scaduta 💸\n\nControlla che non ci siano ulteriori offerte nel bot assistenza e premi il tasto qui sotto per confermare il termine dell'asta.", reply_markup=markupManager.confermaTerminaAsta(moduloID))
    if os.path.exists(file_path):
        os.remove(file_path)
