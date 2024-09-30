from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from urllib.request import urlopen
import re

list_of_event = pd.read_json("mtgtop8.json", orient="index")
print(list_of_event)
# poc sur la permière liste 

page = urlopen(list_of_event.loc[0]['url'])
html = page.read().decode("latin-1")
soup = BeautifulSoup(html, "html.parser")

# contient la liste des div qui représentent une liste de deck
list_of_decks = str(soup.find_all("div", attrs={"style" : "flex:1;"}))

deck_name, player, deck_url = [], [], []

for line in list_of_decks.split(","):
    important_info = line.split("><")[1:3] # récupère les données importantes dans les divs
    
    deck_name.append(re.search('">.*?<', str(important_info), re.IGNORECASE).group()[2:-1]) # extrait le nom du deck
    player.append(re.search('player=.*?"', str(important_info), re.IGNORECASE).group()[7:-1].replace("+", " ")) # extrait le nom du joueur
    deck_url.append(f"https://www.mtgtop8.com/event{re.search('href.*?>', str(important_info), re.IGNORECASE).group()[6:-2]}") # extrait l'url' du deck

deck_data = pd.DataFrame(columns=["Player", "Deck", "URL"])
for i in range(0, len(deck_name)):
    deck_data.loc[i] = [player[i], deck_name[i], deck_url[i]]

file_path = f"C:/Users/Utilisateur/Documents/python/web_scrp_mtg/{list_of_event.loc[0]['name']}.json"

event_json = deck_data.to_json(orient='index')
parsed = json.loads(event_json)

with open(file_path, 'w') as file:
        json.dump(parsed, file, indent=2)
        file.close()

