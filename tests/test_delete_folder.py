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
    assert create_response.status_code == 201 #проверяем что папка создалась

    delete_response = requests.delete(url=RESOURCES_URL, headers=headers, params=params)
    assert delete_response.status_code == 204 #проверяем что папка удалилась

    check_response = requests.get(url=RESOURCES_URL, headers=get_headers(), params=params)
    assert check_response.status_code == 404 #через get проверяем что папка точно удалилась

    delete_response2 = requests.delete(url=RESOURCES_URL, headers=headers, params=params)
    assert delete_response2.status_code == 404 #повторное удаление (удаление несущ папки)

    no_path_delete = requests.delete(url=RESOURCES_URL, headers=headers)
    assert no_path_delete.status_code == 400 #удаление без path

