import json
from datetime import datetime
import os

import telebot

import markupManager
import moduliManager
import sponsorManager

twoTimesClickScambio = []

bot = telebot.TeleBot("<TOKEN>", parse_mode="HTML")

def checkFineAsta():
    now = datetime.now()
    directory_path = "orarioTermineAste"
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                if file.read() == f"{now.hour}:{now.minute}":
                    #ora puoi fare tutto quello che vuoi
                    moduloID = filename.split(".txt")[0]
                    print(f"il modulo #{moduloID} è scaduto")
                    file.close()
                    moduliManager.avvisaTermineAsta(moduloID, file_path)
    twoTimesClickScambio.clear()

def checkUtentiSponsor():
    path = 'sponsorUsers.json'
    if os.path.exists(path):
        with open(path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    for user in users:
        if not bot.get_chat(user).first_name.lower().__contains__("#atlantistradecenter"):
            #se non contiene l'hashtag
            try:
                bot.send_message(user, "<b>Ci dispiace tanto che hai smesso di utilizzare il nostro hashtag</b> #AtlantisTradeCenter. Ti abbiamo sempre apprezzato qui e speriamo che tu possa continuare a far parte della nostra community. Il tuo contributo è importante per noi! 😊🌟\n<b>Se desideri riprovare a utilizzare l'hashtag, sei più che benvenuto.</b> Sarà un piacere ricompensarti per il tuo impegno!", reply_markup=markupManager.tastoBackToHome())
                sponsorManager.rimuoviUserSponsor(user)
            except:
                pass
