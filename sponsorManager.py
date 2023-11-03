import datetime
import json
import os

import telebot

import fileManager

bot = telebot.TeleBot("6694548358:AAEyP9jRmRLl65dhVGJk_tXAsScUIJr00Vk", parse_mode="HTML")

def checkUserSponsor(chat_id):
    path = "sponsorUsers.json"

    if os.path.exists(path):
        with open(path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    if str(chat_id) in users:
        return True
    else:
        return False

def aggiungiUserSponsor(chat_id):
    path = "sponsorUsers.json"

    if os.path.exists(path):
        with open(path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    if not str(chat_id) in users:
        users[str(chat_id)] = {'giornoInizio': datetime.datetime.now().day,
                               'ora': datetime.datetime.now().hour}
        with open(path, 'w') as file:
            json.dump(users, file, indent=4)


def rimuoviUserSponsor(chat_id):
    path = "sponsorUsers.json"

    if os.path.exists(path):
        with open(path, "r") as file:
            try:
                users = json.load(file)
            except json.JSONDecodeError:
                users = {}
    else:
        users = {}

    if str(chat_id) in users:
        del users[str(chat_id)]  # Rimuovi l'utente dalla lista

        # Sovrascrivi il file con l'elenco aggiornato degli utenti
        with open(path, 'w') as file:
            json.dump(users, file, indent=4)
