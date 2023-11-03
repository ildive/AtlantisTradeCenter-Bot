import telebot

bot = telebot.TeleBot("6694548358:AAEyP9jRmRLl65dhVGJk_tXAsScUIJr00Vk", parse_mode="HTML")

def sendErrorModuloNonTrovato(chat_id):
    bot.send_message(chat_id, "C'è stato un'errore. Contatta l'assistenza cliccando qui sotto")