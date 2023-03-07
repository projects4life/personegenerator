import pytest
import requests
from bs4 import BeautifulSoup
import re
import os
import subprocess

username = os.environ.get("APP_USER")
password = os.environ.get("APP_PASSWORD")


ENDPOINT = "http://localhost:80"
LIMIT = 5

def test_limitter():
    ###check that the first 5 times are ok
    for i in range(LIMIT):
        response = requests.get(f"{ENDPOINT}/persona")
        assert response.status_code == 200 
    
    #check that the 6 time is returning 429
    response = requests.get(f"{ENDPOINT}/persona")
    print(response)
    assert response.status_code == 429


    for i in range(LIMIT):
        response = requests.get(f"{ENDPOINT}/personaR")
        assert response.status_code == 200 
    
    response = requests.get(f"{ENDPOINT}/personaR")
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
