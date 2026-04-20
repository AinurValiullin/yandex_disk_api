import requests
from config.base import RESOURCES_URL
from utils.assertions import assert_error_response, assert_resources_structure, assert_resources_items
from client.yandex_disk_api_client import get_resources

def test_resources_status_code(headers): #тест статус кода ответа
    assert get_resources(headers, "/").status_code == 200

def test_resources_check_response(headers): #теста ответа сервера
    data = get_resources(headers, "/").json() #присваиваем переменной data JSON ответа сервера 
    assert_resources_structure(data)

def test_resources_items_fields(headers): #тест соответвия элементов списка items (поля)
    data = get_resources(headers, "/").json()
    assert_resources_items(data)    

def test_unauthorized(): #негативный тест на отсутствие токена
    response = get_resources(None, "/")
    assert response.status_code == 401
    assert_error_response(response.json()) #проверка ответа об ошибке

def test_without_path(headers): #негативный тест на отсутствие пути(path)
    response = requests.get(RESOURCES_URL, headers=headers)
    assert response.status_code == 400
    assert_error_response(response.json()) #проверка ответа об ошибке

def test_invalid_path(headers): #негативный тест на несущуствующий путь
    response = get_resources(headers, "/invalid_folder_123456789")
    assert response.status_code == 404
    assert_error_response(response.json()) #проверка ответа об ошибке