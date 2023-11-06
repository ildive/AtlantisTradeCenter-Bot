import os
from datetime import datetime, timedelta
import json

contaSpam = {}

def abbrev_to_number(abbrev_str):
    # Rimuovi eventuali spazi bianchi e converti la stringa in maiuscolo
    if abbrev_str is not None:
        abbrev_str = abbrev_str.strip().lower()

        # Verifica se la stringa termina con "K"
        if abbrev_str.endswith("k"):
            try:
                # Estrai il valore numerico prima della "K"
                num_str = abbrev_str[:-1]

                # Rimuovi eventuali spazi all'interno della stringa numerica
                num_str = num_str.replace(" ", "")

                num_str = num_str.replace(",", ".")

                num_value = float(num_str)

                # Moltiplica per 1000 per ottenere il valore completo
                full_value = int(num_value * 1000)
                return full_value
            except ValueError:
                pass
    return abbrev_str

def number_to_abbrev(number):
    if isinstance(number, int):
        if number >= 1000:
            # Calcola il valore abbreviato
            abbrev_value = number / 1000

            # Verifica se la parte decimale è zero
            if abbrev_value.is_integer():
                # Se la parte decimale è zero, formatta il risultato senza ".0"
                abbrev_str = f"{int(abbrev_value)}k"
            else:
                # Altrimenti, formatta il risultato con una cifra decimale
                abbrev_str = f"{abbrev_value:.1f}k"

            return abbrev_str
        else:
            # Se il numero è inferiore a 1000, restituisci il numero stesso come stringa
            return str(number)
    else:
        return str(number)


def messageTextToModuloID(text):
    try:
        moduloID = text.split("Modulo #")[1].split("\n")[0]
    except:
        moduloID = text.split("modulo #")[1].split("\n")[0]
    return moduloID

def getTextModulo(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("text", None)
    except FileNotFoundError:
        return None

def getOfferta(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("ultima_offerta", None)
    except FileNotFoundError:
        return None

def getOfferente(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("ultimo_offerente", None)
    except FileNotFoundError:
        return None

def getMessageID(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("message_id", None)
    except FileNotFoundError:
        return None

def getStafferModulo(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("stafferModulo", None)
    except FileNotFoundError:
        return None

def getPhotoBool(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("photo", None)
    except FileNotFoundError:
        return None

def getIsTerminata(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("isTerminata", None)
    except FileNotFoundError:
        return None

def getCreatoreModulo(moduloID):
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            return data.get("creatoreModulo", None)
    except FileNotFoundError:
        return None

def setIsTerminata(moduloID, isTerminataBool):
    if isTerminataBool:
        try:
            os.remove(f"orarioTermineAste/{moduloID}.txt")
        except:
            pass
    try:
        with open(f"messaggiPostatiCanale/{moduloID}.txt", "r", encoding="utf-8") as file:
            data = json.load(file)
            # Aggiorna il parametro 'creatoreModulo' con il nuovo creatore
            data["isTerminata"] = isTerminataBool

        with open(f"messaggiPostatiCanale/{moduloID}.txt", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return True
    except FileNotFoundError:
        return False



def getBaseAsta(textAsta):
    baseAsta = str(textAsta).split("🪙 Base asta:")[1].split("\n")[0]
    return baseAsta

def getRilancio(textAsta):
    rilancioAsta = str(textAsta).split("💵 Rilancio:")[1].split("\n")[0]
    return rilancioAsta

def getCompraOra(textAsta):
    compraOra = str(textAsta).split("🏦 Compra ora:")[1].split("\n")[0]
    return compraOra

def aggiungiUnOraAsta(moduloID):
    #aggiungi scadenza
    orarioUnOra = datetime.now() + timedelta(hours=1)
    with open("orarioTermineAste/" + str(moduloID) + ".txt", "w") as file:
        file.write(f"{orarioUnOra.hour}:{orarioUnOra.minute}")
        file.close()

def getTextFromModuloID(modulo_id):
    try:
        with open(f"messaggiPostatiCanale/{modulo_id}.txt", "r", encoding="utf-8") as file:
            return json.load(file).get("text", None)
    except FileNotFoundError:
        return None

def getModuloIdFromMessageId(message_id):
    modulo_id = None
    directory = "messaggiPostatiCanale"

    try:
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                file_path = os.path.join(directory, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    fileMessage_id = json.load(file).get("message_id", None)
                    if str(fileMessage_id) == str(message_id):
                        modulo_id = str(filename)
                        break  # Esci dal ciclo quando trovi il modulo
        return modulo_id
    except FileNotFoundError:
        return None


def aggiungi_un_ora():
    current_time = datetime.now()
    updated_time = current_time + timedelta(hours=1)
    return updated_time.strftime('%H:%M')

def getAggiungi7Giorni(chat_id):
    with open("sponsorUsers.json", 'r') as file:
        try:
            users = json.load(file)
            giorno = users.get(str(chat_id), {}).get("giornoInizio", 0)

        except json.JSONDecodeError:
            return False
    updated_time = timedelta(days=giorno) + timedelta(days=7)
    return updated_time.days

def getOre(chat_id):
    with open("sponsorUsers.json", 'r') as file:
        try:
            users = json.load(file)
            giorno = users.get(str(chat_id), {}).get("giornoInizio", 0)

        except json.JSONDecodeError:
            return False
    updated_time = timedelta(days=giorno) + timedelta(days=7)
    return updated_time.days

def antiSpam(chat_id, moduloID):
    if chat_id in contaSpam:
        # se funziona si lascia così (scherzo, questa seconda comparazione serve a evitare che, se voglio offrire a 2 moduli differenti\n
        # ...quindi cliccando start a 1 minuto di differenza tra un'offerta e l'altra, non mi mostri l'offerta continuandomi a cancellare /start
        if str(contaSpam[chat_id]) == str(moduloID):
            return False

    contaSpam[chat_id] = moduloID
    return True

def rimuoviAntiSpam(chat_id):
    try:
        contaSpam.pop(chat_id)
    except:
        pass

