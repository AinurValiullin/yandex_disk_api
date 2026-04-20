from utils.helpers import get_name
from client.yandex_disk_api_client import get_resources
from utils.assertions import assert_error_response
from utils.helpers import create_and_check_folder, delete_and_check, copy_and_check_folder, copy_expect_error

def test_copy_folder(headers): #позитивный тест на создание копии папки
    folder_name = get_name("folder") #даем уникальное имя
    create_and_check_folder(headers, folder_name) #создаем папку (с проверками)
    copy_folder_name = f"copy_{folder_name}" #даем уникальное имя
    copy_and_check_folder(headers, folder_name, copy_folder_name) #создадим копию (с проверкой)
    delete_and_check(headers, folder_name) #удалим тестовую папку (с проверками)
    delete_and_check(headers, copy_folder_name) #удалим тестовую папку (с проверками)

def test_copy_to_existing_folder(headers): #негативный тест на копирование папки уже существующую
    folder_name = get_name() #даем уникальное имя
    copy_folder_name = f"copy_{folder_name}" #даем уникальное имя
    create_and_check_folder(headers, folder_name) #создаем папку (с проверками)
    create_and_check_folder(headers, copy_folder_name) #создаем папку (с проверками)
    before = get_resources(headers, copy_folder_name).json()
    copy_expect_error(headers, folder_name, copy_folder_name, 409)
    after = get_resources(headers, copy_folder_name).json()
    assert before["_embedded"]["items"] == after["_embedded"]["items"] #сравниваем JSON существующей папки до и после копирования (на случай если копирование перезаписало его)
    delete_and_check(headers, folder_name) #удалим тестовую папку (с проверками)
    delete_and_check(headers, copy_folder_name) #удалим тестовую папку (с проверками)

def test_copy_from_non_existing_folder(headers): #негативный тест на копирование не существующий папки
    folder_name = get_name() #даем уникальное имя
    copy_folder_name = f"copy_{folder_name}" #даем уникальное имя
    copy_expect_error(headers, folder_name, copy_folder_name, 404)
    check_copy = get_resources(headers, copy_folder_name)
    assert check_copy.status_code == 404
    assert_error_response(check_copy.json())
    
def test_copy_without_token(headers): #негативный тест на копирование без токена
    folder_name = get_name() #даем уникальное имя
    copy_folder_name = f"copy_{folder_name}" #даем уникальное имя
    create_and_check_folder(headers, folder_name)
    copy_expect_error(None, folder_name, copy_folder_name, 401)
    delete_and_check(headers, folder_name) #удалим тестовую папку (с проверками)