import pytest
import requests
from bs4 import BeautifulSoup
import re

ENDPOINT = "http://localhost:8080"

# Test the ability of the application to generate an image and information and display it on the persona route
def test_persona_route():
    timeout_seconds = 60 

    try:
        response = requests.get(f"{ENDPOINT}/personaR", timeout=timeout_seconds)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, "html.parser")
        img = soup.find("img", {"id": "avatar"})
        print(img)
        assert re.match("static/images/.*", img["src"])
    except ConnectionError as e:
        print(f"ConnectionError: {e}")