from flask import Flask
import requests

app = Flask(__name__)


# Index page
@app.route('/', methods=['GET'])
def index():
    return 'soon be implemented'

# gets image from this person does not exists
def get_random_image():
    return "soon implemented"


def get_image_info_from_aws():
    return "soon implemented"

def send_info_to_chat_gpt():
    return "soon implemented"

def render_result():
    return "soon implemented" 
