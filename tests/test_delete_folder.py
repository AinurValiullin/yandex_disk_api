from client.yandex_disk_api_client import get_resources, delete
from utils.assertions import assert_error_response
from utils.helpers import create_and_check_folder, delete_and_check, get_name

def test_delete_folder(headers): #позитивный тест проверки удаление папки
    folder_name = get_name("folder") #даем уникальное имя
    create_and_check_folder(headers, folder_name) #создаем папку (с проверками)
    delete_and_check(headers, folder_name) #удалим тестовую папку (с проверками)

def test_delete_folder_non_empty(headers): #позитивный тест на удаление не пустой папки
    folder_name = get_name("folder") #даем уникальное имя
    second_folder = get_name("second_folder") #даем уникальное имя
    create_and_check_folder(headers, folder_name) #создаем папку (с проверками)
    create_and_check_folder(headers, f"{folder_name}/{second_folder}") #создаем папку (с проверками)
    delete_and_check(headers, folder_name) #удалим тестовую папку (с проверками)   

def test_delete_non_exist_folder(headers): #негативный тест проверки удаления несуществ папки
    folder_name = get_name() #даем уникальное имя
    check = get_resources(headers, folder_name) #проверим что нету такой папки
    assert check.status_code == 404 
    assert_error_response(check.json()) #проверка ответа об ошибке
    del_response = delete(headers, folder_name) #удаляем несуществующую папку
    assert del_response.status_code == 404
    assert_error_response(del_response.json()) #проверка ответа об ошибке

def test_delete_no_token(): #негативный тест на удаление папки без токена
    folder_name = get_name() #даем уникальное имя
    del_response = delete(None, folder_name) #удаляем папку без токена
    assert del_response.status_code == 401
    assert_error_response(del_response.json()) #проверка ответа об ошибке

def test_delete_folder_twice(headers): #негативный тест на повторное удаление папки
    folder_name = get_name("folder") #даем уникальное имя
    create_and_check_folder(headers, folder_name) #создаем папку (с проверками)
    delete_and_check(headers, folder_name) #удалим тестовую папку (с проверками)  
    second_del_response = delete(headers, folder_name) #повторно удалим тестовую папку
    assert second_del_response.status_code in [404, 202]
    if second_del_response.status_code == 404:
        assert_error_response(second_del_response.json()) #проверка ответа об ошибке