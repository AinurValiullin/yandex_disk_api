import time
import uuid
from client.yandex_disk_api_client import create_folder, get_resources, delete, copy
from utils.assertions import assert_operation_response, assert_resources_structure, assert_resources_items, assert_error_response

def get_name(prefix="folder"):
    return f"{prefix}_{uuid.uuid4().hex[:8]}"

def create_and_check_folder(headers, path): #фунция создания и проверки папки
    create_response = create_folder(headers, path) #создадим тестовую папку
    assert create_response.status_code == 201 #проверка статус кода ответа на создание папки
    assert_operation_response(create_response.json()) #проверка успешного (201) ответа сервера JSON
    get_response = get_resources(headers, path) #через get перепроверим что папка точно создалась
    assert get_response.status_code == 200 #проверка статус кода ответа на get
    assert_resources_structure(get_response.json()) #проверка успешного ответа (200) сервера
    assert_resources_items(get_response.json()) #проверка успешного ответа (200) сервера

def delete_and_check(headers, path): #функция для удаления
    del_response = delete(headers, path) #удаляем
    assert del_response.status_code in [200, 202, 204] #проверка статус кода ответа
    for _ in range(5): #иногда тест падает из за асинхронности (не мгновенное удаление), поэтому добавил повтор
        check = get_resources(headers, path) #через get проверим что папка точно удалилась
        if check.status_code == 404:
            return
        else:
            time.sleep(1) #усыпляем на 1 сек
    assert check.status_code == 404
    assert_error_response(check.json()) #проверка ответа сервера об ошибке

def copy_and_check_folder(headers, source_path, target_path): #функция копирования
    copy_response = copy(headers, source_path, target_path) #создадим копию
    assert copy_response.status_code in [201, 202] #проверка статус кода ответа
    assert_operation_response(copy_response.json()) #проверка успешного (201) ответа сервера JSON
    get_response = get_resources(headers, target_path) #через get перепроверим что папка точно создалась
    assert get_response.status_code == 200 #проверка статус кода ответа на get
    data = get_response.json()
    assert_resources_structure(data) #проверка успешного ответа (200) сервера
    assert_resources_items(data) #проверка успешного ответа (200) сервера

def copy_expect_error(headers, source_path, target_path, status_code): #функция копирования для негативных тестов
    response = copy(headers, source_path, target_path)
    assert response.status_code == status_code
    assert_error_response(response.json()) #проверка ответа сервера об ошибке