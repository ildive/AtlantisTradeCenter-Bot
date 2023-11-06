import json
import os

import telebot

import funzioniManager
import markupManager
import schermateManager

from secrets import *

bot = telebot.TeleBot(token, parse_mode="HTML")
utentiDaPremiare = []

#lista dei file
def checkFiles():
    # Verifica se il file 'users.json' esiste, altrimenti lo crea
    try:
        with open('users.json', 'r') as file:
            global users
            users  = json.load(file)
    except FileNotFoundError:
        users = {}
    print("[" + str(__name__) + "] " + "Check files completato.")

def checkUserInList(chat_id, users_dict):
    return str(chat_id) in users_dict

def getPoint(chat_id):
    file_path = "users.json"
    with open(file_path, 'r') as file:
        fileJson = json.load(file)
    return fileJson.get(str(chat_id), {}).get("punti", 0)

def getWarn(chat_id):
    file_path = "users.json"
    with open(file_path, 'r') as file:
        fileJson = json.load(file)
    return fileJson.get(str(chat_id), {}).get("warn", 0)


def getInfoUser(chat_id):
    file_path = "users.json"
    with open(file_path, 'r') as file:
        fileJson = json.load(file)

    # Verifica se il chat_id è presente nel file JSON
    if str(chat_id) in fileJson:
        punti = fileJson[str(chat_id)].get("punti", 0)
        warn = fileJson[str(chat_id)].get("warn", 0)
        isBanned = fileJson[str(chat_id)].get("isBanned", 0)

        if isBanned:
            text = "🐬 ATC user 🐬\n\nPunti: " + str(punti) + "\nWarn: " + str(warn) + "\nBannato: si"
        else:
            text = "🐬 ATC user 🐬\n\nPunti: " + str(punti) + "\nWarn: " + str(warn) + "\nBannato: no"
    else:
        # Se il chat_id non è presente nel file JSON, gestisci il caso di default
        text = "L'utente non ha mai avviato il bot @AtlantisTradeCenterBot."

    return text

def load_user_data(file_path):
    try:
        with open(file_path, 'r') as file:
            user_data = json.load(file)
    except FileNotFoundError:
        user_data = {}
    return user_data

def warnUser(chat_id):
    file_path = "users.json"
    user_data = load_user_data(file_path)

    if str(chat_id) in user_data:
        user_data[str(chat_id)]["warn"] += 1
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        return True  # Restituisce True se l'utente è stato bannato con successo
    else:
        return False  # Restituisce False se l'utente non è stato trovato nel file JSON

def unwarnUser(chat_id):
    file_path = "users.json"
    user_data = load_user_data(file_path)

    if str(chat_id) in user_data:
        if getWarn(chat_id) > 0:
            user_data[str(chat_id)]["warn"] -= 1
            with open(file_path, 'w') as file:
                json.dump(user_data, file, indent=4)
            return True  # Restituisce True se l'utente è stato bannato con successo
        else:
            return "maxRaggiunto"
    else:
        return False  # Restituisce False se l'utente non è stato trovato nel file JSON

def ban_user(chat_id):
    file_path = "users.json"
    user_data = load_user_data(file_path)

    if str(chat_id) in user_data:
        user_data[str(chat_id)]["isBanned"] = True
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        #resetta i warn
        user_data[str(chat_id)]["warn"] = 0
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        return True  # Restituisce True se l'utente è stato bannato con successo
    else:
        return False  # Restituisce False se l'utente non è stato trovato nel file JSON

def unban_user(chat_id):
    file_path = "users.json"
    user_data = load_user_data(file_path)

    if str(chat_id) in user_data:
        user_data[str(chat_id)]["isBanned"] = False
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)
        return True  # Restituisce True se l'utente è stato sbannato con successo
    else:
        return False  # Restituisce False se l'utente non è stato trovato nel file JSON

def checkBannedStatus(chat_id):
    # Leggi il file JSON degli utenti
    file_path = "users.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        # Se il file non esiste, crea un dizionario vuoto
        users = {}

    # Verifica se l'utente è nel dizionario degli utenti
    if str(chat_id) in users:
        is_banned = users[str(chat_id)].get('isBanned', False)
        return is_banned
    else:
        # L'utente non è nel dizionario, quindi è considerato non bannato
        return False

def arrivoFoto(message, moduloVuoto):
    if schermateManager.canSendModulo(message.chat.id):
        #ottieni il file della foto
        file_id = message.photo[-1].file_id
        #ottieni l'URL diretto del file dalla Telegram API
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{bot.token}/{file_info.file_path}'

        if moduloVuoto[message.chat.id].photo is None:
            with open('temp.jpg', 'wb') as photo:
                response = bot.download_file(file_info.file_path)
                photo.write(response)
                photo.close()

            with open('temp.jpg', 'rb') as photo:
                nuovoMessaggioConFoto = bot.send_photo(chat_id=message.chat.id, photo=photo, caption=moduloVuoto[message.chat.id].text, reply_markup=markupManager.inviaModuloAlloStaff())
                photo.close()
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            bot.delete_message(message.chat.id, moduloVuoto[message.chat.id].id)
            moduloVuoto[message.chat.id] = nuovoMessaggioConFoto
        else:
            bot.delete_message(message.chat.id, message.id)
            bot.send_message(message.chat.id, "Puoi inserire una sola foto per modulo. Se vuoi cambiarla <b>chiudi questo modulo</b> e aprine un'altro", reply_markup=markupManager.capitoMarkup())
    else:
        bot.delete_message(message.chat.id, message.id)
        schermateManager.showHome(message.chat.id)

#inizio funzioni manage Modulo per lo staff (inline keyboard sul gruppo)
def setNewOfferta(moduloID, newOfferta):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Aggiorna il parametro 'creatoreModulo' con il nuovo creatore
            data["ultima_offerta"] = newOfferta

        with open(f"messaggiPostatiCanale/{moduloID}.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True
    except FileNotFoundError:
        return False

def setNewOfferente(moduloID, newOfferente):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Aggiorna il parametro 'creatoreModulo' con il nuovo creatore
            data["ultimo_offerente"] = newOfferente

        with open(f"messaggiPostatiCanale/{moduloID}.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True
    except FileNotFoundError:
        return False

def setNewMessageID(moduloID, newMessageID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Aggiorna il parametro 'creatoreModulo' con il nuovo creatore
            data["message_id"] = newMessageID

        with open(f"messaggiPostatiCanale/{moduloID}.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True
    except FileNotFoundError:
        return False

def setNewText(moduloID, nexText):
    tipoModulo = None
    markup = None

    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Aggiorna il parametro 'creatoreModulo' con il nuovo creatore
            data["text"] = nexText

        with open(f"messaggiPostatiCanale/{moduloID}.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        try:
            #prende il tipo di modulo
            try:
                tipoModulo = str(nexText).split("🐬")[1].strip().split(" ")[0].lower()
            except:
                tipoModulo = None

            if funzioniManager.getOfferta(moduloID) is not None:
                markup = markupManager.setOffertaMarkup(funzioniManager.getOfferta(moduloID), moduloID, False)
            else:
                if tipoModulo == "asta":
                    markup = markupManager.offriCustomStartUrlAsta(moduloID)
                elif tipoModulo == "cercasi":
                    markup = markupManager.offriCustomStartUrlCercasi(moduloID)
            if tipoModulo is not None:
                try:
                    bot.edit_message_text(chat_id=canaleAste, message_id=funzioniManager.getMessageID(moduloID), text=nexText, reply_markup=markup)
                except:
                    bot.edit_message_caption(chat_id=canaleAste, message_id=funzioniManager.getMessageID(moduloID), caption=nexText, reply_markup=markup)
                return True
        except Exception:
            return False
    except FileNotFoundError:
        return False

#modulo
def salvaModulo(text, ultima_offerta, chat_id_ultimoOfferente, message_id, photoBool, isTerminata, mittenteModulo, stafferModulo):
    if not os.path.exists("messaggiPostatiCanale/" + str(funzioniManager.messageTextToModuloID(text)) + ".txt"):
        #se il file non esiste, quindi da creare
        # Crea un dizionario con la struttura desiderata
        data = {
            "text": text,
            "ultima_offerta": ultima_offerta,
            "ultimo_offerente": chat_id_ultimoOfferente,
            "message_id": message_id,
            "photo": photoBool,
            "isTerminata": isTerminata,
            "creatoreModulo": mittenteModulo,
            "stafferModulo": stafferModulo
        }
        # Scrivi il dizionario in un file JSON
        with open("messaggiPostatiCanale/" + str(funzioniManager.messageTextToModuloID(text)) + ".txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
            file.close()
    else:
        #Il file esiste, è da modificare
        with open(f"messaggiPostatiCanale/{funzioniManager.messageTextToModuloID(text)}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            # uso if perchè non si deve interrompere e deve verificare tutte le condizioni
            if data["text"] is not None:
                data["text"] = text
            if data["ultima_offerta"] is not None:
                data["ultima_offerta"] = ultima_offerta
            if data["ultimo_offerente"] is not None:
                data["ultimo_offerente"] = chat_id_ultimoOfferente
            if data["message_id"] is not None:
                data["message_id"] = message_id
            if data["photo"] is not None:
                data["photo"] = photoBool
            if data["creatoreModulo"] is not None:
                data["creatoreModulo"] = mittenteModulo
            if data["stafferModulo"] is not None:
                data["stafferModulo"] = stafferModulo
        with open(f"messaggiPostatiCanale/{funzioniManager.messageTextToModuloID(text)}.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

def offertaInPunti(moduloID):
    offerta = funzioniManager.abbrev_to_number(funzioniManager.getOfferta(moduloID))
    try:
        if offerta is not None and offerta != "":
            punti = int(offerta) // 5000
            return punti
        else:
            return False
    except:
        return False


def assegnaPuntiCompratoreVenditore(moduloID, puntiDalloStaff):
    creatore = funzioniManager.getCreatoreModulo(moduloID)
    offerente = funzioniManager.getOfferente(moduloID)

    file_path = "users.json"
    user_data = load_user_data(file_path)
    if puntiDalloStaff is None:
        #Potremmo dire che è la prima volta che viene eseguita questa funzione e il bot proverà ad assegnare automaticamente i punti
        if str(creatore) in user_data and str(offerente) in user_data:
            punti = offertaInPunti(moduloID)
            if punti is not False:
                user_data[str(creatore)]["punti"] += punti
                user_data[str(offerente)]["punti"] += punti
                with open(file_path, 'w') as file:
                    json.dump(user_data, file, indent=4)
                return True  # Restituisce True se l'utente è stato bannato con successo
            else:
                #TODO continua qui, manda un messaggio ai delegati inserendo manualmente a quanti punti equivale quella cifra
                bot.send_message(groupStafferChat_id, f"🏆  Punti 🏆\n\nHo avuto dei problemi nell'assegnare dei punti per venditore e compratore del modulo #{moduloID}\n\nUltima offerta: {funzioniManager.getOfferta(moduloID)}\n\nA quanto equivalgono in punti questa offerta? rispondi a questo messaggio con la risposta.\nRicorda che ogni 5k si da un punto.\n\nEsempio 10k = 2 punti\nEsempio 15k = 3 punti\nEsempio 17k = 3 punti")
        else:
            if not str(creatore) in user_data:
                creatoreUrl = f"tg://user?id={creatore}"
                bot.send_message(1654713548, f"l'utente ID: {creatore} non ha avviato il bot. Contattalo qui sotto in modo che possa assegnargli i punti", reply_markup=markupManager.showUser(creatoreUrl))
            if not str(offerente) in user_data:
                offerenteUrl = f"tg://user?id={offerente}"
                bot.send_message(1654713548, f"l'utente ID: {offerente} non ha avviato il bot. Contattalo qui sotto in modo che possa assegnargli i punti",reply_markup=markupManager.showUser(offerenteUrl))
            return False  # Restituisce False se l'utente non è stato trovato nel file JSON
    else:
        user_data[str(creatore)]["punti"] += puntiDalloStaff
        user_data[str(offerente)]["punti"] += puntiDalloStaff
        with open(file_path, 'w') as file:
            json.dump(user_data, file, indent=4)



