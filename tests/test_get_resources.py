import requests
from config.base import RESOURCES_URL
from config.auth import get_headers

def test_get_files():
    params = {
        "path": "/"
    }

    response = requests.get(url=RESOURCES_URL, headers=get_headers(), params=params)
    assert response.status_code == 200 #проверка что код в ответе 200

    data = response.json()
    assert "_embedded" in data #проверка что в ответе есть embedded
    assert "items" in data["_embedded"] #проверка что есть итемс в ответе в поле embedded
    items = data["_embedded"]["items"]
    assert type(items) is list #проверка что итемс это список