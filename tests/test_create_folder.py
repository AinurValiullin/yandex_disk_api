import requests
from config.base import RESOURCES_URL, get_name
from config.auth import get_headers


def test_create_folder():
    folder_name = get_name("folder") 
    params = {
        "path": f"/{folder_name}"
    }

    response = requests.put(url=RESOURCES_URL, headers=get_headers(), params=params) #создаем папку для теста
    assert response.status_code == 201

    delete_response = requests.delete(url=RESOURCES_URL, headers=get_headers(), params=params) #удаляем тестовую папку
    assert delete_response.status_code == 204 #проверяем что папка удалилась