import get_event, get_list_of_decks, get_deck_list
import pandas as pd
import os


def main():

    # creation of event list json file 
    filepath = r"C:/Users/Utilisateur/Documents/python/web_scrp_mtg/mtgtop8.json"
    date_last_update = get_event.get_date_last_update(filepath)
    followed_format = get_event.get_mtgtop8_format()
    list_of_events = get_event.get_list_of_event(followed_format["STANDARD"])
    event_data = get_event.get_event_data(list_of_events, date_last_update)
    get_event.data_to_json(event_data, filepath)
    
    # creation of list of deck json files
    list_of_event = pd.read_json(filepath, orient="index")
    get_list_of_decks.get_list_of_decks(list_of_event)

    # creation of deck list json files
    list_of_deck = [str(x[0]) for x in os.walk(r"C:\Users\Utilisateur\Documents\python\web_scrp_mtg\events")]
    filenames = get_deck_list.get_file_names(list_of_deck)
    get_deck_list.get_deck_list(filenames, 0)

main()