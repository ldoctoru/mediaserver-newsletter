from source import configuration
import requests

def get_root_items():
    headers = {
        "Authorization": f'MediaBrowser Token="{configuration.conf.jellyfin.api_token}"'
    }

    response = requests.get(f'{configuration.conf.jellyfin.url}/Items', headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error while getting the root items, status code: {response.status_code}. Answer: {response.json()}.")
    return response.json()


def get_item_from_parent(parent_id):
    headers = {
        "Authorization": f'MediaBrowser Token="{configuration.conf.jellyfin.api_token}"'
    }

    response = requests.get(f'{configuration.conf.jellyfin.url}/Items?ParentId={parent_id}&fields=DateCreated', headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error while getting the items from parent, status code: {response.status_code}. Answer: {response.json()}.")

    return response.json()