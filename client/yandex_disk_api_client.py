import requests
from config.base import RESOURCES_URL, COPY_URL

def normalize_path(path):
    if not path:
        return "/"
    if path.startswith("/"):
        return path
    else:
        return f"/{path}"

def get_resources(headers, path="/"):
    return requests.get(RESOURCES_URL, headers=headers, params={"path": normalize_path(path)})

def create_folder(headers, path):
    return requests.put(RESOURCES_URL, headers=headers, params={"path": normalize_path(path)})

def delete(headers, path="/"):
    return requests.delete(RESOURCES_URL, headers=headers, params={"path": normalize_path(path)})

def copy(headers, source_path, target_path):
    params = {
        "from": normalize_path(source_path),
        "path": normalize_path(target_path)
    }
    return requests.post(url=COPY_URL, headers=headers, params=params)