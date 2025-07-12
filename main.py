import sys
import datetime as dt
from source import configuration, TmdbAPI, email_template, email_controller
from source.configuration import logging
from source.configuration_checker import check_configuration
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger

# Load correct API module
if configuration.conf.server_type == "emby":
    from source import EmbyAPI as MediaServerAPI
else:
    from source import JellyfinAPI as MediaServerAPI

# [Keep populate_series_item_from_episode and populate_series_item_with_series_related_information mostly the same]
# Update calls to JellyfinAPI -> MediaServerAPI

def populate_series_item_with_series_related_information(series_items, watched_tv_folders_id):
    for folder_id in watched_tv_folders_id:
        for serie_name in series_items.keys():
            item = MediaServerAPI.get_item_from_parent_by_name(parent_id=folder_id, name=serie_name)
            if item:
                series_items[item['Name']]["year"] = item.get("ProductionYear", "Unknown")
                tmdb_id = item.get("ProviderIds", {}).get("Tmdb")

                if tmdb_id:
                    tmdb_info = TmdbAPI.get_media_detail_from_id(id=tmdb_id, type="tv")
                else:
                    logging.info(f"Item {serie_name} has no TMDB id, searching by title.")
                    tmdb_info = TmdbAPI.get_media_detail_from_title(title=serie_name, type="tv", year=item.get("ProductionYear"))

                if not tmdb_info:
                    logging.warning(f"Item {serie_name} not found on TMDB.")
                else:
                    series_items[item['Name']]["description"] = tmdb_info.get("overview", "No overview available.")
                    poster_path = tmdb_info.get("poster_path")
                    series_items[item['Name']]["poster"] = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else configuration.conf.defaults.poster_fallback
            else:
                logging.warning(f"Series {serie_name} not found in server. Skipping.")

def send_newsletter():
    logging.info("Sending newsletter ...")
    folders = MediaServerAPI.get_root_items()
    watched_film_folders_id = []
    watched_tv_folders_id = []

    for item in folders:
        if item["Name"] in configuration.conf.jellyfin.watched_film_folders:
            watched_film_folders_id.append(item["Id"])
        elif item["Name"] in configuration.conf.jellyfin.watched_tv_folders:
            watched_tv_folders_id.append(item["Id"])

    total_movie = 0
    total_tv = 0
    movie_items = {}
    series_items = {}

    for folder_id in watched_film_folders_id:
        items, total_count = MediaServerAPI.get_item_from_parent(
            parent_id=folder_id,
            type="movie",
            minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.jellyfin.observed_period_days)
        )
        total_movie += total_count
        for item in items:
            tmdb_id = item.get("ProviderIds", {}).get("Tmdb")
            tmdb_info = TmdbAPI.get_media_detail_from_id(id=tmdb_id, type="movie") if tmdb_id else \
                        TmdbAPI.get_media_detail_from_title(title=item["Name"], type="movie", year=item.get("ProductionYear"))

            if not tmdb_info:
                logging.warning(f"Movie {item['Name']} not found on TMDB.")
                continue

            movie_items[item["Name"]] = {
                "year": item.get("ProductionYear"),
                "created_on": item.get("DateCreated"),
                "description": tmdb_info.get("overview", "No overview available."),
                "poster": f"https://image.tmdb.org/t/p/w500{tmdb_info.get('poster_path')}" if tmdb_info.get("poster_path") else configuration.conf.defaults.poster_fallback
            }

    for folder_id in watched_tv_folders_id:
        items, total_count = MediaServerAPI.get_item_from_parent(
            parent_id=folder_id,
            type="tv",
            minimum_creation_date=dt.datetime.now() - dt.timedelta(days=configuration.conf.jellyfin.observed_period_days)
        )
        total_tv += total_count
        for item in items:
            if item.get("Type") == "Episode":
                populate_series_item_from_episode(series_items, item)

    populate_series_item_with_series_related_information(series_items, watched_tv_folders_id)

    if movie_items or series_items:
        template = email_template.populate_email_template(
            movies=movie_items,
            series=series_items,
            total_tv=total_tv,
            total_movie=total_movie
        )
        email_controller.send_email(template)
        logging.info("All emails sent.")
    else:
        logging.info("No new items to report.")

def newsletter_job():
    try:
        send_newsletter()
    except Exception as e:
        logging.error(f"[FATAL] Error during newsletter send: {e}")

if __name__ == "__main__":
    logging.info("Jellyfin/Emby Newsletter starting...")
    try:
        check_configuration()
    except Exception as e:
        logging.error(f"[FATAL] Configuration check failed: {e}")
        sys.exit(1)

    if configuration.conf.scheduler.enabled:
        scheduler = BlockingScheduler()
        trigger = CronTrigger().from_crontab(configuration.conf.scheduler.cron)
        scheduler.add_job(newsletter_job, trigger)
        logging.info(f"Scheduler started. Next run at {trigger.get_next_fire_time(None, dt.datetime.now()).isoformat()}")
        scheduler.start()
    else:
        logging.info("Scheduler disabled. Sending newsletter once.")
        send_newsletter()