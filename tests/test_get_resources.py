import requests
from config.base import RESOURCES_URL
from utils.assertions import assert_error_response
from client.yandex_disk_api_client import get_resources

def test_resources_status_code(headers): #тест статус кода ответа
    assert get_resources(headers, "/").status_code == 200

def test_resources_check_response(headers): #теста ответа сервера
    data = get_resources(headers, "/").json() #присваиваем переменной data JSON ответа сервера 
    assert isinstance(data, dict) #проверяем что ответ соответствует структуре ключ-значение (JSON)
    assert "_embedded" in data #проверка что в ответе есть embedded
    items = data["_embedded"]["items"] #в переменную items сохраняем список файлов/папок из ответа
    assert "items" in data["_embedded"] #проверка что есть итемс в ответе в поле embedded
    assert isinstance(items, list) #проверка что итемс это список
    assert "error" not in data #проверяем что в JSON ответе нет ключа "error"

def test_resources_items_fields(headers): #тест соответвия элементов списка items (поля)
    data = get_resources(headers, "/").json()
    items = data["_embedded"]["items"] #присваиваем переменной items список items с ответа
    for item in items: #проходимся по элементам списка
        assert "name" in item #проверка обязательных полей в ответе
        assert "type" in item #проверка обязательных полей в ответе
        assert item["type"] in ["file", "dir"] #проверка что корректный тип значения 
        assert "path" in item #проверка обязательных полей в ответе
        assert "created" in item #проверка обязательных полей в ответе
        assert "modified" in item #проверка обязательных полей в ответе
        assert "resource_id" in item #проверка обязательных полей в ответе
        assert "revision" in item #проверка обязательных полей в ответе
        assert "comment_ids" in item #проверка обязательных полей в ответе

def test_resources_items_correct_types(headers):  #тест соответвия элементов списка items (типы)
    data = get_resources(headers, "/").json()
    items = data["_embedded"]["items"] #присваиваем переменной items список items с ответа
    for item in items: #проходимся по элементам списка
        assert isinstance(item["name"], str) #проверка что корректный тип значения
        assert isinstance(item["type"], str) #проверка что корректный тип значения
        assert isinstance(item["path"], str) #проверка что корректный тип значения

def test_unauthorized(): #негативный тест на отсутствие токена
    response = get_resources(None, "/")
    assert response.status_code == 401
    data = response.json()
    assert_error_response(data)

def test_without_path(headers): #негативный тест на отсутствие пути(path)
    response = requests.get(RESOURCES_URL, headers=headers)
    assert response.status_code == 400
    data = response.json()
    assert_error_response(data)

def test_invalid_path(headers): #негативный тест на несущуствующий путь
    response = get_resources(headers, "/invalid_folder_123456789")
    assert response.status_code == 404 
    data = response.json()
    assert_error_response(data)