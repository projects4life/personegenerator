from flask import Flask
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)


# Index page
@app.route('/', methods=['GET'])
def index():
    return 'soon be implemented'

# gets image from this person does not exists
def get_random_image():
    # Sending a get request to get the image url
    url = "https://this-person-does-not-exist.com/en"
    response = requests.get(url)
    # parsing the response using BeautifulSoup to find the image url 
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", {"id": "avatar"})
    random_image_url=f"https://this-person-does-not-exist.com{img['src']}"

    print(random_image_url)
    
    # sending a request to get the generated image and saving it to a file 
    image = requests.get(random_image_url)
    filename = "images/random-face.jpg"
    with open(filename, "wb") as file:
        file.write(image.content)

    

    
    return "soon will work"

def get_image_info_from_aws():
    return "soon implemented"

def send_info_to_chat_gpt():
    return "soon implemented"

def render_result():
    return "soon implemented" 



if __name__ == '__main__':
    get_random_image()
    app.run(host='0.0.0.0',debug=True)
