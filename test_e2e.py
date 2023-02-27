import pytest
import requests
from bs4 import BeautifulSoup


ENDPOINT = "http://localhost:80"

# Test the ability of the application to generate an image and information and display it on the persona route
def test_persona_route():
    response = requests.get(f"{ENDPOINT}/persona")
    # parsing the response 
    soup = BeautifulSoup(response.text, "html.parser")
    print(soup)

test_persona_route()