import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

import funzioniManager

from secrets import *

bot = telebot.TeleBot(token, parse_mode="HTML")

def accettaRichiestaRecensioneMarkup(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("💫 Lascia recensione ✨", callback_data=f"tastoLasciaRecensione#{moduloID}"))
    return markup

def chiediRecensioneClienti(moduloID):
    creatore = funzioniManager.getCreatoreModulo(moduloID)
    offerente = funzioniManager.getOfferente(moduloID)
    text = f"🌟 Ciao! Speriamo tu abbia avuto un'ottima esperienza con noi 🌟\nSe potessi, ti preghiamo di lasciare una breve recensione riguardante il Modulo #{moduloID} cliccando il tasto qui sotto.\nSarà molto apprezzata! 🙏"
    try:
        bot.send_message(creatore, text, reply_markup=accettaRichiestaRecensioneMarkup(moduloID))
    except:
        pass
    try:
        bot.send_message(offerente, text, reply_markup=accettaRichiestaRecensioneMarkup(moduloID))
    except:
        pass

def recensioneMarkup(moduloID):
    markup = InlineKeyboardMarkup()
    markup.row_width = 5
    markup.add(InlineKeyboardButton("Stelle", callback_data=moduloID))
    markup.add(InlineKeyboardButton("⭐️", callback_data="stellaRecensione1"),
               InlineKeyboardButton("⭐️", callback_data="stellaRecensione2"),
               InlineKeyboardButton("⭐️", callback_data="stellaRecensione3"),
               InlineKeyboardButton("⭐️", callback_data="stellaRecensione4"),
               InlineKeyboardButton("⭐️", callback_data="stellaRecensione5"))
    return markup
