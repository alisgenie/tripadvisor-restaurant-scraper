
stop_list=[]
car_speciali=[]




with open('./assets/caratteri_speciali.txt', 'r', encoding='utf-8') as f:

    for r in f:
        car_speciali.extend(r.split("\n"))
        car_speciali.pop()


with open('./assets/my_stop_words.txt', 'r', encoding='utf-8') as f:

    for r in f:
        stop_list.extend(r.split("\n"))
        stop_list.pop()

#print(stop_list)
#print(car_speciali)


def clean(testo:str):

    testo = testo.lower()
    testo = " " + testo + " "
    testo = testo.replace("\n", "\n ")

    for x in car_speciali:

        if x in testo:
            testo = testo.replace(x, " ")


    ##utilizzare il codice in basso se voglio pulire il testo da una variabile string
    for x in stop_list:
        a = " " + x + " "

        if a in testo:
            testo = testo.replace(a, " ")
    
    return testo

