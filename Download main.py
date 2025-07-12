import sys 
from source import configuration, TmdbAPI, email_template, email_controller
import datetime as dt
from source.configuration import logging
from source.configuration_checker import check_configuration
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger


def populate_series_item_from_episode(series_items, item):
    if "SeriesName" not in item.keys():
        logging.warning(f"Item {item['Name']} has no SeriesName. Skipping.")
        return
    if item["SeriesName"] not in series_items.keys():
        series_items[item["SeriesName"]] = {
            "episodes": [],
            "seasons": [],
            "created_on": "undefined",
            "description": "No description available.",
            "year": "undefined",
            "poster": "https://redthread.uoregon.edu/files/original/affd16fd5264cab9197da4cd1a996f820e601ee4.png"
        }
    if item["SeasonName"] not in series_items[item["SeriesName"]]["seasons"]:
        series_items[item["SeriesName"]]["seasons"].append(item["SeasonName"])
    series_items[item["SeriesName"]]["episodes"].append(item.get('IndexNumber'))
    if series_items[item["SeriesName"]]["created_on"] != "undefined" or series_items[item["SeriesName"]]["created_on"] is not None:
        try: 
            if dt.datetime.fromisoformat(series_items[item["SeriesName"]]["created_on"]) < dt.datetime.fromisoformat(item["DateCreated"]):
                series_items[item["SeriesName"]]["created_on"] = item["DateCreated"]
        except:
            pass
    series_items[item["SeriesName"]]["created_on"] = item.get("DateCreated", "undefined") 


def populate_series_item_with_series_related_information(series_items, watched_tv_folders_id):
    from source import JellyfinAPI
    for folder_id in watched_tv_folders_id:
        for serie_name in series_items.keys():
            item = JellyfinAPI.get_item_from_parent_by_name(parent_id=folder_id, name=serie_name)
            if item is not None:
                series_items[item['Name']]["year"] = item["ProductionYear"]
                tmdb_id = None
                if "ProviderIds" in item.keys():
                    if "Tmdb" in item["ProviderIds"].keys():
                        tmdb_id = item["ProviderIds"]["Tmdb"]

                if tmdb_id is not None:
                    tmdb_info = TmdbAPI.get_media_detail_from_id(id=tmdb_id, type="tv")
                else:
                    logging.info(f"Item {item['SeriesName']} has no TMDB id, searching by title.")
                    tmdb_info = TmdbAPI.get_media_detail_from_title(title=item["SeriesName"], type="tv", year=item["ProductionYear"])

                if tmdb_info is None:
                    logging.warning(f"Item {item['Name']} has not been found on TMDB. Skipping.")
                else:
                    if "overview" not in tmdb_info.keys():
                        logging.warning(f"Item {item['SeriesName']} has no overview.")
                        tmdb_info["Overview"] = "No overview available."
                    series_items[item['Name']]["description"] = tmdb_info["overview"]

                    series_items[item['Name']]["poster"] = f"https://image.tmdb.org/t/p/w500{tmdb_info['poster_path']}" if tmdb_info["poster_path"] else "https://redthread.uoregon.edu/files/original/affd16fd5264cab9197da4cd1a996f820e601ee4.png"
            else:
                logging.warning(f"Item {serie_name} has not been found in Jellyfin. Skipping.")




def send_newsletter():
    from source import JellyfinAPI
    logging.info("Sending newsletter ...")
    folders = JellyfinAPI.get_root_items()
    watched_film_folders_id = []
    watched_tv_folders_id = []
    for item in folders:
        if item["Name"] in configuration.conf.server.watched_film_folders:
            watched_film_folders_id.append(item["Id"])
            logging.info(f"Folder {item['Name']} is watched for films.")
        elif item["Name"] in configuration.conf.server.watched_tv_folders:
            watched_tv_folders_id.append(item["Id"])
            logging.info(f"Folder {item['Name']} is watched for TV series.")
        else:
            logging.warning(f"Folder {item['Name']} is not watched. Skipping. Add "{item['Name']}" in your watched folder to include it.")

    total_movie = 0
    total_tv = 0
    movie_items = {}
    series_items = {}

    for folder_id in watched_film_folders_id:
        items, total_count = JellyfinAPI.get_item_from_parent(parent_id=folder_id, type="movie", minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.server.observed_period_days))
        total_movie += total_count
        for item in items:
            tmdb_id = None
            if "ProductionYear" not in item.keys():
                logging.warning(f"Item {item['Name']} has no production year.")
                item["ProductionYear"] = 0
            if "DateCreated" not in item.keys():
                logging.warning(f"Item {item['Name']} has no creation date.")
                item["DateCreated"] = None
            if "ProviderIds" in item.keys() and "Tmdb" in item["ProviderIds"]:
                tmdb_id = item["ProviderIds"]["Tmdb"]

            if tmdb_id is not None:
                tmdb_info = TmdbAPI.get_media_detail_from_id(id=tmdb_id, type="movie")
            else:
                logging.info(f"Item {item['Name']} has no TMDB id, searching by title.")
                tmdb_info = TmdbAPI.get_media_detail_from_title(title=item["Name"], type="movie", year=item["ProductionYear"])

            if tmdb_info is None:
                logging.warning(f"Item {item['Name']} has not been found on TMDB. Skipping.")
            else:
                if "overview" not in tmdb_info.keys():
                    logging.warning(f"Item {item['Name']} has no overview.")
                    tmdb_info["overview"] = "No overview available."

                movie_items[item["Name"]] = {
                    "year": item["ProductionYear"],
                    "created_on": item["DateCreated"],
                    "description": tmdb_info["overview"],
                    "poster": f"https://image.tmdb.org/t/p/w500{tmdb_info['poster_path']}" if tmdb_info["poster_path"] else "https://redthread.uoregon.edu/files/original/affd16fd5264cab9197da4cd1a996f820e601ee4.png"
                }

    for folder_id in watched_tv_folders_id:
        items, total_count = JellyfinAPI.get_item_from_parent(parent_id=folder_id, type="tv", minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.server.observed_period_days))
        total_tv += total_count
        for item in items:
            if item["Type"] == "Episode":
                populate_series_item_from_episode(series_items, item)

    populate_series_item_with_series_related_information(series_items=series_items, watched_tv_folders_id=watched_tv_folders_id)
    logging.debug("Series populated : " + str(series_items))
    if len(movie_items) + len(series_items) > 0:
        template = email_template.populate_email_template(movies=movie_items, series=series_items, total_tv=total_tv, total_movie=total_movie)
        email_controller.send_email(template)
        logging.info("All emails sent.")
    else:
        logging.warning("No new items found in watched folders. No email sent.")

    logging.info("Newsletter sent. Thank you for using Jellyfin/Emby Newsletter.")


def newsletter_job():
    try:
        send_newsletter()
    except Exception as e:
        logging.error(f"[FATAL] An error occurred while sending the newsletter: {e}")
        logging.error("Sending newsletter failed. Program will continue to run and retry at the next scheduled time.")


if __name__ == "__main__":
    logging.info("Jellyfin/Emby Newsletter starting...")
    logging.info("Checking configuration ...")
    try:
        check_configuration()
    except Exception as e:
        logging.error(f"[FATAL] Configuration check failed: {e}")
        sys.exit(1)
    logging.info("Configuration check passed.")

    if configuration.conf.scheduler.enabled:
        try:
            scheduler = BlockingScheduler()
            trigger = CronTrigger().from_crontab(configuration.conf.scheduler.cron)
        except Exception as e:
            logging.error(f"[FATAL] Failed to initialize scheduler: {e}")
            sys.exit(1)

        scheduler.add_job(newsletter_job, trigger)
        logging.info(f"Newsletter scheduler started. Next run at {trigger.get_next_fire_time(None, dt.datetime.now()).isoformat()}")
        scheduler.start()
    else:
        logging.info("Scheduler disabled. Sending newsletter once.")
        send_newsletter()
