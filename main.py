import sys 
from source import configuration, JellyfinAPI, TmdbAPI
import datetime as dt
import logging



if __name__ == "__main__":
    print("Welcome to jellyfin automatic newsletter !\n")
    print("Developped by Seaweedbrain, under MIT License.")
    print("##############################################\n\n")

    folders = JellyfinAPI.get_root_items()
    watched_film_folders_id = []
    watched_tv_folders_id = []
    for item in folders:
        if item["Name"] in configuration.conf.jellyfin.watched_film_folders :
           watched_film_folders_id.append(item["Id"])
        elif item["Name"] in configuration.conf.jellyfin.watched_tv_folders :
            watched_tv_folders_id.append(item["Id"])
        else:
            logging.warning(f"Folder {item['Name']} is not watched. Skipping.")


    for folder_id in watched_film_folders_id:

        items = JellyfinAPI.get_item_from_parent(parent_id=folder_id,type="movie", minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.jellyfin.observed_period_days))
        for item in items:
            print(f"Item {item['Name']} has been created on {item['DateCreated']}")
    
    for folder_id in watched_tv_folders_id:
        
        items = JellyfinAPI.get_item_from_parent(parent_id=folder_id, type="tv", minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.jellyfin.observed_period_days))
        for item in items:
            if item["Type"] == "Episode":
                print(f"Item {item['SeriesName']} {item['SeasonName']} episode {item['IndexNumber']}has been created on {item['DateCreated']}\n\n")

    


    


