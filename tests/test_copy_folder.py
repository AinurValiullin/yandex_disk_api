from config.base import get_name
from client.yandex_disk_api_client import create_folder, get_resources, delete, copy
from utils.assertions import assert_create_folder_response, assert_error_response

def test_copy_folder(headers): #позитивный тест на создание копии папки
    folder_name = get_name("folder") 
    response = create_folder(headers, folder_name)
    assert response.status_code == 201
    assert_create_folder_response(response.json())
    response = get_resources(headers, f"/{folder_name}") #через get проверим что папка точно создалась
    assert response.status_code == 200

    copy_folder_name = f"copy_{folder_name}" #создадим копию
    copy_response = copy(headers, folder_name, copy_folder_name)
    assert copy_response.status_code in [201, 202] 
    assert_create_folder_response(copy_response.json())
    response = get_resources(headers, f"/{copy_folder_name}") #через get проверим что папка точно создалась
    assert response.status_code == 200

    del_response = delete(headers, f"/{folder_name}") #удалим тестовую папку1
    assert del_response.status_code in [200, 202, 204]
    del_response = delete(headers, f"/{copy_folder_name}") #удалим тестовую папку2
    assert del_response.status_code in [200, 202, 204]

def test_copy_to_existing_folder(headers): #негативный тест на копирование папки уже существующую
    folder_name = get_name()
    copy_folder_name = f"copy_{folder_name}"

    create_folder(headers, folder_name)
    create_folder(headers, copy_folder_name)

    response = copy(headers, folder_name, copy_folder_name)
    assert response.status_code == 409
    assert_error_response(response.json())

    check = get_resources(headers, f"/{copy_folder_name}")
    assert check.status_code == 200

    delete(headers, f"/{folder_name}")
    delete(headers, f"/{copy_folder_name}")

def test_copy_from_non_existing_folder(headers): #негативный тест на копирование не существующий папки
    folder_name = get_name()
    copy_folder_name = f"copy_{folder_name}"

    response = copy(headers, folder_name, copy_folder_name)
    assert response.status_code == 404
    assert_error_response(response.json())
    check_copy = get_resources(headers, f"/{copy_folder_name}")
    assert check_copy.status_code == 404
    
def test_copy_without_token(headers): #негативный тест на копирование без токена
    folder_name = get_name()
    copy_folder_name = f"copy_{folder_name}"

    create_folder(headers, folder_name)
    
    response = copy(None, folder_name, copy_folder_name)
    assert response.status_code == 401
    assert_error_response(response.json())

    delete(headers, f"/{folder_name}")