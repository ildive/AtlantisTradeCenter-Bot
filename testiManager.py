import datetime
import json

import funzioniManager


def testoSponsor(chat_id):
    if funzioniManager.getAggiungi7Giorni(chat_id) is not False and funzioniManager.getAggiungi7Giorni(chat_id) is not False:
        giorni = funzioniManager.getAggiungi7Giorni(chat_id)
        mese = datetime.datetime.now().month
        with open("sponsorUsers.json", 'r') as file:
            users = json.load(file)
            ora = users.get(str(chat_id), {}).get("ora",0)
            text = f"""
🌟 Registrazione Avvenuta con Successo! 🌟
        
Ciao! Ti confermiamo che la tua registrazione per guadagnare 2 punti ATC con l'hashtag #AtlantisTradeCenter è stata completata con successo. 😊
    
Adesso tutto ciò che devi fare è mantenere l'hashtag nel tuo 'first_name' per una settimana consecutiva. Non appena avrai completato questa semplice sfida, riceverai automaticamente 2 punti ATC come nostro ringraziamento.
    
<b>Il giorno {giorni}/{mese} alle ore {ora}:00</b>, i punti saranno tuoi. Continua a essere parte attiva della nostra community e grazie per il tuo sostegno! 🌟 """
    return text