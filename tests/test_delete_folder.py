import requests
from config.base import RESOURCES_URL, get_name
from config.auth import get_headers

def test_delete_folder():
    headers = get_headers()
    folder_name = get_name("folder")

    params = {
        "path": f"/{folder_name}"
    }

    create_response = requests.put(url=RESOURCES_URL, headers=headers, params=params)
    assert create_response.status_code == 201

    delete_response = requests.delete(url=RESOURCES_URL, headers=headers, params=params)
    assert delete_response.status_code == 204