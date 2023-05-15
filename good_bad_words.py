# Questo è uno script per individuare le parole più usate nelle recensioni positive o negative 
# ai Ristoranti su TripAdvisor

# Saranno considerate negative le parole più frequenti dalle 1 a 3 stelline e negative quelle dalle 4 alle 5
# sarà eliminata da entrambi gli insiemi la loro intersezione.


from scraper_trip_vi_quattro import scrape_trip as scrape
from clean_text import clean

url = "https://www.tripadvisor.it/Restaurant_Review-g187801-d10450049-Reviews-Fourghetti-Bologna_Province_of_Bologna_Emilia_Romagna.html#REVIEWS"
file_name = "reviews.csv"

scrape(url,10, file_name)

bad_comments_l = []
good_comments_l = []
with open(file_name, 'r', encoding='UTF-8') as f:
    f.readline()

    for line in f:
        
        line = line.strip("\n")
        line = line.split(",")
        comment = line[2]
        comment = clean(comment)
        stars = int(line[0])
        if stars < 4:
            bad_comments_l.append(comment)
        else:
            good_comments_l.append(comment)

# print (good_comments_l)
# print (bad_comments_l)


def freq_word(target_comments:str, other_comments:str,output_file:str):

    l_parole = []
    l_altre_parole = []
    d_parole = {}
    for x in target_comments:
        l_parole.extend(x.split())
    for x in other_comments:
        l_altre_parole.extend(x.split())


    parole_uniche = set(l_parole)
    altre_parole_uniche = set (l_altre_parole)
    parole_uniche = parole_uniche - altre_parole_uniche
    del altre_parole_uniche
    parole_uniche = list(parole_uniche)
    parole_uniche.sort()
    print(type(parole_uniche))

    #mi dimentico spesso, che per esempio
    d_parole = d_parole.fromkeys(parole_uniche)


    for key in d_parole:
        d_parole[key] = l_parole.count(key)


    word_freq = []
    for key, value in d_parole.items():
        word_freq.append((value, key))
    word_freq.sort(reverse=True)

    with open(output_file, 'w', encoding='utf-8') as f:
        for x in word_freq:
            f.write(f'{x[0]} frequenze per {x[1]}\n')

    return word_freq





bad_frequency = freq_word(bad_comments_l, good_comments_l,"bad_words.txt")
good_frequency = freq_word(good_comments_l, bad_comments_l,"good_words.txt")
print(good_frequency)
# print(bad_frequency)
