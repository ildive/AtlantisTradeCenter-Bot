import secrets

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import funzioniManager

def banUtente(chatID_daBannare):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🔨 Bannalo malissimo 💥", callback_data="banUser#" + str(chatID_daBannare)))
    return markup

def homeMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📄 Crea un modulo 📄", callback_data="home/tastoModulo"),
               InlineKeyboardButton(text="🚨 Assistenza 🚨", url="http://t.me/AssistenzaAtlantisTradeCenterBot"),
               #split perchè canaleAste contiene il tag del canale con la @ davanti
               InlineKeyboardButton(text="📣 Canale 📣", url=f"http://t.me/{(secrets.canaleAste).split('@')[1]}"),
               InlineKeyboardButton("ℹ️ info ℹ️", callback_data="home/tastoInfo"))
    return markup

def infoMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📝 Regolamento 📝", url="https://telegra.ph/Regolamento-dellAtlantis-Trade-Center-ATC-09-07"))
    markup.add(InlineKeyboardButton("🏆 Funzionamento punti 🏆", url="https://telegra.ph/Funzionamento-dei-Punti-dellAtlantis-Trade-Center-ATC-09-07"))
    #Funzione momentaneamente disabilitata da abilitare quando aprirà il server. È già tutto pronto, basta rimuovere qui l'hashtag.
    #markup.add(InlineKeyboardButton("🛍 Ricevi punti gratis 🛍", callback_data="home/tastoInfo/tastoPuntoGratis"))
    markup.add(InlineKeyboardButton("🧑‍💻 Dev 🧑‍💻", url="http://t.me/Il_dive"))
    markup.add(InlineKeyboardButton("🏠 Torna alla home 🏠", callback_data="backToHomeBtn"))
    return markup

def puntiGratisMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✅ Ho fatto ✅", callback_data="home/tastoInfo/tastoPuntoGratis/hoFattoBtn"))
    markup.add(InlineKeyboardButton("🏠 Torna alla home 🏠", callback_data="backToHomeBtn"))
    return markup

def scegliModuloMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("💰 Vendita 💰", callback_data="home/tastoModulo/tastoModuloVendita"),
               InlineKeyboardButton("🔍 Cercasi 🔍", callback_data="home/tastoModulo/tastoModuloCercasi"))
    markup.add(InlineKeyboardButton("🔙 Indietro 🔙", callback_data="tastoModuloIndietro"))
    return markup


def tastoChiudiMessaggio():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("❌ Chiudi ❌", callback_data="tastoChiudiMessaggio"))
    return markup


def inviaModuloAlloStaff():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📣 Invia allo staff 📣", callback_data="tastoModuloVenditaInviaStaff"))
    markup.add(InlineKeyboardButton("🔙 Indietro 🔙", callback_data="tastoModuloIndietro"))
    return markup

def moduloInviatoMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✅ Inviato ✅", callback_data="tastoInviato"))
    return markup

def tastoBackToHome():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🏠 Torna alla Home 🏠", callback_data="backToHomeBtn"))
    return markup

def canaleAsteMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📣 canale 📣", url="https://t.me/AtlantisTradeCenter"))
    return markup

def offerteBotMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("💸 Bot offerte 💸", url="https://t.me/AssistenzaAtlantisTradeCenterBot"))
    return markup

def caricamento():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("⏳ Caricamento ⏳", callback_data="none"))
    return markup

def capitoMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("👍 Capito 👍", callback_data="capito"))
    return markup

def offriCustomStartUrlAsta(codiceModulo):
    #t.me/your_bot?start=XXXX
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("💰 Nessuna offerta 💰", callback_data="none"))
    markup.add(InlineKeyboardButton("💸 Offri 💸", url="https://t.me/AtlantisTradeCenterBot?start="+str(codiceModulo)))
    markup.add(InlineKeyboardButton("📄 Crea un modulo 📄", url="https://t.me/AtlantisTradeCenterBot"))
    return markup

def offriCustomStartUrlCercasi(codiceModulo):
    #t.me/your_bot?start=XXXX
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("💸 Ho l'oggetto 💸", url="https://t.me/AtlantisTradeCenterBot?start="+str(codiceModulo)))
    markup.add(InlineKeyboardButton("📄 Crea un modulo 📄", url="https://t.me/AtlantisTradeCenterBot"))
    return markup

def confermaPossesso(codiceModulo):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("💸 Conferma vendita 💸", callback_data="confermaPossessoN" + str(codiceModulo)))
    markup.add(InlineKeyboardButton("🔙 Chiudi 🔙", callback_data="tastoModuloIndietro"))
    return markup


def setOffertaMarkup(soldiOfferti, moduloID, isOrarioDaGenerare):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if isOrarioDaGenerare:
        orario = funzioniManager.aggiungi_un_ora()
    else:
        try:
            with open(f"orarioTermineAste/{moduloID}.txt", 'r') as file:
                orario = file.read()
        except:
            orario = funzioniManager.aggiungi_un_ora()

    try:
        markup.add(InlineKeyboardButton("💰 Offerti: " + str(funzioniManager.number_to_abbrev(int(soldiOfferti))) + " 💰", callback_data="none"),
            InlineKeyboardButton("⏳ Fine: " + str(orario) + " ⏳", callback_data="none"))
    except:
        markup.add(InlineKeyboardButton("💰 Offerti: " + str(funzioniManager.number_to_abbrev(soldiOfferti)) + " 💰", callback_data="none"),
               InlineKeyboardButton("⏳ Fine: " + str(orario) + " ⏳", callback_data="none"))
    markup.add(InlineKeyboardButton("💸 Offri 💸", url="https://t.me/AtlantisTradeCenterBot?start=" + str(moduloID)))
    markup.add(InlineKeyboardButton("📄 Crea un modulo 📄", url="https://t.me/AtlantisTradeCenterBot"))
    return markup

def setFineAstaMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("⏳ Asta terminata ⏳", callback_data="none"))
    markup.add(InlineKeyboardButton("📄 Crea un modulo 📄", url="https://t.me/AtlantisTradeCenterBot"))
    return markup

def setOggettoTrovato():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("📦 Oggetto trovato 📦", callback_data="none"))
    markup.add(InlineKeyboardButton("📄 Crea un modulo 📄", url="https://t.me/AtlantisTradeCenterBot"))
    return markup

def offertaAttualeMarkup(soldiOfferti, moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    if soldiOfferti is not None:
        #seconda offerta o più (rilancio)
        rilancioMinimo = int(funzioniManager.abbrev_to_number(soldiOfferti)) + int(funzioniManager.abbrev_to_number(funzioniManager.getRilancio(funzioniManager.getTextModulo(moduloID))))
        try:
            markup.add(InlineKeyboardButton("💰 Offerta attuale: " + str(funzioniManager.number_to_abbrev(int(soldiOfferti))) + " 💰", callback_data="none"))
        except:
            markup.add(InlineKeyboardButton("💰 Offerta attuale: " + str(funzioniManager.number_to_abbrev(soldiOfferti)) + " 💰", callback_data="none"))
        if not int(funzioniManager.abbrev_to_number(soldiOfferti)) >= int(funzioniManager.abbrev_to_number(funzioniManager.getCompraOra(funzioniManager.getTextModulo(moduloID)))):
            markup.add(InlineKeyboardButton(f"💲 Rilancia di {funzioniManager.number_to_abbrev(rilancioMinimo)} 💲", callback_data=f"rilancioMinimo#{moduloID}#{rilancioMinimo}"))
    else:
        #prima offerta
        offertaMinima = funzioniManager.getBaseAsta(funzioniManager.getTextModulo(moduloID))
        markup.add(InlineKeyboardButton("💰 Offerta attuale: 0 💰", callback_data="none"))
        markup.add(InlineKeyboardButton(f"💲 Offri {funzioniManager.number_to_abbrev(offertaMinima)} 💲", callback_data=f"rilancioMinimo#{moduloID}#{offertaMinima}"))
    markup.add(InlineKeyboardButton("🏦 Usa il Compra ora 🏦", callback_data="compraOra#" + str(moduloID)))
    markup.add(InlineKeyboardButton("🔙 Indietro 🔙", callback_data="tastoModuloIndietro"))
    return markup

def tastiEsitoModulo(chat_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("👤 User 👤", url="tg://user?id=" + str(chat_id)))
    markup.add(InlineKeyboardButton("✅ Approva ✅", callback_data="tastoModuloApprova"),
               InlineKeyboardButton("📝 Approva edit 📝", callback_data="tastoModuloApprovaEdit"))
    markup.add(InlineKeyboardButton("❌ Rifiuta ❌", callback_data="tastoModuloRifiuta"))
    return markup

def tastiRifiutaModulo(userUrl):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    try:
        if userUrl is not None:
            markup.add(InlineKeyboardButton("👤 User 👤", url=userUrl))
        else:
            markup.add(InlineKeyboardButton("👤 User non valido 👤", callback_data="none"))
            return markup
    except:
        markup.add(InlineKeyboardButton("👤 User non valido 👤", callback_data="none"))
        return markup
    markup.add(InlineKeyboardButton("Modulo incompleto", callback_data="tastoModuloRifiuta|incompleto"),
               InlineKeyboardButton("Poco interessante", callback_data="tastoModuloRifiuta|pocoInteressante"),
               InlineKeyboardButton("Prezzo non consono", callback_data="tastoModuloRifiuta|prezzoNonConsono"),
               InlineKeyboardButton("Altro", callback_data="tastoModuloRifiuta|altro"),
               InlineKeyboardButton("🔙 Indietro 🔙", callback_data="backToTastiEstioModulo"))
    return markup

def redirectPostCanale(message_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📣 Visualizza Post 📣", url="https://t.me/AtlantisTradeCenter/" + str(message_id)))
    return markup

def redirectPostCanaleTornaALlaHome(message_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("📣 Visualizza Post 📣", url="https://t.me/AtlantisTradeCenter/" + str(message_id)))
    markup.add(InlineKeyboardButton("🏠 Torna alla Home 🏠", callback_data="backToHomeBtn"))
    return markup

def offertaRegistrataMarkup(message_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("✅ Offerta registrata ✅", callback_data="-"))
    markup.add(InlineKeyboardButton("📣 Visualizza Post 📣", url="https://t.me/AtlantisTradeCenter/" + str(message_id)))
    return markup

def showUser(userUrl):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("👤 User 👤", url=userUrl))
    return markup

def visualizzaClientiCercasi(userUrl, moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    try:
        if userUrl is not None:
            markup.add(InlineKeyboardButton("👤 Venditore del cercasi 👤", url=userUrl))
        else:
            markup.add(InlineKeyboardButton("Compratore ID non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("Compratore ID non valido", callback_data="none"))
    try:
        if funzioniManager.getCreatoreModulo(moduloID) is not None:
            venditoreUrl = f"tg://user?id={funzioniManager.getCreatoreModulo(moduloID)}"
            markup.add(InlineKeyboardButton("👤 Cercatore 👤", url=venditoreUrl))
        else:
            markup.add(InlineKeyboardButton("Cercatore ID non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("Cercatore ID non valido", callback_data="none"))
    markup.add(InlineKeyboardButton("🗂 Scambio effettuato 🗂", callback_data=f"scambioEffettuato#{moduloID}"))
    return markup

def visualizzaClientiCompraOra(userUrl, moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    try:
        if userUrl is not None:
            markup.add(InlineKeyboardButton("👤 Compratore - compra ora 👤", url=userUrl))
        else:
            markup.add(InlineKeyboardButton("Compratore ID non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("Compratore ID non valido", callback_data="none"))
    try:
        if funzioniManager.getCreatoreModulo(moduloID) is not None:
            venditoreUrl = f"tg://user?id={funzioniManager.getCreatoreModulo(moduloID)}"
            markup.add(InlineKeyboardButton("👤 Venditore 👤", url=venditoreUrl))
        else:
            markup.add(InlineKeyboardButton("Venditore ID non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("Venditore ID non valido", callback_data="none"))
    markup.add(InlineKeyboardButton("🗂 Scambio effettuato 🗂", callback_data=f"scambioEffettuato#{moduloID}"))
    return markup

def visualizzaClientiAstaTerminata(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    offerenteChatID = funzioniManager.getOfferente(moduloID)
    try:
        if offerenteChatID is not None:
            urlOfferente = f"tg://user?id={offerenteChatID}"
            markup.add(InlineKeyboardButton("👤 Compratore 👤", url=urlOfferente))
        else:
            markup.add(InlineKeyboardButton("Compratore ID non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("Compratore ID non valido", callback_data="none"))
    try:
        creatoreModuloChatID = funzioniManager.getCreatoreModulo(moduloID)
        if creatoreModuloChatID is not None:
            venditoreUrl = f"tg://user?id={creatoreModuloChatID}"
            markup.add(InlineKeyboardButton("👤 Venditore 👤", url=venditoreUrl))
        else:
            markup.add(InlineKeyboardButton("Venditore ID non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("Venditore ID non valido", callback_data="none"))
    markup.add(InlineKeyboardButton("🗂 Scambio effettuato 🗂", callback_data=f"scambioEffettuato#{moduloID}"))
    return markup

def contattaAssistenzaMarkup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🚨 Assistenza 🚨", url="https://t.me/AssistenzaAtlantisTradeCenterBot"))
    markup.add(InlineKeyboardButton("🏠 Torna alla Home 🏠", callback_data="backToHomeBtn"))
    return markup

def assistenzaMarkupSenzaHome():
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("🚨 Assistenza 🚨", url="https://t.me/AssistenzaAtlantisTradeCenterBot"))
    return markup

def manageModuloStaff(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    tipoModulo = funzioniManager.getTextModulo(moduloID).split("🐬")[1].strip().split(" ")[0].lower()
    if tipoModulo == "asta":
        markup.add(InlineKeyboardButton("⚙️ Ultima offerta ⚙️", callback_data="ultima_offerta#" + str(moduloID)))
    elif tipoModulo == "cercasi" and funzioniManager.getIsTerminata(moduloID) is True:
        markup.add(InlineKeyboardButton("⚙️ Torna disponibile ⚙️", callback_data="tornaDisponibileCercasi#" + str(moduloID)))
    markup.add(InlineKeyboardButton("⚙️ Ultimo offerente ⚙️", callback_data="ultimo_offerente#" + str(moduloID)),
               InlineKeyboardButton("⚙️ Testo ⚙️", callback_data="testo#" + str(moduloID)),
               InlineKeyboardButton("⚙️ Message id ⚙️", callback_data="message_id#" + str(moduloID)))
    urlUser = f"tg://user?id={funzioniManager.getCreatoreModulo(moduloID)}"
    try:
        markup.add(InlineKeyboardButton("👤 creatore modulo 👤", url=urlUser))
    except:
        markup.add(InlineKeyboardButton("👤 id creatore non valido 👤", callback_data="none"))
    if funzioniManager.getIsTerminata(moduloID) is False:
        markup.add(InlineKeyboardButton("⏱ Termina ⏱", callback_data="termina#" + str(moduloID)))
    else:
        markup.add(InlineKeyboardButton("⏱ Terminata ⏱", callback_data="none"))

    markup.add(InlineKeyboardButton("🔙 Chiudi 🔙", callback_data="tastoChiudiElimina"))
    return markup



def manageModuloUltimaOffertaStaff(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if funzioniManager.getOfferta(moduloID) is not None:
        markup.add(InlineKeyboardButton("📝 Set 📝", callback_data="setNew_ultima_offerta#" + str(moduloID)),
                   InlineKeyboardButton("🔄 Reset 🔄", callback_data="reset_ultima_offerta#" + str(moduloID)))
    else:
        markup.add(InlineKeyboardButton("📝 Set 📝", callback_data="setNew_ultima_offerta#" + str(moduloID)))

    markup.add(InlineKeyboardButton("🔙 Manage 🔙", callback_data="tastoBackManage#" + str(moduloID)))
    return markup


def manageModuloUltimoOfferenteStaff(moduloID, ultimoOfferenteUrl):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    if funzioniManager.getOfferente(moduloID) is not None:
        markup.add(InlineKeyboardButton("📝 Set 📝", callback_data="setNew_ultimo_offerente#" + str(moduloID)),
                   InlineKeyboardButton("🔄 Reset 🔄", callback_data="reset_ultimo_offerente#" + str(moduloID)))
    else:
        markup.add(InlineKeyboardButton("📝 Set 📝", callback_data="setNew_ultimo_offerente#" + str(moduloID)))

    try:
        # Prova ad aggiungere il pulsante "👤 User 👤" solo se ultimoOfferenteUrl non è None
        if ultimoOfferenteUrl is not None:
            markup.add(InlineKeyboardButton("👤 User 👤", url=ultimoOfferenteUrl))
        else:
            markup.add(InlineKeyboardButton("User non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("User non valido", callback_data="none"))

    markup.add(InlineKeyboardButton("🔙 Manage 🔙", callback_data="tastoBackManage#" + str(moduloID)))
    return markup

def manageModuloTextStaff(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("📝 Set 📝", callback_data="setNew_moduloText#" + str(moduloID)))
    markup.add(InlineKeyboardButton("🔙 Manage 🔙", callback_data="tastoBackManage#" + str(moduloID)))
    return markup

def manageModuloMessageIDStaff(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("📝 Set 📝", callback_data="setNew_moduloMessageID#" + str(moduloID)))
    markup.add(InlineKeyboardButton("🔙 Manage 🔙", callback_data="tastoBackManage#" + str(moduloID)))
    return markup

def ultimoOfferente(ultimoOfferenteUrl):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    try:
        # Prova ad aggiungere il pulsante "👤 User 👤" solo se ultimoOfferenteUrl non è None
        if ultimoOfferenteUrl is not None:
            markup.add(InlineKeyboardButton("👤 User 👤", url=ultimoOfferenteUrl))
        else:
            markup.add(InlineKeyboardButton("User non valido", callback_data="none"))
    except Exception:
        # Se si verifica un errore, è perchè dice che l'url non è valido --> quindi l'user id non è valido
        markup.add(InlineKeyboardButton("User non valido", callback_data="none"))


def backToManageModulo(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("🔙 Manage 🔙", callback_data="tastoBackManage#" + str(moduloID)))
    return markup

def confermaTerminaAsta(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("⏱ Termina ⏱", callback_data="tastoTerminaAsta#" + str(moduloID)),
               InlineKeyboardButton("🚨 Bot assistenza 🚨", url="http://t.me/AssistenzaAtlantisTradeCenterBot"))
    return markup