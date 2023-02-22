from flask import Flask
import requests
import boto3

app = Flask(__name__)

# Index page
@app.route('/', methods=['GET'])
def index():
    return 'soon be implemented'

# gets image from this person does not exists
def get_random_image():
    return "soon implemented"


def get_image_info_from_aws():
    photo="photo.png"
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
        response = client.detect_labels(Image={'Bytes': image.read()})
        
    print('Detected labels in ' + photo)    
    for label in response['Labels']:
        print (label['Name'] + ' : ' + str(label['Confidence']))

    return len(response['Labels'])

def send_info_to_chat_gpt():
    return "soon implemented"

def render_result():
    return "soon implemented" 


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
