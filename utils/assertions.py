
def assert_error_response(data): #функция для теста ответа сервера об ошибке
    assert isinstance(data, dict)
    assert "error" in data #проверка обязательных полей в ответе
    assert "description" in data #проверка обязательных полей в ответе
    assert "message" in data #проверка обязательных полей в ответе
    assert isinstance(data["error"], str) #проверка что корректный тип значения
    assert isinstance(data["description"], str) #проверка что корректный тип значения
    assert isinstance(data["message"], str) #проверка что корректный тип значения

def assert_create_folder_response(data): 
    assert isinstance(data, dict)
    assert "method" in data
    assert "href" in data
    assert isinstance(data["method"], str)
    assert isinstance(data["href"], str)

def assert_copy_folder_response(data): 
    assert isinstance(data, dict)
    assert "method" in data
    assert "href" in data
    assert isinstance(data["method"], str)
    assert isinstance(data["href"], str)