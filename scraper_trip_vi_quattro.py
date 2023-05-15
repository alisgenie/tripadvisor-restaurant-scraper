# 03/02/2023 - Script Python per scaricare tutte le recensioni di un ristorante da TripAdvisor(FUNZIONA SOLO SU TRIPADVISOR IT)
#ore di lavoro = 6 +
# ========ISTRUZIONI PER IL FUNZIONAMENTO==============

# Per far funzionare questo codice installa le librerie(anche detti moduli) python requests e bs4
# digitando nel terminale le seguenti righe
# pip install -U requests
# pip install -U bs4

# Cosa manca ancora a questo codice?
#   - selezionare l'indirizzo
#   - selezionare quante persone lo hanno trovato utile
#   - plus: selezionare i dati di ogni recensitore e magari classificarne l'affidabilità

import requests
from bs4 import BeautifulSoup
import time
import re



#=================▼▼▼▼▼▼=====VARIABILI CHE PUO' MODIFICARE L'UTENTE=======▼▼▼▼▼▼=====================


# prima pagina delle recensioni del ristorante di interesse
# link del seguente tipo:  Restauran_Review ▼▼▼▼▼▼           Reviews   ▼▼▼▼▼▼   nome ristorante ▼▼▼▼▼▼ (la prima pagina senza -or nel link)
#url = "https://www.tripadvisor.it/Restaurant_Review-g187807-d17382076-Reviews-Le_Delizie_Gourmet-Rimini_Province_of_Rimini_Emilia_Romagna.html"

url = "https://www.tripadvisor.it/Restaurant_Review-g1187205-d2477694-Reviews-Terrazza-Rivazzurra_Rimini_Province_of_Rimini_Emilia_Romagna.html"

# numero di recensioni desiderate, se 0 scarica tutte le recensioni di un ristorante dalla piu recente
num = 0
# nome del file in cui vuoi salvare le recensioni, (verrà creato nella stessa cartella di questo file python)
file_name = "reviews.csv"


#====================▲▲▲▲▲▲====VARIABILE CHE PUO' MODIFICARE L'UTENTE========▲▲▲▲▲▲===================


def scrape_trip( url: str,num : int,file_name : str):


    #PRIMA CHIAVE DELL'INGHIPPO cambiare il parametro 'User-Agent':
    #io ho aperto il link https://www.whatsmyua.info/   per selezionare l'user agent del broswer da cui navigo di solito
    #meglio metterci l'user agent locale non so se questo è collegato direttamente al mio computer
    #                                              ▼ ▼ ▼
    #     response = requests.get(url, headers= {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0"})
    response = requests.get(url, headers= {'User-Agent': "Mozilla/5.0"})
    if response.status_code == 200:
        print("Success: Page Downloaded")
    else:
        print("ci sono degli errori")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    reviews_count = int(soup.find('span', class_='reviews_header_count').text.strip('()'))
    if (num==0):
        num = int(reviews_count/10)
    else:
        num = int(num/10)

    

    # variabile in secondi per monitorare il tempo totale impiegato
    start_time = time.time()

    try:
        with open(file_name, 'w', encoding='UTF-8') as f:

            f.write(f"stars,date,comment\n")

    except Exception as e:
        print('errore durante l\'elaborazione del file', e)
        return
    #preparo l'url per le pagine seguenti
    url = url.replace("-Reviews-", f"-Reviews-or00-")

    #il ciclo for reitera fino a num-1 compreso
    for n in range(0, num):        


        soup = BeautifulSoup(response.text, 'html.parser')


    # https://automatetheboringstuff.com/2e/chapter12/#calibre_link-390
    #        selettore css          ▼ ▼ ▼ ▼ ▼
        comments = soup.select("div.review-container")

        try:
            with open(file_name, 'a', encoding='UTF-8') as f:

                for com in comments:
                
                    com = str(com)
                    soup = BeautifulSoup(com, 'html.parser')

                #Prendiamo le stelline
                    stars = soup.select("div.review-container span.ui_bubble_rating")
                    stars = str(stars)
                    stars = re.search(r'\d+', stars).group().strip("0")

                #prendiamo la data

                    date = soup.find('span', class_='ratingDate')['title']


                #prendiamo il commento
                    com = soup.select('p')
                    com = com[0].text.replace("\n"," ")
                    f.write(f"{stars},{date},{com}\n")

        except Exception as e:
            print('errore durante l\'elaborazione del file', e)


    # pausa di 3 secondi per simulare il comportamento umano, e anche così c'è il rischo che veniamo bloccati
        time.sleep(2)


        now = time.time()
        print(f"\n\nCommenti importati dalla pagina {n+1}.  {round(now-start_time,2)} secondi trascorsi.")
        
        url = url.replace(f"-Reviews-or{n}0-", f"-Reviews-or{n+1}0-")
        response = requests.get(url, headers= {'User-Agent': "Mozilla/5.0"})
        if response.status_code == 200:
            print(f"Success: Page {n+2} Downloaded")
            print("from: ", url)
            
        else:
            print(f"problema ad importare la pagina {n+1}")
            break
        
        

    print(f"\n\nHai impiegato {round(time.time()-start_time,2)} secondi.")



# scrape_trip(url,num,file_name)