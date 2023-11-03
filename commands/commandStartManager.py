import json
import telebot
import fileManager
import os

bot = telebot.TeleBot("<TOKEN>")


def checkRegistrazione(message):
    print("arrivato")
    # L'utente non è nel file
    file_path = "users.json"
    chat_id = message.chat.id

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    if not fileManager.checkUserInList(chat_id, users):
        users[str(chat_id)] = {'punti': 0,
                               'warn': 0,
                               'isBanned': False}

        with open('users.json', 'w') as file:
            json.dump(users, file, indent=4)
