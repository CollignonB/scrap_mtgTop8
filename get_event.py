from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from urllib.request import urlopen
import re

import datetime

base_url = "https://www.mtgtop8.com/"

page = urlopen(base_url)
html = page.read().decode("latin-1")
soup = BeautifulSoup(html, "html.parser")

file_path = "C:/Users/Utilisateur/Documents/python/web_scrp_mtg/mtgtop8.json"
if os.path.isfile(r"C:\Users\Utilisateur\Documents\python\web_scrp_mtg\mtgtop8.json"):
    # récupération de la date de dernière création du json,                        retrait de l'heure, changement de format
    date_last_update = datetime.datetime.fromtimestamp(os.path.getmtime(file_path)).date()
else :
    date_last_update = datetime.date(year= 2024, month= 10, day= 3)
# passage par une regex car l'utilisation de del est moche
# pattern de regex pour trouver les urls
pattern = 'format?.*?>'
links = re.findall(pattern, html, re.IGNORECASE)
format_urls = [] # liste des urls de tout les formats du site

# creation des urls completes + ajout dans la liste format_urls
for link in links :
    format_urls.append(base_url + link[:-1])

# listes des formats suivis avec leur url récupéré sur le site /!\ pas stable si changement sur le site
followed_format = {"STANDARD" : format_urls[8], "PIONEER" : format_urls[9], "MODERN" : format_urls[10], "DUEL COMMANDER" : format_urls[15]}

page = urlopen(followed_format["STANDARD"])
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

list_of_events = soup.find_all("td")[1]


events_inforamtion = []
re_url_event = '"ev.*?"' #regex qui va recupérer l'url de l'envent
re_name_event = 'f=[A-Z]{2,3}">.*?</a' #regex qui va récuéprer le nom de l'event  [A-Z]{2,3}?".*?</a
re_date_event = '12%">.*?</' # regex qui va récupérer la date de l'event

event_url = []  # liste des urls des évenements
event_name = [] # liste des noms des évenements
event_date = [] # liste des dates des évenements

for row in list_of_events.findAll('tr', {"class"  : "hover_tr"}):
    events_inforamtion.append(str(row.findAll('td')).split(",")[1::2])

    # récupération des balises utilent dans le code html
    important = str(row.findAll('td')).split(",")

    date_of_event = re.search(re_date_event, str(important), re.IGNORECASE).group()[5:-2]

    temp_date = datetime.date(year=int(f'20{date_of_event[-2:]}'), month=int(date_of_event[3:5]), day=int(date_of_event[:2]))

    # récuperation de la date de l'évenement
    if temp_date >= date_last_update:

        foramted_date = datetime.datetime.strptime(date_of_event,"%d/%m/%y")

        event_date.append((foramted_date))

        event_url.append(f"{base_url}{re.search(re_url_event, str(important), re.IGNORECASE).group()[1:-1]}&switch=text") 

        # recupération du nom de l'evenement
        if format != "EDH":
            # print(re.search(re_name_event, str(important), re.IGNORECASE).group()[6:-3])
            event_name.append(re.search(re_name_event, str(important), re.IGNORECASE).group()[6:-3])
        else:
            event_name.append(re.search(re_name_event, str(important), re.IGNORECASE).group()[7:-3])


# création d'un dictionnaire pour créer le Dataframe

dict = {'name' : event_name, 'url' : event_url, 'date' : event_date}



if not dict['name']: 
    print("le dictionnaire est vide")
else:
    if os.path.isfile(r"C:\Users\Utilisateur\Documents\python\web_scrp_mtg\mtgtop8.json"):
        list_of_event = pd.read_json("mtgtop8.json", orient="index")
    
        evenement = pd.concat([pd.DataFrame(dict), list_of_event])
    else:
        evenement = pd.DataFrame(dict)
    # pd.to_datetime(evenement['date']).apply(lambda x: x.date())
    evenement = evenement.sort_values(by=['date'], ascending = False).drop_duplicates().reset_index(drop=True)
    # evenement['date'] = pd.to_datetime(evenement['date'], format="%Y-%m-%d")
    evenement['date'] = evenement['date'].dt.date
    print(evenement['date'])
    event_json = evenement.to_json(orient='index', date_format='iso')
    parsed = json.loads(event_json)
    with open(file_path, 'w') as file:
            json.dump(parsed, file, indent=2)
            file.close()
    
    print('json file created')


"""
    Pour plustard : Esaayé de faire un json qui ne se réécrit pas
"""