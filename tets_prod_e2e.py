import pytest
import requests
from bs4 import BeautifulSoup
import re

ENDPOINT = "http://localhost:80"
LIMIT = 5

# def test_limitter():
#     for i in range(LIMIT):
#         response = requests.get(f"{ENDPOINT}/persona")
#         #assert response.status_code == 200 # untill gebeta is ok this is like this
    
#     response = requests.get(f"{ENDPOINT}/persona")
#     print(response)
#     assert response.status_code == 429

def test_login():
    payload = {
    "email": "MENI",
    "password": "MAMTERA"
    }
    payload2 = {
    "email": "meni",
    "password": "MAMTERA"
    }
    response = requests.get(f"{ENDPOINT}/admin")
    print(response.status_code)
    assert response.status_code == 200

    response = requests.post(f"{ENDPOINT}/login" , data=payload2)
    assert response.status_code == 401

    response = requests.post(f"{ENDPOINT}/login" , data=payload)
    assert response.status_code == 200
