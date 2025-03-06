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
       
        

class Config:
    required_keys = ["jellyfin", "tmdb"]
    def __init__(self, data):
        for key in self.required_keys:
            if key not in data:
                logging.error(f"[FATAL] Load config fail. Was expecting the key {key}")
                exit(1)
    
        self.jellyfin = Jellyfin(data["jellyfin"])
        self.tmdb = Tmdb(data["tmdb"])
    
    



try:
    with open("./config/config.yml") as config_yml:
        try:
            raw_conf = yaml.safe_load(config_yml)
            conf = Config(raw_conf)
        
        except yaml.YAMLError as exc:
            raise Exception(exc)
except Exception as e :
    raise Exception(f"[FATAL] API will stop now. Error while checking config file, {e}")