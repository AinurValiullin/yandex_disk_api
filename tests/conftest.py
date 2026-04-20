import pytest
import requests
import os
from dotenv import load_dotenv
from config.base import RESOURCES_URL
from config.base import get_name

load_dotenv()

token = os.getenv("TOKEN")

@pytest.fixture
def headers():
    return {
        "Authorization": "OAuth " + token
    }

# @pytest.fixture
# def create_folder(headers):
#     return requests.put(RESOURCES_URL, headers=headers, params={"path":f"{get_name()}"})