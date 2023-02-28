import pytest
import requests
from bs4 import BeautifulSoup
import re

ENDPOINT = "http://localhost:80"
LIMIT = 5

def test_limitter():
    for i in range(LIMIT):
        response = requests.get(f"{ENDPOINT}/persona")
        #assert response.status_code == 200 # untill gebeta is ok this is like this
    
    response = requests.get(f"{ENDPOINT}/persona")
    print(response)
    assert response.status_code == 429
