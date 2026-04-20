from config.base import get_name
import time
import requests
from config.base import RESOURCES_URL
from client.yandex_disk_api_client import create_folder, get_resources, delete
from utils.assertions import assert_create_folder_response, assert_error_response

def delete_and_check(headers, path): #функция для удаления
    del_response = delete(headers, path)
    assert del_response.status_code in [200, 202, 204]
    time.sleep(1)
    check = get_resources(headers, path) #через get проверим что папка точно удалилась
    assert check.status_code == 404
    assert_error_response(check.json()) #проверка ответа об ошибке

def test_create_folder(headers): #позитивный тест на создание папки
    folder_name = get_name("folder") 
    response = create_folder(headers, folder_name)
    assert response.status_code == 201
    assert_create_folder_response(response.json())
    response = get_resources(headers, f"/{folder_name}") #через get проверим что папка точно создалась
    assert response.status_code == 200
    delete_and_check(headers, f"/{folder_name}") #удалим тестовую папку
   
def test_create_folder_already_exists(headers): #негативный тест на создание уже существующей папки
    folder_name = get_name("folder")
    first = create_folder(headers, folder_name) #создадим папку
    assert first.status_code == 201
    response = create_folder(headers, folder_name) #повторно создадим папку с таким именем
    assert response.status_code == 409
    assert_error_response(response.json()) #проверка ответа об ошибке
    delete_and_check(headers, f"/{folder_name}") #удалим тестовую папку

def test_create_folder_no_token(): #негативный тест на создание папки без токена
    folder_name = get_name("folder")
    response = create_folder(None, folder_name)
    assert response.status_code == 401
    assert_error_response(response.json()) #проверка ответа об ошибке

def test_create_folder_without_name(headers): #негативный тест на создание папки без имени
    response = requests.put(RESOURCES_URL, headers=headers)
    assert response.status_code == 400
    assert_error_response(response.json()) #проверка ответа об ошибке