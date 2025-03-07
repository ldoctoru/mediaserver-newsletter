import yaml
import logging

class Jellyfin:
    required_keys = ["url", "api_token",  "watched_film_folders", "watched_tv_folders", "observed_period_days"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                raise Exception(f"[FATAL] Load config fail. Was expecting the key jellyfin.{key}")
                
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
    required_keys= ["language","subject","title","subtitle","jellyfin_url","unsubscribe_email","jellyfin_owner_name"]
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
    required_keys=["smtp_server", "smtp_port", "smtp_username", "smtp_password", "smtp_sender_email"]
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
    required_keys = ["jellyfin", "tmdb", "email_template", "email", "recipients"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key {key}")
                exit(1)
    
        self.jellyfin = Jellyfin(data["jellyfin"])
        self.tmdb = Tmdb(data["tmdb"])
        self.email_template = EmailTemplate(data["email_template"])
        self.email = Email(data["email"])
        self.recipients = data["recipients"]
    
    



try:
    with open("./config/config.yml") as config_yml:
        try:
            raw_conf = yaml.safe_load(config_yml)
            conf = Config(raw_conf)
        
        except yaml.YAMLError as exc:
            raise Exception(exc)
except Exception as e :
    raise Exception(f"[FATAL] API will stop now. Error while checking config file, {e}")