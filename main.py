import datetime
import json
import os
import traceback

import requests
import telebot
from telebot import custom_filters

import erroriManager
import fileManager
import funzioniManager
import moduliManager
import markupManager
import offerteManager
import recensioniManager
import schermateManager
import sponsorManager
import taskManager
import testiManager
from commands import commandStartManager

from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler()
bot = telebot.TeleBot("<TOKEN>", parse_mode="HTML")
groupModuliChat_id = "-1001974658159"
groupStafferChat_id = "-1001933687315"
canaleAste = "@AtlantisTradeCenter"
devCID = "1654713548"
maxWarnBeforeBan = 2

listaFile = "files.txt"

moduloVuoto = {}

# Funzione per verificare l'esistenza dei file
def checkFiles(file_list):
    for file in file_list:
        if not os.path.exists(file):
            open(file, "x")
            print("File " + file + " creato.")


# Verifica l'esistenza del file di lista e crea i file se necessario
if os.path.exists(listaFile):
    file_list = [line.rstrip() for line in open(listaFile)]
    checkFiles(file_list)
else:
    with open(listaFile, "w", encoding='utf-8') as lista_file:
        lista_file.write("admins.txt\nusers.json")
    file_list = ["admins.txt", "users.json"]
    checkFiles(file_list)

adminr = [line.rstrip() for line in open('admins.txt')]

@bot.message_handler(commands=['ban'])
def banCommand(message):
    if message.reply_to_message is not None and message.reply_to_message.forward_from is not None and str(message.chat.id) == str(groupStafferChat_id):
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']:
            userDaBannare = message.reply_to_message.forward_from.id
            if fileManager.ban_user(userDaBannare):
                # tutto questo di sotto si esegue solo se è stato bannato e ritorna True se è stato bannato con successo
                bot.send_message(message.chat.id, "ID: " + str(userDaBannare) + " bannato con successo")
                try:
                    bot.send_message(userDaBannare, "🚷 Sei stato bannato dal bot 🚷\n\nPer lo sban contattaci qui sotto", reply_markup=markupManager.assistenzaMarkupSenzaHome())
                except:
                    pass
            else:
                bot.send_message(message.chat.id, "L'utente ID: " + str(userDaBannare) + " non è registrato al bot.")
            bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=['unban', 'sban'])
def unbanCommand(message):
    if message.reply_to_message is not None and message.reply_to_message.forward_from is not None and str(message.chat.id) == str(groupStafferChat_id):
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']:
            userDaSbannare = message.reply_to_message.forward_from.id
            if fileManager.unban_user(userDaSbannare):
                #tutto questo di sotto si esegue solo se è stato bannato e ritorna True se è stato bannato con successo
                bot.send_message(message.chat.id, "ID: " + str(userDaSbannare) + " sbannato con successo")
                try:
                    bot.send_message(userDaSbannare, "🚷 Sei stato sbannato dal bot 🚷\n\nOra puoi usare tutti i servizi dell'Atlantis Trade Center.", reply_markup=markupManager.tastoBackToHome())
                except:
                    pass
            else:
                bot.send_message(message.chat.id, "L'utente ID: " + str(userDaSbannare) + " non è registrato al bot.")
            bot.delete_message(message.chat.id, message.id)


@bot.message_handler(commands=['warn'])
def warnCommand(message):
    if message.reply_to_message is not None and message.reply_to_message.forward_from is not None and str(message.chat.id) == str(groupStafferChat_id):
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']:
            userDaWarnare = message.reply_to_message.forward_from.id
            if fileManager.warnUser(userDaWarnare):
                # tutto questo di sotto si esegue solo se è stato bannato e ritorna True se è stato bannato con successo
                bot.send_message(message.chat.id, "ID: " + str(userDaWarnare) + " warnato con successo")
                warn = fileManager.getWarn(userDaWarnare)
                if warn >= maxWarnBeforeBan:
                    bot.send_message(groupStafferChat_id, "L'user ID: " + str(userDaWarnare) + " ha " + str(warn) + " warn. Clicca il tasto qui sotto per bannarlo", reply_markup=markupManager.banUtente(userDaWarnare))
                try:
                    bot.send_message(userDaWarnare, "Hai ricevuto un warn, fai attenzione perchè a " + str(maxWarnBeforeBan) + " warn, verrai bannato!\n\nI tuoi warn: " + str(warn), reply_markup=markupManager.capitoMarkup())
                except:
                    pass
            else:
                bot.send_message(message.chat.id, "L'utente ID: " + str(userDaWarnare) + " non è registrato al bot.")
            bot.delete_message(message.chat.id, message.id)

@bot.message_handler(commands=['unwarn', 'diswarn'])
def unwarnCommand(message):
    if message.reply_to_message is not None and message.reply_to_message.forward_from is not None and str(message.chat.id) == str(groupStafferChat_id):
        if bot.get_chat_member(message.chat.id, message.from_user.id).status in ['administrator', 'creator']:
            userDaUnwarnare = message.reply_to_message.forward_from.id
            if fileManager.unwarnUser(userDaUnwarnare) == "maxRaggiunto":
                #l'utente ha già 0 warn
                bot.send_message(groupStafferChat_id, "L'utente ID: " + str(userDaUnwarnare) + " ha già 0 warn")
            elif fileManager.unwarnUser(userDaUnwarnare):
                bot.send_message(message.chat.id, "ID: " + str(userDaUnwarnare) + " unwarnato con successo")
                warn = fileManager.getWarn(userDaUnwarnare)
                try:
                    bot.send_message(userDaUnwarnare, "Ti è stato rimosso un warn!\n\nI tuoi warn: " + str(warn), reply_markup=markupManager.capitoMarkup())
                except:
                    pass
            else:
                bot.send_message(message.chat.id, "L'utente ID: " + str(userDaUnwarnare) + " non è registrato al bot.")
            bot.delete_message(message.chat.id, message.id)



@bot.callback_query_handler(func=lambda call: call.data.startswith("banUser#"))
def banUserMarkup(call):
    if bot.get_chat_member(call.message.chat.id, call.from_user.id).status in ['administrator', 'creator']:
        userDaBannare = call.data.split("#")[1]
        if fileManager.ban_user(userDaBannare):
            # tutto questo di sotto si esegue solo se è stato bannato e ritorna True se è stato bannato con successo
            bot.send_message(call.message.chat.id, "ID: " + str(userDaBannare) + " bannato con successo")
            try:
                bot.send_message(userDaBannare, "🚷 Sei stato bannato dal bot 🚷\n\nPer lo sban contattaci qui sotto", reply_markup=markupManager.assistenzaMarkupSenzaHome())
            except:
                pass
        else:
            bot.send_message(call.message.chat.id, "L'utente ID: " + str(userDaBannare) + " non è registrato al bot.")
        bot.delete_message(call.message.chat.id, call.message.id)



@bot.message_handler(commands=['start', 'home'])
def startCommand(message):
    commandStartManager.checkRegistrazione(message)
    if not fileManager.checkBannedStatus(message.chat.id):
        if len(message.text.split(" ")) > 1:
            # codice nel comando start
            command = message.text.split()[1]
            if funzioniManager.antiSpam(message.chat.id, command):
                #la funzione ritorna true quindi è l'avvio è voluto. È stato aggiunto all'array
                try:
                    #se il comando secondario di /start è il codice del modulo
                    tipoModulo = funzioniManager.getTextModulo(command).split("🐬")[1].strip().split(" ")[0].lower()
                    if tipoModulo == "asta":
                        bot.send_message(message.chat.id, "🫰 OFFERTA 🫰\n\n" + funzioniManager.getTextModulo(command).split("Per offrire clicca qui sotto 👇")[0] + "\n<b>Rispondi</b> a questo messaggio con la cifra che vuoi offrire, oppure offri cliccando il tasto sottostante.", reply_markup=markupManager.offertaAttualeMarkup(funzioniManager.getOfferta(command), command))
                    elif tipoModulo == "cercasi":
                        bot.send_message(message.chat.id, "🫰 POSSESSO 🫰\n\n" + funzioniManager.getTextModulo(command) + "\n\n cliccando qui sotto confermo di:\n   -possedere l'oggetto\n   -venderlo al prezzo stabilito nel cercasi", reply_markup=markupManager.confermaPossesso(codiceModulo=command))
                except Exception as e:
                    print(traceback.format_exc())
                    bot.send_message(message.chat.id, "C'è stato un errore nell'elaborazione di questo modulo.\n<b>Per offrire</b> clicca qui sotto e parla con un operatore")
                    with open("errori/errore_modulo_"+str(command)+".txt", "w", encoding='utf-8') as file:
                        file.write(str(traceback.format_exc()))
                        file.close()
                        bot.send_message(devCID, "Errore modulo " + str(command) + " aggiunto alla cartella errori. Buon mal di testa nel provare a risolverlo ;)")
            else:
                #sta spammando, l'utente si trova già nell'array
                bot.delete_message(message.chat.id, message.id)
        else:
            #semplice start
            schermateManager.showHome(message.chat.id)
            funzioniManager.rimuoviAntiSpam(message.chat.id)
            if message.chat.type == "supergroup":
                print(message.chat.id)
    else:
        bot.send_message(message.chat.id, "🚷 Sei stato bannato dal bot 🚷\n\nPer lo sban contattaci qui sotto", reply_markup=markupManager.assistenzaMarkupSenzaHome())

@bot.message_handler(commands=['assegnaPunti'])
def assegnaPuntiCommand(message):
    if message.reply_to_message is not None and message.reply_to_message.forward_from_chat is not None and str(message.chat.id) == str(groupStafferChat_id):
        #se ha risposto ad un messaggio valido e si trova nel gruppo staff
        moduloID = funzioniManager.messageTextToModuloID(message.reply_to_message.text)
        if fileManager.assegnaPuntiCompratoreVenditore(moduloID, None) is False:
            bot.reply_to(message.reply_to_message, "Qualcosa è andato storto nell'assegnazione dei punti, uno dei due utenti non è registrato al bot. Il direttore è stato automaticamente avvisato e se ne occuperà personalmente.")
        elif fileManager.assegnaPuntiCompratoreVenditore(moduloID, None) is True:
            bot.reply_to(message.reply_to_message, "I punti sono stati assegnati ad entrambi gli utenti con successo!")
        bot.delete_message(message.chat.id, message.id)


@bot.callback_query_handler(func=lambda call: call.data == "home/tastoModulo" and not fileManager.checkBannedStatus(call.message.chat.id))
def triggerTastoModulo(call):
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id,caption="Di quale modulo hai bisogno?", reply_markup=markupManager.scegliModuloMarkup())

@bot.callback_query_handler(func=lambda call: call.data == "home/tastoInfo" and not fileManager.checkBannedStatus(call.message.chat.id))
def triggerTastoinfo(call):
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id,caption="ℹ️ Informazioni ℹ️", reply_markup=markupManager.infoMarkup())

@bot.callback_query_handler(func=lambda call: call.data == "home/tastoInfo/tastoPuntoGratis" and not fileManager.checkBannedStatus(call.message.chat.id))
def triggerTastoPuntoGratis(call):
    if not sponsorManager.checkUserSponsor(call.message.chat.id):
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption="""
    🌟 <b>Come ottenere 2 Punti Gratis</b> 🌟

Hai voglia di guadagnare 2 punti ATC senza sforzo? Ecco come:

1️⃣ <b>Aggiorna il tuo Nome:</b> Vai nelle impostazioni del tuo profilo e cliccando sui 3 pallini in alto a destra, seleziona 'modifica Nome' o 'modifica Profilo', poi seleziona il tasto Nome.

2️⃣ <b>Aggiungi l'Hashtag:</b> Inserisci l'hashtag #AtlantisTradeCenter come parte del tuo Nome ('first_name'). Assicurati di inserirlo nel Nome, no cognome, username o bio.

3️⃣ <b>Tienilo per una Settimana:</b> Mantieni l'hashtag nel tuo 'first_name' per almeno una settimana consecutiva. Questo dimostrerà il tuo impegno.

4️⃣ <b>Ricevi i Tuoi Punti:</b> Una volta che hai mantenuto l'hashtag per una settimana, riceverai automaticamente 2 punti ATC come nostro ringraziamento.

Non c'è bisogno di fare altro! È un modo semplice per guadagnare punti e restare connessi con la nostra community. Grazie per il tuo sostegno! 😊🌟""", reply_markup=markupManager.puntiGratisMarkup())
    else:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=testiManager.testoSponsor(call.message.chat.id), reply_markup=markupManager.tastoBackToHome())


@bot.callback_query_handler(func=lambda call: call.data == "home/tastoInfo/tastoPuntoGratis/hoFattoBtn" and not fileManager.checkBannedStatus(call.message.chat.id))
def triggerTastoPuntoGratisHoFatto(call):
    if not sponsorManager.checkUserSponsor(call.message.chat.id):
        if str(call.message.chat.first_name).lower().__contains__("#atlantistradecenter"):
            sponsorManager.aggiungiUserSponsor(call.message.chat.id)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=testiManager.testoSponsor(call.message.chat.id), reply_markup=markupManager.tastoBackToHome())
        else:
            bot.answer_callback_query(call.id, "⚠️ Attenzione ⚠️\n\nNon risulta che hai l'hashtag #AtlantisTradeCenter sul tuo nome", show_alert=True)
    else:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=testiManager.testoSponsor(call.message.chat.id), reply_markup=markupManager.tastoBackToHome())


@bot.callback_query_handler(func=lambda call: call.data == 'tastoChiudiMessaggio' and not fileManager.checkBannedStatus(call.message.chat.id))
def chiudiMessaggio(call):
    schermateManager.setInvioModulo(call.message.chat.id, False)
    moduloVuoto.pop(call.message.chat.id, None)
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
    schermateManager.showHome(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'home/tastoModulo/tastoModuloVendita' and not fileManager.checkBannedStatus(call.message.chat.id))
def creaModuloVendita(call):
    bot.delete_message(call.message.chat.id, message_id=call.message.id)
    moduloInviatoDaBot = bot.send_message(chat_id=call.message.chat.id, text=moduliManager.asta(), reply_markup=markupManager.tastoChiudiMessaggio())
    moduloVuoto[call.message.chat.id] = moduloInviatoDaBot
    schermateManager.setInvioModulo(call.message.chat.id, True)


@bot.callback_query_handler(func=lambda call: call.data == 'home/tastoModulo/tastoModuloCercasi' and not fileManager.checkBannedStatus(call.message.chat.id))
def creaModuloCercasi(call):
    bot.delete_message(call.message.chat.id, message_id=call.message.id)
    moduloInviatoDaBot = bot.send_message(chat_id=call.message.chat.id, text=moduliManager.cercasi(), reply_markup=markupManager.tastoChiudiMessaggio())
    moduloVuoto[call.message.chat.id] = moduloInviatoDaBot
    schermateManager.setInvioModulo(call.message.chat.id, True)

@bot.message_handler(func=lambda message: str(message.text).startswith("🐬") and message.chat.type == "private")
def riceviModulo(message):
    try:
        moduloID = message.text.split("#")[1].split("\n\n")[0]
    except:
        moduloID = message.caption.split("#")[1].split("\n\n")[0]
    if message.chat.type == "private":
        # se si trova in una chat privata (user-bot)
        if schermateManager.canSendModulo(message.chat.id):
            # aggiungo questa condizione perchè sennò il bot mi da come errore che il messaggio da modificare non è stato modificato
            if moduloVuoto[message.chat.id].photo is not None:
                # +1 perchè è il messaggio successivo o +0 se vengono fatte modifiche una volta inviata la foto
                if message.text != moduloVuoto[message.chat.id].caption:
                    try:
                        messageModificato = bot.edit_message_caption(chat_id=message.chat.id, message_id=moduloVuoto[message.chat.id].id + 1, caption=message.text, reply_markup=markupManager.inviaModuloAlloStaff())
                    except:
                        messageModificato = bot.edit_message_caption(chat_id=message.chat.id, message_id=moduloVuoto[message.chat.id].id, caption=message.text, reply_markup=markupManager.inviaModuloAlloStaff())
            else:
                if message.text != moduloVuoto[message.chat.id].text:
                    messageModificato = bot.edit_message_text(chat_id=message.chat.id, message_id=moduloVuoto[message.chat.id].id, text=message.text, reply_markup=markupManager.inviaModuloAlloStaff())
            bot.delete_message(chat_id=message.chat.id, message_id=message.id)
            try:
                moduloVuoto[message.chat.id] = messageModificato
            except:
                pass
        else:
            bot.delete_message(message.chat.id, message.id)
            schermateManager.showHome(message.chat.id)
    #se invece si trova nel gruppo moduli è per fare una modifica
    elif message.chat.type == "supergroup":
        if str(message.chat.id) == str("-1001974658159"):
            if message.reply_to_message != None:
                userUrl = message.reply_to_message.reply_markup.keyboard[0][0].url
                userChat_id = userUrl.split("=")[1]
                if message.reply_to_message.photo is None:
                    #Se non contiene una foto
                    bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text=message.text, reply_markup=markupManager.tastiEsitoModulo(userChat_id))
                else:
                    bot.edit_message_caption(chat_id=message.chat.id, message_id=message.reply_to_message.id, caption=message.text, reply_markup=markupManager.tastiEsitoModulo(userChat_id))

            bot.delete_message(message.chat.id, message.id)

@bot.message_handler(content_types=['photo'])
def fotoModulo(message):
    if str(message.chat.id) == str(groupStafferChat_id):
        #si tratta di un modulo nel gruppo staff
        pass
    else:
        fileManager.arrivoFoto(message, moduloVuoto)

@bot.callback_query_handler(func=lambda call: call.data == 'tastoModuloVenditaInviaStaff' and not fileManager.checkBannedStatus(call.message.chat.id))
def InviaModulo(call):
    moduliManager.inviaModulo(call)
    schermateManager.setInvioModulo(call.message.chat.id, False)
    # resetta i messaggiDaCancellare[]
    if call.message.chat.id in moduloVuoto:
        moduloVuoto.pop(call.message.chat.id, None)

@bot.callback_query_handler(func=lambda call: call.data == 'backToHomeBtn' and not fileManager.checkBannedStatus(call.message.chat.id))
def backToHome(call):
    try:
        bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption="🏠 Home 🏠\n\n🆕 I tuoi Punti: " + str(fileManager.getPoint(call.message.chat.id)) + " 🆕", reply_markup=markupManager.homeMarkup())
    except:
        bot.delete_message(call.message.chat.id, call.message.id)
        schermateManager.showHome(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'tastoModuloIndietro' and not fileManager.checkBannedStatus(call.message.chat.id))
def backModulo(call):
    backToHome(call)
    # rimuovi chat id dall'anti spam
    funzioniManager.rimuoviAntiSpam(call.message.chat.id)

@bot.callback_query_handler(func=lambda call: call.data == 'capito' and not fileManager.checkBannedStatus(call.message.chat.id))
def capitoBtn(call):
    bot.delete_message(call.message.chat.id, call.message.id)


@bot.callback_query_handler(func=lambda call: call.data == 'tastoModuloApprova' and not fileManager.checkBannedStatus(call.message.chat.id))
def approvaModulo(call):
    moduloIncompleto = moduliManager.componiModulo(call)
    moduliManager.postaModulo(call, moduloIncompleto, False)

@bot.callback_query_handler(func=lambda call: call.data == 'tastoModuloApprovaEdit' and not fileManager.checkBannedStatus(call.message.chat.id))
def approvaModulo(call):
    moduloIncompleto = moduliManager.componiModulo(call)
    moduliManager.postaModulo(call, moduloIncompleto, True)

@bot.callback_query_handler(func=lambda call: call.data == 'tastoModuloRifiuta' and not fileManager.checkBannedStatus(call.message.chat.id))
def rifiutaModulo(call):
    userUrl = call.message.reply_markup.keyboard[0][0].url
    bot.edit_message_reply_markup(groupModuliChat_id, call.message.id, reply_markup=markupManager.tastiRifiutaModulo(userUrl))

#motivazione rifiuta modulo
@bot.callback_query_handler(func=lambda call: call.data.startswith('tastoModuloRifiuta|') and not fileManager.checkBannedStatus(call.message.chat.id))
def rifiutaModuloMotivazione(call):
    stafferModulo = call.from_user.first_name
    #Invia messaggio all'utente
    userUrl = call.message.reply_markup.keyboard[0][0].url
    userChat_id = userUrl.split("=")[1]
    motivazione = call.data.split('|')[1]
    testoMotivazione = ""
    if motivazione == "incompleto":
        testoMotivazione = "Il modulo che hai inviato è incompleto. Per favore, assicurati di aver compilato tutti i campi richiesti."
    elif motivazione == "pocoInteressante":
        testoMotivazione = "Il tuo modulo è stato considerato poco rilevante. Se hai altre offerte o richieste da condividere, ti incoraggiamo a farlo."
    elif motivazione == "prezzoNonConsono":
        testoMotivazione = "Il prezzo nel tuo modulo non è adatto al prodotto. Ti consigliamo di rivederlo prima di inviare nuovamente il modulo."
    elif motivazione == "altro":
        testoMotivazione = "Un nostro operatore ti contatterà a breve per spiegarti il motivo per il quale il tuo modulo è stato rifiutato."
    if testoMotivazione != "":
        #modifica il call.message
        if call.message.photo is None:
            moduloID = funzioniManager.messageTextToModuloID(call.message.text)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"{call.message.text}\n\nRifiutata da: {stafferModulo}", reply_markup=markupManager.showUser(userUrl))
        else:
            moduloID = funzioniManager.messageTextToModuloID(call.message.caption)
            bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.id, caption=f"{call.message.caption}\n\nRifiutata da: {stafferModulo}", reply_markup=markupManager.showUser(userUrl))
        #Invia messaggio
        text = f"Oh no! Il tuo modulo #{moduloID} è stato rifiutato, ecco la motivazione:\n\n<b>{testoMotivazione}</b>\n\nSe pensi si tratti di un errore, non esitare a contattarci cliccando il tasto qui sotto."
        bot.send_message(userChat_id, text, reply_markup=markupManager.contattaAssistenzaMarkup())

@bot.callback_query_handler(func=lambda call: call.data.startswith("confermaPossessoN") and not fileManager.checkBannedStatus(call.message.chat.id))
def conferma_possesso_handler(call):
    moduloID = call.data.split("confermaPossessoN")[1]
    bot.edit_message_reply_markup(chat_id=canaleAste, message_id=funzioniManager.getMessageID(moduloID), reply_markup=markupManager.setOggettoTrovato())
    fileManager.setNewOfferente(moduloID=moduloID, newOfferente=call.message.chat.id)
    funzioniManager.setIsTerminata(moduloID, True)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🐬 Modulo #" + str(moduloID) + " 🐬\n\nVendita confermata con successo!", reply_markup=markupManager.tastoBackToHome())
    # rimuovi user dall'anti spam
    funzioniManager.rimuoviAntiSpam(call.message.chat.id)
    urlUser = "tg://user?id=" + str(call.message.chat.id)
    try:
        bot.send_message(funzioniManager.getStafferModulo(moduloID), f"🤑 Cercasi terminato. L'utente qui sotto ha dato disponibilità dell'oggetto per il cercasi #{moduloID}! 💸\nL'attuale offerta è: {funzioniManager.getOfferta(moduloID)}\n\nVai a effettuare lo scambio!", reply_markup=markupManager.visualizzaClientiCercasi(urlUser, moduloID))
        bot.send_message(chat_id=groupStafferChat_id, text=f"🤑 Cercasi #{moduloID} terminato con successo 💸\n\nÈ stato inviato un messaggio allo staffer che ha preso in carico questo cercasu per effettuare lo scambio!")
    except:
        bot.send_message(chat_id=groupStafferChat_id, text=f"🤑Non sono riuscito a contattare il delegato ID: {funzioniManager.getStafferModulo(moduloID)}. Il cercasi #{moduloID} è terminato 💸\nL'attuale offerta è: {funzioniManager.getOfferta(moduloID)}\n\nVai a effettuare lo scambio!", reply_markup=markupManager.visualizzaClientiCercasi(urlUser, moduloID))


@bot.callback_query_handler(func=lambda call: call.data.startswith("rilancioMinimo#") and not fileManager.checkBannedStatus(call.message.chat.id))
def rilanciaConRilancioMinimo(call):
    moduloID = call.data.split("rilancioMinimo#")[1].split("#")[0]
    rilancioMinimo = call.data.split("#")[2]
    offerteManager.registraOffertaFromCall(call.message, moduloID, rilancioMinimo)


@bot.callback_query_handler(func=lambda call: call.data.startswith("compraOra#") and not fileManager.checkBannedStatus(call.message.chat.id))
def compraOra(call):
    moduloID = call.data.split("compraOra#")[1]
    offerteManager.compraOra(call.message, moduloID)


@bot.message_handler(commands=['manage'])
def manageCommand(message):
    if str(message.chat.id) == str(groupStafferChat_id):
        if message.reply_to_message.forward_from_chat is not None:
            if str(message.reply_to_message.forward_from_chat.username) == str(canaleAste.split("@")[1]):
                #.split perchè la funzione ritorna il nome del file
                #se il modulo viene dal canale
                try:
                    moduloID = funzioniManager.getModuloIdFromMessageId(message.reply_to_message.forward_from_message_id).split(".txt")[0]
                except:
                    if message.reply_to_message is not None:
                        try:
                            moduloID = message.reply_to_message.text.split("#")[1].split("\n\n")[0]
                        except:
                            moduloID = message.reply_to_message.caption.split("#")[1].split("\n\n")[0]
                bot.reply_to(message.reply_to_message, "Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))
        else:
            bot.reply_to(message, "Devi rispondere ad un messaggio!")
    bot.delete_message(message.chat.id, message.id)

#Inizio vari handler tasti gestione moduli per lo staff
@bot.callback_query_handler(func=lambda call: call.data.startswith("tornaDisponibileCercasi#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloTornaDispinibileCercasi(call):
    moduloID = call.data.split("#")[1]
    funzioniManager.setIsTerminata(moduloID, False)
    fileManager.setNewOfferente(moduloID, None)
    fileManager.setNewOfferta(moduloID, None)
    try:
        bot.edit_message_reply_markup(canaleAste, funzioniManager.getMessageID(moduloID), reply_markup=markupManager.offriCustomStartUrlCercasi(moduloID))
    except:
        pass
    try:
        bot.edit_message_reply_markup(groupStafferChat_id, call.message.id, reply_markup=markupManager.manageModuloStaff(moduloID))
    except:
        pass

@bot.callback_query_handler(func=lambda call: call.data.startswith("ultima_offerta#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloUltimaOfferta(call):
    moduloID = call.data.split("#")[1]
    offerta = funzioniManager.getOfferta(moduloID)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🆔: #" + str(moduloID) + "\n\n💸 Offerta attuale: " + str(offerta), reply_markup=markupManager.manageModuloUltimaOffertaStaff(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("setNew_ultima_offerta#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloUltimaOffertaSetNew(call):
    moduloID = call.data.split("#")[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="📝 set offerta 📝\n\n" + call.message.text + "\n\n <b>rispondi</b> a questo messaggio scrivendo la nuova offerta.", reply_markup=markupManager.backToManageModulo(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("reset_ultima_offerta#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloResetUltimaOfferta(call):
    moduloID = call.data.split("#")[1]
    #scrive nel file
    fileManager.setNewOfferta(moduloID, None)
    funzioniManager.setIsTerminata(moduloID, False)
    #modifica il post sul canale
    moduliManager.moficaModuloOfferta(moduloID, None)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("ultimo_offerente#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloUltimoOfferente(call):
    moduloID = call.data.split("#")[1]
    offerenteChatID = funzioniManager.getOfferente(moduloID)
    if offerenteChatID is not None:
        offerenteUrl = "tg://user?id=" + str(offerenteChatID)
    else:
        offerenteUrl = None
    try:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🆔: #" + str(moduloID) + "\n\n🆔 offerente: " + str(offerenteChatID), reply_markup=markupManager.manageModuloUltimoOfferenteStaff(moduloID, offerenteUrl))
    except:
        offerenteUrl = None
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🆔: #" + str(moduloID) + "\n\n🆔 offerente: " + str(offerenteChatID), reply_markup=markupManager.manageModuloUltimoOfferenteStaff(moduloID, offerenteUrl))

@bot.callback_query_handler(func=lambda call: call.data.startswith("setNew_ultimo_offerente#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloUltimoOfferenteSetNew(call):
    moduloID = call.data.split("#")[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="📝 set offerente 📝\n\n" + call.message.text + "\n\n <b>rispondi</b> a questo messaggio scrivendo il chat ID del nuovo offerente.", reply_markup=markupManager.backToManageModulo(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("reset_ultimo_offerente#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloResetUltimoOfferente(call):
    moduloID = call.data.split("#")[1]
    fileManager.setNewOfferente(moduloID, None)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("testo#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloMessageID(call):
    moduloID = call.data.split("#")[1]
    testo = funzioniManager.getTextModulo(moduloID)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🆔: #" + str(moduloID) + f"\n\n📄 Testo:\n<code>{str(testo)}</code>", reply_markup=markupManager.manageModuloTextStaff(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("message_id#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloMessageID(call):
    moduloID = call.data.split("#")[1]
    messageID = funzioniManager.getMessageID(moduloID)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="🆔: #" + str(moduloID) + "\n\n🆔 messaggio: " + str(messageID), reply_markup=markupManager.manageModuloMessageIDStaff(moduloID))


@bot.callback_query_handler(func=lambda call: call.data.startswith("setNew_moduloText#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloTextSetNew(call):
    moduloID = call.data.split("#")[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="📝 set nuovo testo 📝\n\n" + call.message.text + "\n\n <b>rispondi</b> a questo messaggio scrivendo il nuovo testo.", reply_markup=markupManager.backToManageModulo(moduloID))


@bot.callback_query_handler(func=lambda call: call.data.startswith("setNew_moduloMessageID#") and not fileManager.checkBannedStatus(call.message.chat.id))
def manageModuloMessageIDSetNew(call):
    moduloID = call.data.split("#")[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="📝 set message ID 📝\n\n" + call.message.text + "\n\n <b>rispondi</b> a questo messaggio scrivendo il nuovo message ID.", reply_markup=markupManager.backToManageModulo(moduloID))

@bot.callback_query_handler(func=lambda call: call.data.startswith("tastoTerminaAsta#") and not fileManager.checkBannedStatus(call.message.chat.id))
def tastoTerminaAsta(call):
    moduloID = call.data.split("#")[1]
    funzioniManager.setIsTerminata(moduloID, True)
    bot.edit_message_reply_markup(chat_id=canaleAste, message_id=funzioniManager.getMessageID(moduloID), reply_markup=markupManager.setFineAstaMarkup())
    try:
        bot.send_message(funzioniManager.getStafferModulo(moduloID), f"🤑 La tua asta #{moduloID} è terminata! 💸\nL'attuale offerta è: {funzioniManager.getOfferta(moduloID)}\n\nVai a effettuare lo scambio!", reply_markup=markupManager.visualizzaClientiAstaTerminata(moduloID))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"🤑 Asta #{moduloID} terminata con successo 💸\n\nÈ stato inviato un messaggio allo staffer che ha preso in carico quest'asta per effettuare lo scambio!")
    except:
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text=f"🤑Non sono riuscito a contattare il delegato ID: {funzioniManager.getStafferModulo(moduloID)}. L'asta #{moduloID} è terminata 💸\nL'attuale offerta è: {funzioniManager.getOfferta(moduloID)}\n\nVai a effettuare lo scambio!", reply_markup=markupManager.visualizzaClientiAstaTerminata(moduloID))


@bot.callback_query_handler(func=lambda call: call.data.startswith("termina#") and not fileManager.checkBannedStatus(call.message.chat.id))
def setTerminaModulo(call):
    moduloID = call.data.split("#")[1]
    if "asta" in str(funzioniManager.getTextModulo(moduloID)).lower():
        #il modulo da terminare è un'asta
        tastoTerminaAsta(call)
    else:
        #il modulo è un cercasi
        bot.edit_message_reply_markup(chat_id=canaleAste, message_id=funzioniManager.getMessageID(moduloID), reply_markup=markupManager.setOggettoTrovato())
    funzioniManager.setIsTerminata(moduloID, True)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))


@bot.callback_query_handler(func=lambda call: call.data == "tastoChiudiElimina" and not fileManager.checkBannedStatus(call.message.chat.id))
def chiudiMessaggioElimina(call):
    bot.delete_message(call.message.chat.id, call.message.id)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tastoBackManage#") and not fileManager.checkBannedStatus(call.message.chat.id))
def backToManageModulo(call):
    manageCommand(call.message)

#Fine vari handler tasti gestione moduli per lo staff
@bot.callback_query_handler(func=lambda call: call.data.startswith("scambioEffettuato#") and not fileManager.checkBannedStatus(call.message.chat.id))
def tastoScambioEffettuato(call):
    moduloID = call.data.split("#")[1]
    if not call.message.chat.id in taskManager.twoTimesClickScambio:
        #il chat_id non si trova nella lista ---> è il 'primo' click
        taskManager.twoTimesClickScambio.append(call.message.chat.id)
        bot.answer_callback_query(call.id, "⚠️ Attenzione ⚠️\nCliccando di nuovo questo tasto confermerai che:\n - lo scambio è stato effettuato\n - la tassa è stata pagata\nVerranno assegnati automaticamente i punti a venditore e compratore", show_alert=True)
    else:
        #Lo scambio è stato confermato (doppio click)
        if fileManager.assegnaPuntiCompratoreVenditore(moduloID, None) is False:
            bot.send_message(call.message.chat.id, "Qualcosa è andato storto nell'assegnazione dei punti, uno dei due utenti non è registrato al bot. Il direttore è stato automaticamente avvisato e se ne occuperà personalmente.")
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=f"Modulo #{moduloID} contrassegnato come completato.")
        bot.send_message(devCID, f"Il tuo delegato ID: {call.message.chat.id}\nNome utente: {call.message.chat.username}\nNome: {call.message.chat.first_name}\n\nHa effettuatolo scambio di questo modulo:\n\n{funzioniManager.getTextModulo(moduloID)}\n\nL'offerta è di {funzioniManager.getOfferta(moduloID)}")
        try:
            taskManager.twoTimesClickScambio.remove(call.message.chat.id)
        except:
            pass
        #chiedi una recensione ai 2 clienti
        recensioniManager.chiediRecensioneClienti(moduloID)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tastoLasciaRecensione#") and not fileManager.checkBannedStatus(call.message.chat.id))
def tastoLasciaRecensione(call):
    moduloID = call.data.split("#")[1]
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💫 Come valuteresti l'esperienza generale di questo scambio? 💫", reply_markup=recensioniManager.recensioneMarkup(moduloID))


@bot.callback_query_handler(func=lambda call: call.data.startswith("stellaRecensione") and not fileManager.checkBannedStatus(call.message.chat.id))
def sceltaStellaRecensione(call):
    try:
        recensione = call.data.split("stellaRecensione")[1]
    except:
        recensione = call.data.split("stellaRecensione")

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="""
🌟 <b>Grazie per la Tua Recensione!</b> 🐬

Ciao! Volevamo esprimere la nostra gratitudine per la tua recensione. La tua opinione è importante per noi e ci aiuta a migliorare costantemente la nostra community.

Grazie per aver dedicato del tempo per condividere la tua esperienza. Apprezziamo il tuo contributo e speriamo che tu possa continuare a essere parte della nostra community. 😊🌟""", reply_markup=markupManager.tastoBackToHome())
    moduloID = call.message.reply_markup.keyboard[0][0].callback_data
    bot.send_message(groupStafferChat_id, f"🌟 Recensione 🌟\n\nIl modulo #{moduloID} è stato valutato dall'utente ID:{call.message.chat.id} con {recensione} stelle.")


@bot.message_handler(func=lambda message: message.reply_to_message is not None and not fileManager.checkBannedStatus(message.chat.id))
def handle_reply(message):
    if message.reply_to_message.text.startswith("📝 set offerta 📝"):
        #se viene mandata la nuova offerta manualmente
        moduloID = message.reply_to_message.text.split("#")[1].split("\n")[0]
        compraOra = funzioniManager.getTextModulo(moduloID).split("🏦 Compra ora: ")[1].split("\n")[0]
        if funzioniManager.getOfferta(moduloID) is None or not int(funzioniManager.abbrev_to_number(funzioniManager.getOfferta(moduloID))) >= int(funzioniManager.abbrev_to_number(compraOra)):
            try:
                funzioniManager.setIsTerminata(moduloID, False)
                funzioniManager.aggiungiUnOraAsta(moduloID)
            except:
                pass
            #quindi, se l'offerta nel file è None (non c'è) oppure se l'offerta (c'è nel file) e non è maggiore o uguale al compra ora (altrimenti significa che è stato utilizzato), procede...
            fileManager.setNewOfferta(moduloID, message.text)
            bot.delete_message(message.chat.id, message.id)
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))
        else:
            bot.send_message(message.chat.id, "L'asta è terminata", reply_markup=markupManager.tastoChiudiMessaggio())
        #aggiorna l'offerta sul canale
        moduliManager.moficaModuloOfferta(moduloID, message.text)

    elif message.reply_to_message.text.startswith("📝 set offerente 📝"):
        #se viene mandato il chat id del nuovo offerente
        moduloID = message.reply_to_message.text.split("#")[1].split("\n")[0]
        fileManager.setNewOfferente(moduloID, message.text)
        bot.delete_message(message.chat.id, message.id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))
    elif message.reply_to_message.text.startswith("📝 set message ID 📝"):
        #se viene mandato il nuovo message ID
        moduloID = message.reply_to_message.text.split("#")[1].split("\n")[0]
        fileManager.setNewMessageID(moduloID, message.text)
        bot.delete_message(message.chat.id, message.id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))
    elif message.reply_to_message.text.startswith("📝 set nuovo testo 📝"):
        #se viene mandato il nuovo testo da modificare
        moduloID = message.reply_to_message.text.split("#")[1].split("\n")[0]
        #questa funzione modifica sia il file che il messaggio postato sul canale.
        fileManager.setNewText(moduloID, message.text)
        bot.delete_message(message.chat.id, message.id)
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text="Modulo #" + str(moduloID), reply_markup=markupManager.manageModuloStaff(moduloID))
    elif message.reply_to_message.text.startswith("🫰 OFFERTA 🫰"):
        offerteManager.registraOfferta(message)
    elif message.reply_to_message.text.startswith("🏆  Punti 🏆"):
        if int(message.text) % 1 == 0:
            #se è intero...
            moduloID = message.reply_to_message.text.split("#")[1].split("\n")[0]
            fileManager.assegnaPuntiCompratoreVenditore(funzioniManager.messageTextToModuloID(message.reply_to_message.text), int(message.text))
            bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text=f"I punti del modulo #{moduloID} sono stati assegnati a entrambi i clienti con successo.")
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        else:
            bot.reply_to(message, "La cifra inserita non è valida. I punti devono essere numeri interi.")


@bot.message_handler(func=lambda message: message.forward_from is not None and not fileManager.checkBannedStatus(message.chat.id))
def handle_forwarded_message(message):
    chat_id = message.forward_from.id
    text = "ID: <code>" + str(chat_id) + "</code>" + "\n\n" + fileManager.getInfoUser(chat_id)
    urlUser = "tg://user?id=" + str(chat_id)
    bot.send_message(message.chat.id, text, reply_markup=markupManager.showUser(urlUser))

#schedule part - check fine asta ecc...
scheduler.add_job(taskManager.checkFineAsta, 'interval', seconds=55)
scheduler.add_job(taskManager.checkUtentiSponsor, 'interval', seconds=120)


bot.add_custom_filter(custom_filters.TextStartsFilter())

# Avvia lo scheduler
scheduler.start()
bot.polling(none_stop=True)

# Attendi che il bot Telegram e lo scheduler terminino
try:
    bot.infinity_polling()
except (KeyboardInterrupt, SystemExit):
    # Chiudi il bot in modo pulito quando si preme Ctrl+C
    bot.stop_polling()
    scheduler.shutdown()
