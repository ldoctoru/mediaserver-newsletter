from source import configuration
import requests
import datetime as dt

def get_root_items():
    headers = {
        "Authorization": f'MediaBrowser Token="{configuration.conf.jellyfin.api_token}"'
    }

    response = requests.get(f'{configuration.conf.jellyfin.url}/Items', headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error while getting the root items, status code: {response.status_code}. Answer: {response.json()}.")
    return response.json()["Items"]


def get_item_from_parent(parent_id, type, minimum_creation_date=None):
    if type not in ["movie", "tv"]:
        raise Exception(f"Error while retrieving a media from Jellyfin. Type must be 'movie' or 'tv'. Got {type}")
    headers = {
        "Authorization": f'MediaBrowser Token="{configuration.conf.jellyfin.api_token}"'
    }



    response = requests.get(f'{configuration.conf.jellyfin.url}/Items?ParentId={parent_id}&fields=DateCreated,ProviderIds&Recursive=true', headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error while getting the items from parent, status code: {response.status_code}. Answer: {response.json()}.")
    
    if not minimum_creation_date:
        return response.json()["Items"], response.json()["TotalRecordCount"]
    else:
        recent_items = []
        for item in response.json()["Items"]:
            creation_date = dt.datetime.strptime(item["DateCreated"].split("T")[0], "%Y-%m-%d")
            if creation_date > minimum_creation_date:
                recent_items.append(item)
        return recent_items, response.json()["TotalRecordCount"]