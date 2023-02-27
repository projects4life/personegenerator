import pytest
import requests
from bs4 import BeautifulSoup
import re

ENDPOINT = "http://localhost:80"

# Test the ability of the application to generate an image and information and display it on the persona route
def test_persona_route():
    response = requests.get(f"{ENDPOINT}/persona")
    # parsing the response 
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", {"id": "avatar"})
    assert re.match("static/images/.*", img["src"])


# test_persona_route()