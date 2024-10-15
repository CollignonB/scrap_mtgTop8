from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from urllib.request import urlopen
import re
from os import walk

# recupération de la liste des fichiers d'evenement 
list_of_deck = next(walk(r"C:\Users\Utilisateur\Documents\python\web_scrp_mtg\events"), (None, None, []))[2]

# ouverutre d'un fichier d'evenement
deck_lists = pd.read_json(fr"C:\Users\Utilisateur\Documents\python\web_scrp_mtg\events\{list_of_deck[8]}", orient="index")

# for index, row in deck_lists.iterrows():
    # print(deck_lists['Deck'][ind], deck_lists['URL'][ind])

page = urlopen(deck_lists.loc[3]['URL'])
html = page.read().decode("latin-1")
soup = BeautifulSoup(html, "html.parser")

card_name, copy = [], []

list_of_cards = str(soup.find_all("div", attrs={"style" : "margin:3px;flex:1;"}))

for line in list_of_cards.split("<div")[2:]:

    data = re.search(';">.*?</', str(line), re.IGNORECASE)
    important_data = []
    if type(data) == re.Match:
        important_data = re.findall('">.*?<',data.group(), re.IGNORECASE)
    if len(important_data) == 2:
        copy.append(important_data[0][2:-2])
        card_name.append(important_data[1][2:-1])
# print(copy, card_name)

deck_list = pd.DataFrame(columns=["number of copy", "card name", "main/side"])
main_deck_size = 0
for i in range(0, len(copy)):
    if main_deck_size != 60:
        deck_list.loc[i] = [copy[i], card_name[i], "Main Deck"]
        main_deck_size += int(copy[i])
    else:
        deck_list.loc[i] = [copy[i], card_name[i], "Sideboard"]



print(deck_list)

"""
amélioration : 
récupérer l'url de chaque carte sur scryfall.com via un bot qui recherche le nom de la carte sur le site et recupère l'url
"""