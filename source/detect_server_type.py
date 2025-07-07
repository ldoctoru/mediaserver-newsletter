import requests

def detect_server_type(base_url):
    """
    Detects whether the server at the given base_url is Jellyfin or Emby.
    Returns:
        'jellyfin' if Jellyfin detected,
        'emby' if Emby detected,
        None if detection fails.
    """
    if not base_url or not base_url.startswith(('http://', 'https://')):
        return None

    url = base_url.rstrip('/') + '/System/Info/Public'
    try:
        resp = requests.get(url, timeout=5)
        if resp.status_code != 200:
            return None
        data = resp.json()
        # ProductName or ServerName may contain 'Jellyfin' or 'Emby'
        name_fields = f"{data.get('ServerName', '')} {data.get('ProductName', '')}".lower()
        if 'jellyfin' in name_fields:
            return 'jellyfin'
        if 'emby' in name_fields:
            return 'emby'
    except Exception:
        return None
    return None