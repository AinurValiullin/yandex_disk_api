import requests
from config.base import RESOURCES_URL, COPY_URL, get_name
from config.auth import get_headers


def test_copy_folder():
    headers = get_headers()
    folder = get_name("folder") #даем уникальное имя папке1
    copy_folder = get_name("copy") #даем уникальное имя папке2 

    create_response = requests.put(url=RESOURCES_URL, headers=headers, params={"path": f"/{folder}"}) #создаем папку1 для теста
    assert create_response.status_code == 201 #папка1 создалась

    check_response1 = requests.get(url=RESOURCES_URL, headers=headers, params={"path": f"/{folder}"})
    assert check_response1.status_code == 200 #проверяем через get что папка1 точно существует

    params = {
        "from": f"/{folder}",
        "path": f"/{copy_folder}"
    }

    copy_response = requests.post(url=COPY_URL, headers=headers, params=params)
    assert copy_response.status_code == 201 #скопировали папку1

    check_response2 = requests.get(url=RESOURCES_URL, headers=headers, params={"path": f"/{copy_folder}"})
    assert check_response2.status_code == 200 #проверяем через get что папка2 точно существует

    delete_folder = requests.delete(url=RESOURCES_URL, headers=headers, params={"path": f"/{folder}"})
    assert delete_folder.status_code == 204 #папка1 удалена
    
    delete_copy_folder = requests.delete(url=RESOURCES_URL, headers=headers, params={"path": f"/{copy_folder}"})
    assert delete_copy_folder.status_code == 204 #папка2 удалена

    no_folder = requests.post(url=COPY_URL, headers=headers, params={"from": get_name("invalid"), "path": f"/{copy_folder}"})
    assert no_folder.status_code == 404 #негативный кейс на копирование несущ папки

    no_params = requests.post(url=COPY_URL, headers=headers)
    assert no_params.status_code == 400 #негативный кейс на копирование без params