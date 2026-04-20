from config.base import get_name
from client.yandex_disk_api_client import create_folder, get_resources, delete
from utils.assertions import assert_create_folder_response, assert_error_response

def test_delete_folder(headers): #позитивный тест проверки удаление папки
    folder_name = get_name("folder") 
    response = create_folder(headers, folder_name) #создаем тестовую папку
    assert response.status_code == 201
    assert_create_folder_response(response.json()) #проверка JSON ответа 

    get_response = get_resources(headers, f"/{folder_name}") #через get проверим что папка точно создалась
    assert get_response.status_code == 200
    
    del_response = delete(headers, f"/{folder_name}") #удалим тестовую папку
    assert del_response.status_code in [200, 202, 204]
    
    get_response = get_resources(headers, f"/{folder_name}") #через get проверим что папка точно удалилась
    assert get_response.status_code == 404
    assert_error_response(get_response.json()) #проверка ответа об ошибке    

def test_delete_folder_non_empty(headers): #позитивный тест на удаление не пустой папки
    folder_name = get_name("folder")
    second_folder = get_name("second_folder")
    first_response = create_folder(headers, folder_name) #создаем первую тестовую папку
    assert first_response.status_code == 201
    assert_create_folder_response(first_response.json()) #проверка JSON ответа 

    second_response = create_folder(headers, f"{folder_name}/{second_folder}") #создаем вторую тестовую папку внутри первой
    assert second_response.status_code == 201
    assert_create_folder_response(second_response.json()) #проверка JSON ответа 

    del_response = delete(headers, f"/{folder_name}") #удалим первую папку
    assert del_response.status_code in [200, 202, 204]
    import time
    time.sleep(1) #иногда тест падает потому что не успевает удаляться папка поэтому поставил на повтор
    get_response = get_resources(headers, f"/{folder_name}") #через get проверим что папка точно удалилась
    assert get_response.status_code == 404
    assert_error_response(get_response.json()) #проверка ответа об ошибке    

def test_delete_non_exist_folder(headers): #негативный тест проверки удаления несуществ папки
    folder_name = get_name()

    del_response = delete(headers, f"/{folder_name}")
    assert del_response.status_code == 404
    assert_error_response(del_response.json()) #проверка ответа об ошибке

def test_delete_no_token(): #негативный тест на удаление папки без токена
    folder_name = get_name()
    del_response = delete(None, f"/{folder_name}") #удаляем папку без токена
    assert del_response.status_code == 401
    assert_error_response(del_response.json()) #проверка ответа об ошибке

def test_delete_folder_twice(headers): #негативный тест на повторное удаление папки
    folder_name = get_name("folder") 
    response = create_folder(headers, folder_name) #создаем тестовую папку
    assert response.status_code == 201
    assert_create_folder_response(response.json()) #проверка JSON ответа 

    get_response = get_resources(headers, f"/{folder_name}") #через get проверим что папка точно создалась
    assert get_response.status_code == 200

    first_del_response = delete(headers, f"/{folder_name}") #удалим тестовую папку
    assert first_del_response.status_code in [200, 202, 204]

    second_del_response = delete(headers, f"/{folder_name}") #повторно удалим тестовую папку
    assert second_del_response.status_code == 404