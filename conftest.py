import pytest
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

@pytest.fixture
def headers():
    return {
        "Authorization": "OAuth " + token
    }
