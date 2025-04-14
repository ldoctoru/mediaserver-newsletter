import sys 
from source import configuration, JellyfinAPI, TmdbAPI, email_template, email_controller
import datetime as dt
import logging





if __name__ == "__main__":
    print("Thanks for using jellyfin automatic newsletter !\n")
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

    total_movie = 0
    total_tv = 0
    movie_items = {}
    series_items = {}


    for folder_id in watched_film_folders_id:
        items, total_count = JellyfinAPI.get_item_from_parent(parent_id=folder_id,type="movie", minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.jellyfin.observed_period_days))
        total_movie += total_count
        for item in items:
            if "ProductionYear"  not in item.keys():
                logging.warning(f"Item {item['Name']} has no production year.")
                item["ProductionYear"] = 0
            if "DateCreated" not in item.keys():
                logging.warning(f"Item {item['Name']} has no creation date.")
                item["DateCreated"] = None
            


            tmdb_info = TmdbAPI.get_media_detail_from_title(title=item["Name"], type="movie", year=item["ProductionYear"])

            if "overview" not in tmdb_info.keys():
                logging.warning(f"Item {item['Name']} has no overview.")
                tmdb_info["overview"] = "No overview available."

            movie_items[item["Name"]] = {
                "year":item["ProductionYear"],
                "created_on":item["DateCreated"],
                "description": tmdb_info["overview"],
                "poster": f"https://image.tmdb.org/t/p/w500{tmdb_info['poster_path']}" if tmdb_info["poster_path"] else "https://redthread.uoregon.edu/files/original/affd16fd5264cab9197da4cd1a996f820e601ee4.png"
            }
            
    
    for folder_id in watched_tv_folders_id:
        items, total_count = JellyfinAPI.get_item_from_parent(parent_id=folder_id, type="tv", minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.jellyfin.observed_period_days))
        total_tv += total_count
        for item in items:
            if item["Type"] == "Episode":
                if (item['SeriesName'] in series_items.keys() and item["SeasonName"] not in series_items[item["SeriesName"]]["seasons"] ) or (item['SeriesName'] not in series_items.keys()):

                    if item['SeriesName'] not in series_items.keys() :
                        if "DateCreated" not in item.keys():
                            logging.warning(f"Item {item['SeriesName']} has no creation date.")
                            item["DateCreated"] = None
                        if "ProductionYear" not in item.keys():
                            logging.warning(f"Item {item['SeriesName']} has no production year.")
                            item["ProductionYear"] = 0
                        
                        series_items[item['SeriesName']] = {
                        "seasons": [item["SeasonName"]] if item["SeasonName"] else [],
                        "created_on": item["DateCreated"],
                        }
                        tmdb_info = TmdbAPI.get_media_detail_from_title(title=item["SeriesName"], type="tv", year=item["ProductionYear"])
                        if "overview" not in tmdb_info.keys():
                            logging.warning(f"Item {item['SeriesName']} has no overview.")
                            tmdb_info["Overview"] = "No overview available."
                        series_items[item['SeriesName']]["description"] = tmdb_info["overview"] 
                        series_items[item['SeriesName']]["year"] = item["ProductionYear"]
                        series_items[item['SeriesName']]["poster"] = f"https://image.tmdb.org/t/p/w500{tmdb_info['poster_path']}" if tmdb_info["poster_path"] else "https://redthread.uoregon.edu/files/original/affd16fd5264cab9197da4cd1a996f820e601ee4.png"
                    else:
                        series_items[item['SeriesName']]["seasons"].append(item["SeasonName"])
    
    template = email_template.populate_email_template(movies=movie_items, series=series_items, total_tv=total_tv, total_movie=total_movie)

    #print(template)

    email_controller.send_email(template)

    print("\n\n##############################################")
    print("All done here. Exiting.")


    


