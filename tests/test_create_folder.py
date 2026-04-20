import requests
from config.base import RESOURCES_URL
from client.yandex_disk_api_client import create_folder
from utils.assertions import assert_error_response
from utils.helpers import get_name, create_and_check_folder, delete_and_check

def test_create_folder(headers): #позитивный тест на создание папки
    folder_name = get_name("folder") #даем уникальное имя
    create_and_check_folder(headers, folder_name)
    delete_and_check(headers, f"/{folder_name}") #удалим тестовую папку
   
def test_create_folder_already_exists(headers): #негативный тест на создание уже существующей папки
    folder_name = get_name("folder") #даем уникальное имя
    create_and_check_folder(headers, folder_name)
    response = create_folder(headers, folder_name) #повторно создадим папку с таким именем
    assert response.status_code == 409
    assert_error_response(response.json()) #проверка ответа об ошибке
    delete_and_check(headers, f"/{folder_name}") #удалим тестовую папку

def test_create_folder_no_token(): #негативный тест на создание папки без токена
    folder_name = get_name("folder") #даем уникальное имя
    response = create_folder(None, folder_name)
    assert response.status_code == 401
    assert_error_response(response.json()) #проверка ответа об ошибке

def test_create_folder_without_name(headers): #негативный тест на создание папки без имени
    response = requests.put(RESOURCES_URL, headers=headers)
    assert response.status_code == 400
    assert_error_response(response.json()) #проверка ответа об ошибке