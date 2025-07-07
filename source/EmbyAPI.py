from source import configuration
import requests
import datetime as dt

def _auth_header():
    return {
        "X-Emby-Token": configuration.conf.emby.api_token
    }

def get_user_id():
    """
    Fetch the user ID matching config username (if given), or the first Emby user.
    """
    url = f"{configuration.conf.emby.url.rstrip('/')}/Users"
    headers = _auth_header()
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception(f"Failed to get Emby users: {r.status_code} {r.text}")
    users = r.json()
    if not users:
        raise Exception("No users found on Emby server.")
    # If config username is present, use it
    username = getattr(configuration.conf.emby, "username", None)
    if username:
        for user in users:
            if user["Name"].lower() == username.lower():
                return user["Id"]
        raise Exception(f"User '{username}' not found on Emby server.")
    # Otherwise use the first user
    return users[0]["Id"]

def get_root_items():
    """
    Returns all top-level folders/libraries for the Emby server.
    """
    user_id = get_user_id()
    url = f"{configuration.conf.emby.url.rstrip('/')}/Users/{user_id}/Views"
    headers = _auth_header()
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception(f"Failed to get Emby root items: {r.status_code} {r.text}")
    items = r.json().get("Items", [])
    root_items = []
    for item in items:
        root_items.append({
            "Name": item.get("Name"),
            "Id": item.get("Id"),
            "Type": "Folder"
        })
    return root_items

def get_item_from_parent(parent_id, type, minimum_creation_date=None):
    """
    Fetches items of the given type ("movie" or "tv") from the specified folder/library ID.
    Returns (items, total_count)
    """
    url = f"{configuration.conf.emby.url.rstrip('/')}/Items"
    headers = _auth_header()
    params = {
        "ParentId": parent_id,
        "IncludeItemTypes": "Movie" if type == "movie" else "Series,Episode",
        "Recursive": "true",
        "Fields": "ProviderIds,ProductionYear,DateCreated,SeriesName,SeasonName,Type,Name"
    }
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        raise Exception(f"Failed to get items from parent: {r.status_code} {r.text}")
    items = r.json().get("Items", [])
    # Filter by creation date if needed
    if minimum_creation_date:
        filtered = []
        for item in items:
            try:
                created = item.get("DateCreated")
                if created:
                    dt_obj = dt.datetime.strptime(created.split("T")[0], "%Y-%m-%d")
                    if dt_obj >= minimum_creation_date:
                        filtered.append(item)
                else:
                    filtered.append(item)  # No date? Include anyway
            except Exception:
                filtered.append(item)
        items = filtered
    return items, len(items)

def get_item_from_parent_by_name(parent_id, name):
    """
    Searches for an item by name within a given parent folder.
    Returns the first matching item or None.
    """
    url = f"{configuration.conf.emby.url.rstrip('/')}/Items"
    headers = _auth_header()
    params = {
        "ParentId": parent_id,
        "SearchTerm": name,
        "Recursive": "true",
        "Fields": "ProviderIds,ProductionYear,DateCreated,SeriesName,SeasonName,Type,Name"
    }
    r = requests.get(url, headers=headers, params=params)
    if r.status_code != 200:
        return None
    items = r.json().get("Items", [])
    return items[0] if items else None