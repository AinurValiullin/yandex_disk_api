import requests
from config.base import RESOURCES_URL
from config.auth import get_headers

def test_get_files():
    params = {
        "path": "/"
    }

    response = requests.get(url=RESOURCES_URL, headers=get_headers(), params=params)
    assert response.status_code == 200 #проверка что код в ответе 200

    data = response.json() #сохраняем в переменную data json ответа
    assert isinstance(data, dict) #проверяем что ответ соответствует структуре ключ-значение (JSON)
    assert "_embedded" in data #проверка что в ответе есть embedded
    assert "items" in data["_embedded"] #проверка что есть итемс в ответе в поле embedded
    items = data["_embedded"]["items"] #в переменную items сохраняем список файлов/папок из ответа
    assert isinstance(items, list) #проверка что итемс это список
    
    assert "error" not in data #проверяем что в JSON ответе нет ключа "error"

    for item in items: #проходимся по элементам списка
        assert "name" in item #проверка обязательныъ полей в ответе
        assert "type" in item #проверка обязательныъ полей в ответе
        assert item["type"] in ["file", "dir"] #проверка что корректный тип значения 
        assert "path" in item #проверка обязательныъ полей в ответе
        assert "created" in item #проверка обязательныъ полей в ответе
        assert "modified" in item #проверка обязательныъ полей в ответе
        assert "resource_id" in item #проверка обязательныъ полей в ответе
        assert "revision" in item #проверка обязательныъ полей в ответе
        assert "comment_ids" in item #проверка обязательныъ полей в ответе
        assert isinstance(item["name"], str) #проверка что корректный тип значения
        assert isinstance(item["type"], str) #проверка что корректный тип значения
        assert isinstance(item["path"], str) #проверка что корректный тип значения