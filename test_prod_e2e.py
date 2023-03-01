import pytest
import requests
from bs4 import BeautifulSoup
import re
import os
import subprocess

username = os.environ.get("APP_USER")
password = os.environ.get("APP_PASSWORD")

ENDPOINT = "http://localhost:5000"
LIMIT = 1

def test_limitter():
    for i in range(LIMIT):
        response = requests.get(f"{ENDPOINT}/persona")
        #assert response.status_code == 200 # untill gebeta is ok this is like this
    
    response = requests.get(f"{ENDPOINT}/persona")
    print(response)
    assert response.status_code == 429

def test_login():
    payload = {
    "email": username,
    "password": password

    }

    payload2 = {
    "email": "STUFF",
    "password": "TO TESTS"
    }

    response = subprocess.check_output(['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', ENDPOINT + '/admin'])
    response = int(response.decode().strip())
    assert response == 302

    response = requests.post(f"{ENDPOINT}/login" , data=payload2)
    assert response.status_code == 401

    response = requests.post(f"{ENDPOINT}/login" , data=payload)
    assert response.status_code == 200
