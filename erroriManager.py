import telebot

bot = telebot.TeleBot("<TOKEN>", parse_mode="HTML")

def sendErrorModuloNonTrovato(chat_id):
    bot.send_message(chat_id, "C'è stato un'errore. Contatta l'assistenza cliccando qui sotto")
