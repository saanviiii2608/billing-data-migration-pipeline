import requests

API_URL = "https://httpbin.org/post"

def upload_record(record):

    response = requests.post(API_URL, json=record)

    if response.status_code == 200:
        return True

    return False