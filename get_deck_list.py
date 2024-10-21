from bs4 import BeautifulSoup
import pandas as pd
import json
import os
from urllib.request import urlopen
import re
from os import walk

# recupération de la liste des fichiers d'evenement 
list_of_deck = [str(x[0]) for x in os.walk(r"C:\Users\Utilisateur\Documents\python\web_scrp_mtg\events")]

def get_file_names(list_of_deck):
    filenames = []
    for deck in list_of_deck:

        filenames.append(next(walk(deck), (None, None, []))[2])
    return filenames

def deck_standings(deck_number):
    if deck_number == 0:
                deck_standings = "1"
    elif deck_number == 1:
        deck_standings = "2"
    elif deck_number == 3 or deck_number == 2:
        deck_standings = "3-4"
    elif deck_number >= 4 and deck_number <= 7:
        deck_standings = "5-8"
    elif deck_number >= 8 and deck_number <= 15:
        deck_standings = "9-16"
    elif deck_number >= 16 and deck_number <= 31:
        deck_standings = "17-32"
    else :
        deck_standings = "33-64"
    return deck_standings
    
# ouverutre d'un fichier d'evenement
def get_deck_list(filenames, manual_traitement):
    for event_index in range(1, len(filenames)): 
        if len(filenames[event_index]) != 1:
            print(filenames[event_index][-1][:-5], " deja traité")
            continue
        try:
            deck_lists = pd.read_json(fr"{list_of_deck[event_index]}\{filenames[event_index][-1]}", orient="index")
            player = deck_lists["Player"]
            deck = deck_lists["Deck"]
            url = deck_lists["URL"]
        except KeyError:
            print("Le json n'est pas au bon format")

    # for index, row in deck_lists.iterrows():
        # print(deck_lists['Deck'][ind], deck_lists['URL'][ind])

        for deck_number in range(0, len(deck_lists)):
            page = urlopen(deck_lists.loc[deck_number]['URL'])
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

            deck_standing = deck_standings(deck_number)

            file_path = f"{list_of_deck[event_index]}\#{str(deck_standing)}_{deck_lists['Deck'][deck_number].replace(':','').replace(' ', '_').replace('/', '_')}.json"

            if os.path.isfile(file_path) :
                file_path = f"{list_of_deck[event_index]}\#{str(deck_standing)}_{deck_lists['Deck'][deck_number].replace(':','').replace(' ', '_').replace('/', '_')}({deck_number}).json"


            event_json = deck_list.to_json(orient='index')
            parsed = json.loads(event_json)

            with open(file_path, 'w') as file:
                json.dump(parsed, file, indent=2)
                print(f"#{deck_standings}_{deck_lists['Deck'][deck_number].replace(':','').replace(' ', '_').replace('/', '_')}.json created")
                file.close()
                
        if manual_traitement == 1:
            print("Passer a l'event suivant ? y/n")
            p = input()
            if p.lower() == 'n':
                print("Arret du traitement")
                break
"""
amélioration : 
récupérer l'url de chaque carte sur scryfall.com via un bot qui recherche le nom de la carte sur le site et recupère l'url
"""