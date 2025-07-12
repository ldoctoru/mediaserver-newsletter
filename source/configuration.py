import os
import yaml
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class Scheduler:
    def __init__(self, data):
        if data is None or "cron" not in data:
            logging.info("No cron expression given. The newsletter will run once at startup and then stop.")
            self.enabled = False
        else:
            self.enabled = True
            self.cron = data["cron"]
            parsed_cron = self.cron.strip().split(" ")
            if len(parsed_cron) != 5:
                raise Exception(f"[FATAL] Load config fail. Was expecting a valid cron expression in scheduler.cron, got {self.cron}")
            try:
                self.week_of_day = int(parsed_cron[4])
                self.week_of_day = (self.week_of_day - 1) % 7
                self.cron = " ".join(parsed_cron[:4]) + f" {self.week_of_day}"
            except:
                pass

class Jellyfin:
    required_keys = ["url", "api_token", "watched_film_folders", "watched_tv_folders", "observed_period_days"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                raise Exception(f"[FATAL] Load config fail. Was expecting the key jellyfin.{key}")
        self.url = data["url"]
        self.api_token = data["api_token"]
        self.watched_film_folders = data["watched_film_folders"]
        self.watched_tv_folders = data["watched_tv_folders"]
        self.observed_period_days = data["observed_period_days"]

class Emby:
    required_keys = ["url", "api_token", "watched_film_folders", "watched_tv_folders", "observed_period_days"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                raise Exception(f"[FATAL] Load config fail. Was expecting the key emby.{key}")
        self.url = data["url"]
        self.api_token = data["api_token"]
        self.watched_film_folders = data["watched_film_folders"]
        self.watched_tv_folders = data["watched_tv_folders"]
        self.observed_period_days = data["observed_period_days"]

class Tmdb:
    required_keys = ["api_key"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                raise Exception(f"[FATAL] Load config fail. Was expecting the key tmdb.{key}")
        self.api_key = data["api_key"]

class EmailTemplate:
    required_keys = ["language","subject","title","subtitle","jellyfin_url","unsubscribe_email","jellyfin_owner_name"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                raise Exception(f"[FATAL] Load config fail. Was expecting the key email_template.{key}")
        self.language = data["language"]
        self.subject = data["subject"]
        self.title = data["title"]
        self.subtitle = data["subtitle"]
        self.jellyfin_url = data["jellyfin_url"]
        self.unsubscribe_email = data["unsubscribe_email"]
        self.jellyfin_owner_name = data["jellyfin_owner_name"]

class Email:
    required_keys = ["smtp_server", "smtp_port", "smtp_username", "smtp_password", "smtp_sender_email"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                raise Exception(f"[FATAL] Load config fail. Was expecting the key email.{key}")
        self.smtp_server = data["smtp_server"]
        self.smtp_port = data["smtp_port"]
        self.smtp_user = data["smtp_username"]
        self.smtp_password = data["smtp_password"]
        self.smtp_sender_email = data["smtp_sender_email"]

class Config:
    required_keys = ["server_type", "jellyfin", "emby", "tmdb", "email_template", "email", "recipients"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key {key}")
                exit(1)

        # Allow override by environment variable
        server_type = os.getenv("SERVER_TYPE", data.get("server_type", "")).lower()
        if server_type not in ["jellyfin", "emby"]:
            logging.error('Please set "server_type" to "jellyfin" or "emby" in config.yml or as SERVER_TYPE env variable.')
            exit(1)
        self.server_type = server_type

        self.jellyfin = Jellyfin(data["jellyfin"])
        self.emby = Emby(data["emby"])
        self.tmdb = Tmdb(data["tmdb"])
        self.email_template = EmailTemplate(data["email_template"])
        self.email = Email(data["email"])
        self.recipients = data["recipients"]
        self.scheduler = Scheduler(data["scheduler"]) if "scheduler" in data else Scheduler([])

# Load and validate config at module import
try:
    with open("./config/config.yml") as config_yml:
        try:
            raw_conf = yaml.safe_load(config_yml)
            conf = Config(raw_conf)
        except yaml.YAMLError as exc:
            raise Exception(exc)
except Exception as e:
    raise Exception(f"[FATAL] API will stop now. Error while checking config file, {e}")