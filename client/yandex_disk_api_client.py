import requests
from config.base import RESOURCES_URL, COPY_URL

def get_resources(headers, path="/"):
    return requests.get(RESOURCES_URL, headers=headers, params={"path":path})

def create_folder(headers, folder_name):
    return requests.put(RESOURCES_URL, headers=headers, params={"path": f"/{folder_name}"})

def delete(headers, path="/"):
    return requests.delete(RESOURCES_URL, headers=headers, params={"path": path})

def copy(headers, from_path, to_path):
    params = {
        "from": f"/{from_path}",
        "path": f"/{to_path}"
    }

    return requests.post(url=COPY_URL, headers=headers, params=params)