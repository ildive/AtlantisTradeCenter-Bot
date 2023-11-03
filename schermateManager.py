import telebot
#import botTextManager as btm
import fileManager
import markupManager as mrkp

bot = telebot.TeleBot("<TOKEN>", parse_mode='html')
permessoInvioModuloChatId = []

#questa è la funzione che mostra all'utente la schermata home.
def showHome(chat_id):
    logoATC_image = open('logo ATC.png', 'rb')
    bot.send_photo(chat_id, logoATC_image, "🏠 Home 🏠\n\n🆕 I tuoi Punti: " + str(fileManager.getPoint(chat_id)) + " 🆕", reply_markup=mrkp.homeMarkup())
    logoATC_image.close()

def setInvioModulo(chat_id, bool):
    try:
        if bool:
            permessoInvioModuloChatId.append(chat_id)
        else:
            permessoInvioModuloChatId.remove(chat_id)
    except:
        pass

def canSendModulo(chat_id):
    if chat_id in permessoInvioModuloChatId:
        return True
    else:
        return False


#illumina il commercio
#la torcia dei tuoi affari
#la luce del commercio
