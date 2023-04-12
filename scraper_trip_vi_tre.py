# 03/02/2023 - Script Python per scaricare tutte le recensioni di un ristorante da TripAdvisor(FUNZIONA SOLO SU TRIPADVISOR IT)
#ore di lavoro = 6 +
# ========ISTRUZIONI PER IL FUNZIONAMENTO==============

# Per far funzionare questo codice installa le librerie(anche detti moduli) python requests e bs4
# digitando nel terminale le seguenti righe
# pip install -U requests
# pip install -U bs4

# Cosa manca ancora a questo codice?
#   - selezionare anche la data associata ad ogni elemento
#   - selezionare le stelline attribuitegli
#   - selezionare quante persone lo hanno trovato utile
#   - plus: selezionare i dati di ogni recensitore e magari classificarne l'affidabilità

import requests
from bs4 import BeautifulSoup
import time




#=================▼▼▼▼▼▼=====VARIABILI CHE PUO' MODIFICARE L'UTENTE=======▼▼▼▼▼▼=====================


# prima pagina delle recensioni del ristorante di interesse
# link del seguente tipo:  Restauran_Review ▼▼▼▼▼▼           Reviews   ▼▼▼▼▼▼   nome ristorante ▼▼▼▼▼▼ (la prima pagina senza -or nel link)
#url = "https://www.tripadvisor.it/Restaurant_Review-g187807-d17382076-Reviews-Le_Delizie_Gourmet-Rimini_Province_of_Rimini_Emilia_Romagna.html"

url = "https://www.tripadvisor.it/Restaurant_Review-g187807-d17382076-Reviews-Le_Delizie_Gourmet-Rimini_Province_of_Rimini_Emilia_Romagna.html"

# numero pagine delle recensioni
num = 12

# nome del file in cui vuoi salvare le recensioni, (verrà creato nella stessa cartella di questo file python)
file_name = "recensioni.txt"


#====================▲▲▲▲▲▲====VARIABILE CHE PUO' MODIFICARE L'UTENTE========▲▲▲▲▲▲===================








# variabile in secondi per monitorare il tempo totale impiegato
start_time = time.time()

# contatore per il numero delle recensioni
count = 1

for n in range(-1, num):
    if n > -1:
        url = url.replace("-Reviews-", f"-Reviews-or{n}0-")


#PRIMA CHIAVE DELL'INGHIPPO cambiare il parametro 'User-Agent':
#io ho aperto il link https://www.whatsmyua.info/   per selezionare l'user agent del broswer da cui navigo di solito
#meglio metterci l'user agent locale non so se questo è collegato direttamente al mio computer
#                                              ▼ ▼ ▼
#     response = requests.get(url, headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"})
    response = requests.get(url, headers= {'User-Agent': "Mozilla/5.0"})
    if response.status_code == 200:
        print("Success: Page Downloaded")
    else:
        break


    soup = BeautifulSoup(response.text, 'html.parser')

# SECONDA CHIAVE DELL'INGHIPPO inserire il giusto css selector, per capirlo è necesssaria
# conoscere la logica dietro alle pagine web (html,css), uno spunto:
# https://automatetheboringstuff.com/2e/chapter12/#calibre_link-390
#        selettore css          ▼ ▼ ▼ ▼ ▼
    items = soup.select("div.review-container p")

    try:
        with open(file_name, 'a', encoding='UTF-8') as f:
            for i in items:

                print(f"\n\n\n===================Recensione numero {count}==================================\n\n")
                count = count + 1
                print(i.text)

                f.write(f"\n\n\n\n====Recensione numero {count}\n\n")
                f.write(i.text)

    except Exception as e:
        print('errore durante l\'elaborazione del file', e)


# pausa di 3 secondi per simulare il comportamento umano, e anche così c'è il rischo che veniamo bloccati
# per un comportamento tanto preciso, si possono aggiungere delle pause causali random entro un certo range
#se vai di fretta puoi provare a togliere totalmente la pausa o ad abbassarla, non ho provata
    time.sleep(3)

print(f"\n\nHai impiegato {round(time.time()-start_time,2)} secondi.")

