import pytest
import requests
from bs4 import BeautifulSoup
import re

ENDPOINT = "http://localhost:8080"

# Test the ability of the application to generate an image and information and display it on the persona route
def test_persona_route():
    response = requests.get(f"{ENDPOINT}/personaR")
    # parsing the response 
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", {"id": "avatar"})
    print(img)
    assert re.match("static/images/.*", img["src"])