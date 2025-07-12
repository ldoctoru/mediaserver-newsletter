from source.configuration import conf, logging
import requests
import datetime as dt

def get_root_items():
    headers = {
        "Authorization": f'MediaBrowser Token="{conf.jellyfin.api_token}"'
    }

    response = requests.get(f'{conf.jellyfin.url}/Items', headers=headers)
    if response.status_code != 200:
        logging.error(f"[Jellyfin] Error while getting root items. Status code: {response.status_code}.")
        raise Exception(f"[Jellyfin] Error while getting root items. Status code: {response.status_code}. Response: {response.text}")
    
    return response.json().get("Items", [])

def get_item_from_parent(parent_id, type, minimum_creation_date=None):
    if type not in ["movie", "tv"]:
        raise Exception(f"[Jellyfin] Invalid type '{type}'. Must be 'movie' or 'tv'.")

    headers = {
        "Authorization": f'MediaBrowser Token="{conf.jellyfin.api_token}"'
    }

    url = f"{conf.jellyfin.url}/Items"
    params = {
        "ParentId": parent_id,
        "fields": "DateCreated,ProviderIds",
        "Recursive": "true"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"[Jellyfin] Failed to get items from parent. Status code: {response.status_code}.")
        raise Exception(f"[Jellyfin] Failed to get items from parent. Response: {response.text}")
    
    all_items = response.json().get("Items", [])
    filtered_items = []

    for item in all_items:
        if (item.get("Type") == "Episode" and item.get("LocationType") == "Virtual") or \
           (item.get("Type") == "Movie" and item.get("LocationType") == "Virtual"):
            logging.debug(f"[Jellyfin] Skipping virtual item: {item.get('Name')}")
            continue

        if not minimum_creation_date:
            filtered_items.append(item)
        else:
            try:
                creation_date = dt.datetime.strptime(item["DateCreated"].split("T")[0], "%Y-%m-%d")
                if creation_date > minimum_creation_date:
                    logging.debug(f"[Jellyfin] Recent item: {item['Name']} (added on {creation_date})")
                    filtered_items.append(item)
            except Exception as e:
                logging.warning(f"[Jellyfin] Failed to parse date for item {item.get('Name')}: {e}")

    return filtered_items, response.json().get("TotalRecordCount", 0)

def get_item_from_parent_by_name(parent_id, name):
    headers = {
        "Authorization": f'MediaBrowser Token="{conf.jellyfin.api_token}"'
    }

    url = f"{conf.jellyfin.url}/Items"
    params = {
        "ParentId": parent_id,
        "fields": "DateCreated,ProviderIds",
        "Recursive": "true"
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code != 200:
        logging.error(f"[Jellyfin] Failed to get items from parent by name. Status code: {response.status_code}.")
        raise Exception(f"[Jellyfin] Failed to get items by name. Response: {response.text}")
    
    for item in response.json().get("Items", []):
        if item.get("Name") == name:
            return item

    logging.warning(f"[Jellyfin] No item named '{name}' found under parent ID {parent_id}.")
    return None