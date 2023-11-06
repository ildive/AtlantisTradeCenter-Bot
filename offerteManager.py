import telebot

import fileManager
import funzioniManager
import markupManager

from secrets import *

bot = telebot.TeleBot(token, parse_mode="HTML")

def registraOfferta(message):
    moduloID = funzioniManager.messageTextToModuloID(message.reply_to_message.text)
    messageID = funzioniManager.getMessageID(moduloID)
    photo = funzioniManager.getPhotoBool(moduloID)
    if message.reply_to_message.text.startswith("🫰 OFFERTA 🫰"):
        # è una offerta.
        text = message.text.replace(',', '.')
        if funzioniManager.getIsTerminata(moduloID) is not True:
            #se non è terminata
            if funzioniManager.getOfferta(moduloID) != None:
                #se è la seconda o più offerta..
                ultimoOfferenteChatID = funzioniManager.getOfferente(moduloID)
                try:
                    if int(funzioniManager.abbrev_to_number(text)) - int(funzioniManager.abbrev_to_number(funzioniManager.getRilancio(funzioniManager.getTextFromModuloID(moduloID)))) >= int(funzioniManager.abbrev_to_number(funzioniManager.getOfferta(moduloID))):
                        #OFFERTA RILANCIO VALIDA (offerta inserita - rilancio >= ultima offerta)
                        if not int(funzioniManager.abbrev_to_number(text)) >= int(funzioniManager.abbrev_to_number(funzioniManager.getCompraOra(message.reply_to_message.text))):
                            #se l'offerta ricevuta non è maggiore o uguale al compra ora dell'asta a cui si sta offrendo fai questo:
                            if photo:
                                messageAstaCanale = bot.edit_message_caption(chat_id=canaleAste, message_id=messageID, caption=funzioniManager.getTextModulo(moduloID), reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(text.lower()), moduloID, True))
                            else:
                                messageAstaCanale = bot.edit_message_text(chat_id=canaleAste, message_id=messageID, text=funzioniManager.getTextModulo(moduloID), reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(text.lower()), moduloID, True))
                            fileManager.setNewOfferta(moduloID, newOfferta=funzioniManager.number_to_abbrev(text))
                            fileManager.setNewOfferente(moduloID, newOfferente=message.chat.id)
                            funzioniManager.aggiungiUnOraAsta(moduloID)
                            bot.delete_message(message.chat.id, message.id)
                            bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text=message.reply_to_message.text.split("🫰 OFFERTA 🫰\n\n")[1].split("\n\n\n")[0], reply_markup=markupManager.offertaRegistrataMarkup(funzioniManager.getMessageID(moduloID)))
                            #rimuovi utente dall'anti-spam
                            funzioniManager.rimuoviAntiSpam(message.chat.id)
                            try:
                                bot.send_message(ultimoOfferenteChatID, "😩 <b>OH NO</b>! 😩\nLa tua offerta è stata superata da qualcun'altro. Clicca qui sotto per vedere i dettagli", reply_markup=markupManager.redirectPostCanale(messageAstaCanale.id))
                            except:
                                pass
                        else:
                            # se l'offerta ricevuta è maggiore o uguale al compra ora dell'asta a cui si sta offrendo fai questo:
                            compraOra(message, moduloID)
                            bot.delete_message(message.chat.id, message.id)
                    else:
                        #Offerta inferiore al rilancio minimo
                        rilancioMinimo = int(funzioniManager.abbrev_to_number(funzioniManager.getOfferta(moduloID))) + int(funzioniManager.abbrev_to_number(funzioniManager.getRilancio(funzioniManager.getTextModulo(moduloID))))
                        bot.reply_to(message, "Il rilancio è troppo basso, il minimo deve essere: " + str(funzioniManager.number_to_abbrev(int(rilancioMinimo))))
                except:
                    bot.send_message(message.chat.id, "L'offerta che hai inserito non è valida. Riprova, oppure se pensi che si tratti di un errore contattaci", reply_markup=markupManager.contattaAssistenzaMarkup())
            else:
                #è la prima offerta
                if int(funzioniManager.abbrev_to_number(text)) >= int(funzioniManager.abbrev_to_number(funzioniManager.getBaseAsta(funzioniManager.getTextModulo(moduloID)))):
                    #se l'offerta scritta è maggiore o uguale alla base dell'asta:
                    if not int(funzioniManager.abbrev_to_number(text)) >= int(funzioniManager.abbrev_to_number(funzioniManager.getCompraOra(message.reply_to_message.text))):
                        #se l'offerta ricevuta non è maggiore o uguale al compra ora dell'asta a cui si sta offrendo fai questo:
                        if photo:
                            bot.edit_message_reply_markup(chat_id=canaleAste, message_id=messageID, reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(text.lower()), moduloID, True))
                        else:
                            bot.edit_message_reply_markup(chat_id=canaleAste, message_id=messageID, reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(text.lower()), moduloID, True))
                            fileManager.setNewOfferta(moduloID, newOfferta=funzioniManager.number_to_abbrev(text))
                            fileManager.setNewOfferente(moduloID, newOfferente=message.chat.id)
                        funzioniManager.aggiungiUnOraAsta(moduloID)
                        bot.delete_message(message.chat.id, message.id)
                        bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text=message.reply_to_message.text.split("🫰 OFFERTA 🫰\n\n")[1].split("\n\n\n")[0], reply_markup=markupManager.offertaRegistrataMarkup(funzioniManager.getMessageID(moduloID)))
                        # rimuovi utente dall'anti-spam
                        funzioniManager.rimuoviAntiSpam(message.chat.id)
                    else:
                        # se l'offerta ricevuta è maggiore o uguale al compra ora dell'asta a cui si sta offrendo fai questo:
                        compraOra(message, moduloID)
                        bot.delete_message(message.chat.id, message.id)
                else:
                   bot.reply_to(message, "L'offerta è troppo bassa, la minima deve essere " + funzioniManager.number_to_abbrev(funzioniManager.getBaseAsta(funzioniManager.getTextFromModuloID(moduloID)).strip()))
        else:
            bot.send_message(message.chat.id, "L'asta a cui stai cercando di offrire è attualmente terminata", reply_markup=markupManager.tastoBackToHome())
    #else:
        #è un cercasi

def registraOffertaFromCall(message, moduloID, rilancioMinimo):
    photo = funzioniManager.getPhotoBool(moduloID)
    messageID = funzioniManager.getMessageID(moduloID)
    if funzioniManager.getIsTerminata(moduloID) is not True:
        if funzioniManager.getOfferta(moduloID) != None:
            # se è la seconda o più offerta..
            ultimoOfferenteChatID = funzioniManager.getOfferente(moduloID)
            if int(funzioniManager.abbrev_to_number(rilancioMinimo)) >= int(funzioniManager.abbrev_to_number(funzioniManager.getOfferta(moduloID))) + int(funzioniManager.abbrev_to_number(funzioniManager.getRilancio(funzioniManager.getTextModulo(moduloID)))):
                #se l'offerta è valida e non ho cliccato per esempio offri 100 ad un asta che ormai ha superato i 10k
                if photo:
                    messageAstaCanale = bot.edit_message_caption(chat_id=canaleAste, message_id=messageID, caption=funzioniManager.getTextModulo(moduloID), reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(rilancioMinimo.lower()), moduloID, True))
                else:
                    messageAstaCanale = bot.edit_message_text(chat_id=canaleAste, message_id=messageID, text=funzioniManager.getTextModulo(moduloID), reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(rilancioMinimo.lower()), moduloID, True))
                fileManager.setNewOfferta(moduloID, newOfferta=funzioniManager.number_to_abbrev(rilancioMinimo))
                fileManager.setNewOfferente(moduloID, newOfferente=message.chat.id)
                funzioniManager.aggiungiUnOraAsta(moduloID)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=message.text.split("🫰 OFFERTA 🫰\n\n")[1].split("\n\n\n")[0], reply_markup=markupManager.offertaRegistrataMarkup(funzioniManager.getMessageID(moduloID)))
                #rimuovi utente dall'anti-spam
                funzioniManager.rimuoviAntiSpam(message.chat.id)
                try:
                    bot.send_message(ultimoOfferenteChatID, "😩 <b>OH NO</b>! 😩\nLa tua offerta è stata superata da qualcun'altro. Clicca qui sotto per vedere i dettagli", reply_markup=markupManager.redirectPostCanale(messageAstaCanale.id))
                except:
                    pass
            else:
                bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=markupManager.offertaAttualeMarkup(funzioniManager.getOfferta(moduloID), moduloID))
                bot.reply_to(message, "la cifra che volevi offrire è stata ormai superata, ecco l'offerta attuale")
        else:
            #è la prima offerta
            if int(funzioniManager.abbrev_to_number(rilancioMinimo)) >= int(funzioniManager.abbrev_to_number(funzioniManager.getBaseAsta(funzioniManager.getTextModulo(moduloID)))):
                if photo:
                    bot.edit_message_reply_markup(chat_id=canaleAste, message_id=messageID, reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(rilancioMinimo.lower()), moduloID, True))
                else:
                    bot.edit_message_reply_markup(chat_id=canaleAste, message_id=messageID, reply_markup=markupManager.setOffertaMarkup(funzioniManager.number_to_abbrev(rilancioMinimo.lower()), moduloID, True))
                fileManager.setNewOfferta(moduloID, newOfferta=funzioniManager.number_to_abbrev(rilancioMinimo))
                fileManager.setNewOfferente(moduloID, newOfferente=message.chat.id)
                funzioniManager.aggiungiUnOraAsta(moduloID)
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=message.text.split("🫰 OFFERTA 🫰\n\n")[1].split("\n\n\n")[0], reply_markup=markupManager.offertaRegistrataMarkup(funzioniManager.getMessageID(moduloID)))
                # rimuovi utente dall'anti-spam
                funzioniManager.rimuoviAntiSpam(message.chat.id)
            else:
                try:
                    bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=markupManager.offertaAttualeMarkup(funzioniManager.getOfferta(moduloID), moduloID))
                except:
                    bot.edit_message_reply_markup(message.chat.id, message.id, reply_markup=markupManager.offertaAttualeMarkup(funzioniManager.getBaseAsta(funzioniManager.getTextModulo(moduloID)), moduloID))
                bot.reply_to(message, "la cifra che volevi offrire è stata ormai superata, ecco l'offerta attuale")
    else:
        bot.send_message(message.chat.id, "L'asta a cui stai cercando di offrire è attualmente terminata", reply_markup=markupManager.tastoBackToHome())


def compraOra(message, moduloID):
    ultimoOfferente = funzioniManager.getOfferente(moduloID)
    fileManager.setNewOfferta(moduloID, newOfferta=funzioniManager.number_to_abbrev(funzioniManager.getCompraOra(funzioniManager.getTextModulo(moduloID))))
    fileManager.setNewOfferente(moduloID, newOfferente=message.chat.id)
    messageAstaCanale = bot.edit_message_reply_markup(chat_id=canaleAste, message_id=funzioniManager.getMessageID(moduloID), reply_markup=markupManager.setFineAstaMarkup())
    funzioniManager.setIsTerminata(moduloID, True)
    if message.reply_to_message is None:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.id, text="🐬 Modulo #" + str(moduloID) + " 🐬\n\nCompra ora confermato con successo!", reply_markup=markupManager.redirectPostCanaleTornaALlaHome(funzioniManager.getMessageID(moduloID)))
    else:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.reply_to_message.id, text="🐬 Modulo #" + str(moduloID) + " 🐬\n\nCompra ora confermato con successo!", reply_markup=markupManager.tastoBackToHome())
    urlUser = "tg://user?id=" + str(message.chat.id)
    try:
        bot.send_message(funzioniManager.getStafferModulo(moduloID), f"🤑 È stata utilizzato il compra ora per la tua asta #{moduloID}! 💸\n\nVai a effettuare lo scambio!", reply_markup=markupManager.visualizzaClientiCompraOra(urlUser, moduloID))
        bot.send_message(chat_id=groupStafferChat_id, text=f"🤑 Asta #{moduloID} terminata con successo con Compra Ora 💸\n\nÈ stato inviato un messaggio allo staffer che ha preso in carico quest'asta per effettuare lo scambio!")
    except:
        bot.send_message(chat_id=groupStafferChat_id, text=f"🤑Non sono riuscito a contattare il delegato ID: {funzioniManager.getStafferModulo(moduloID)}. L'asta #{moduloID} è terminata con un Compra Ora 💸\n\nVai a effettuare lo scambio!", reply_markup=markupManager.visualizzaClientiCompraOra(urlUser, moduloID))
    if ultimoOfferente is not None and str(ultimoOfferente) != str(message.chat.id):
        bot.send_message(ultimoOfferente, "Qualcuno ha usato il compra ora per questa asta", reply_markup=markupManager.redirectPostCanale(messageAstaCanale.id))
