
def assert_error_response(data): #функция для теста ответа сервера об ошибке
    assert isinstance(data, dict)
    assert "error" in data #проверка обязательных полей в ответе
    assert "description" in data #проверка обязательных полей в ответе
    assert "message" in data #проверка обязательных полей в ответе
    assert isinstance(data["error"], str) #проверка что корректный тип значения
    assert isinstance(data["description"], str) #проверка что корректный тип значения
    assert isinstance(data["message"], str) #проверка что корректный тип значения

def assert_operation_response(data): 
    assert isinstance(data, dict)
    assert "method" in data
    assert "href" in data
    assert isinstance(data["method"], str)
    assert isinstance(data["href"], str)

def assert_resources_structure(data):
    assert isinstance(data, dict) #проверяем что ответ соответствует структуре ключ-значение (JSON)
    assert "_embedded" in data #проверка что в ответе есть embedded
    assert "items" in data["_embedded"] #проверка что есть итемс в ответе в поле embedded
    items = data["_embedded"]["items"] #присваиваем переменной items список items с ответа
    assert isinstance(items, list) #проверка что итемс это список
    assert "error" not in data #проверяем что в JSON ответе нет ключа "error"
        
def assert_resources_items(data):
    items = data["_embedded"]["items"] #присваиваем переменной items список items с ответа
    for item in items: #проходимся по элементам списка
        assert "name" in item #проверка обязательных полей в ответе
        assert "type" in item #проверка обязательных полей в ответе
        assert "path" in item #проверка обязательных полей в ответе
        assert "created" in item #проверка обязательных полей в ответе
        assert "modified" in item #проверка обязательных полей в ответе
        assert "resource_id" in item #проверка обязательных полей в ответе
        assert "revision" in item #проверка обязательных полей в ответе
        assert "comment_ids" in item #проверка обязательных полей в ответе
        assert item["type"] in ["file", "dir"] #проверка что корректный тип значения 
        assert isinstance(item["name"], str) #проверка что корректный тип значения
        assert isinstance(item["type"], str) #проверка что корректный тип значения
        assert isinstance(item["path"], str) #проверка что корректный тип значения