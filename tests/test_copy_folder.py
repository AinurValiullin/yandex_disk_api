import requests
from config.base import RESOURCES_URL, COPY_URL, get_name
from config.auth import get_headers


def test_copy_folder():
    headers = get_headers()
    folder = get_name("folder") #даем уникальное имя папке1
    copy_folder = get_name("copy") #даем уникальное имя папке2 

    create_response = requests.put(url=RESOURCES_URL, headers=headers, params={"path": f"/{folder}"}) #создаем папку1 для теста
    assert create_response.status_code == 201

    params = {
        "from": f"/{folder}",
        "path": f"/{copy_folder}"
    }

    copy_response = requests.post(url=COPY_URL, headers=headers, params=params)
    assert copy_response.status_code == 201

    delete_folder = requests.delete(url=RESOURCES_URL, headers=headers, params={"path": f"/{folder}"})
    assert delete_folder.status_code == 204
    
    delete_copy_folder = requests.delete(url=RESOURCES_URL, headers=headers, params={"path": f"/{copy_folder}"})
    assert delete_copy_folder.status_code == 204