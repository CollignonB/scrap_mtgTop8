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
    pass

"""
regex qui recupère tout les noms de carte et le nombre d'exemplaire
;">.*?</
"""