import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")

def get_headers():

    headers = {
        "Authorization": "OAuth " + token
    }
    
    return headers
    