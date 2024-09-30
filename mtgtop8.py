from bs4 import BeautifulSoup
import pandas as pd
import json
import os

# import mechanicalsoup

from urllib.request import urlopen
import re

base_url = "https://www.mtgtop8.com/"

page = urlopen(base_url)
html = page.read().decode("latin-1")
soup = BeautifulSoup(html, "html.parser")


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




list_of_decks = soup.find_all("td")[0]
list_of_events = soup.find_all("td")[1]
major_event = [] # listes des 3 évenements notés comme majeur
recent_event = [] #listes des 20 dernier événements, a modifié pour juste récupérer les évenements pas consulté

pattern_event = 'event?.*?>'

events = re.findall(pattern_event, str(list_of_events), re.IGNORECASE)
for i in range(1,4):
    major_event.append(base_url + events[i][:-2])

for i in range(5,28):
    recent_event.append(base_url + events[i][:-2])

events_inforamtion = []
re_url_event = '"ev.*?"' #regex qui va recupérer l'url de l'envent
re_name_event = '[A-Z]{2,3}?".*?</a' #regex qui va récuéprer le nom de l'event
re_date_event = '12%">.*?</' # regex qui va récupérer la date de l'event

event_url = []  # liste des urls des évenements
event_name = [] # liste des noms des évenements
event_date = [] # liste des dates des évenements

for row in list_of_events.findAll('tr', {"class"  : "hover_tr"}):
    events_inforamtion.append(str(row.findAll('td')).split(",")[1::2])

    # récupération des balises utilent dans le code html
    important = str(row.findAll('td')).split(",")[1::2]

    # recréer et stock les urls des evenements
    event_url.append(f"{base_url}{re.search(re_url_event, str(important), re.IGNORECASE).group()[1:-1]}") 

    # recupération du nom de l'evenement
    if format != "EDH":
        event_name.append(re.search(re_name_event, str(important), re.IGNORECASE).group()[4:-3])
    else:
        event_name.append(re.search(re_name_event, str(important), re.IGNORECASE).group()[5:-3])

    # récuperation de la date de l'évenement
    event_date.append(re.search(re_date_event, str(important), re.IGNORECASE).group()[5:-2])

# création d'un dictionnaire pour créer le Dataframe
dict = {'name' : event_name, 'url' : event_url, 'date' : event_date}

evenement = pd.DataFrame(dict)
json = evenement.to_json(orient='index')
parsed = json.loads(json)

file_path = "Documents/python/web_scrp_mtg/mtgtop8.json"

if os.path.exists(file_path):
    with open(file_path, 'w') as file:
        json.dump(parsed, file, indent=2)
        file.close()