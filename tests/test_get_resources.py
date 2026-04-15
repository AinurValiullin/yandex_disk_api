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
    assert isinstance(data, dict)
    assert "_embedded" in data #проверка что в ответе есть embedded
    assert "items" in data["_embedded"] #проверка что есть итемс в ответе в поле embedded
    items = data["_embedded"]["items"]
    assert isinstance(items, list) #проверка что итемс это список
    
    assert "error" not in data

    for item in items:
        assert "name" in item
        assert "type" in item
        assert item["type"] in ["file", "dir"]
        assert "path" in item
        assert "created" in item
        assert "modified" in item
        assert "resource_id" in item
        assert "revision" in item
        assert "comment_ids" in item
        assert isinstance(item["name"], str)
        assert isinstance(item["type"], str)
        assert isinstance(item["path"], str)