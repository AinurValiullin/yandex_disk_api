import requests
from config.base import RESOURCES_URL, get_name
from config.auth import get_headers


def test_create_folder():
    folder_name = get_name("folder") 
    params = {
        "path": f"/{folder_name}"
    }

    response = requests.put(url=RESOURCES_URL, headers=get_headers(), params=params) #создаем папку для теста
    assert response.status_code == 201 #проверяем ответ сервера

    check_response = requests.get(url=RESOURCES_URL, headers=get_headers(), params=params)
    assert check_response.status_code == 200 #через get проверяем что папка точно создалась

    response2 = requests.put(url=RESOURCES_URL, headers=get_headers(), params=params)
    assert response2.status_code == 409 #негативный тест на дубликат

    no_path_response = requests.put(url=RESOURCES_URL, headers=get_headers())
    assert no_path_response.status_code == 400 #негативный тест на отсутствие path

    invalid_name_response = requests.put(url=RESOURCES_URL, headers=get_headers(), params={"path": "////^&&%#???"})
    assert invalid_name_response.status_code == 404 #негативный тест на неcуществующий путь

    delete_response = requests.delete(url=RESOURCES_URL, headers=get_headers(), params=params) #удаляем тестовую папку
    assert delete_response.status_code == 204 #проверяем что папка удалилась