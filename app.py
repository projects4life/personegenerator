#!/usr/bin/env python3
from flask import Flask
import requests
import boto3
import json

app = Flask(__name__)

# Index page
@app.route('/', methods=['GET'])
def index():
    print(get_image_info_from_aws())
    return 'soon be implemented'

# gets image from this person does not exists
def get_random_image():
    return "soon implemented"


def get_image_info_from_aws():
    
    photo="photo.jpg"
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
            response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    
    print('Detected faces for ' + photo)    
    for faceDetail in response['FaceDetails']:
        print('The detected face is between ' + str(faceDetail['AgeRange']['Low']) 
              + ' and ' + str(faceDetail['AgeRange']['High']) + ' years old')
        print("gender" + str(faceDetail['Gender']['Value']) + "with" + str(faceDetail['Gender']['Confidence']) + "%" )
        print('Here are the other attributes:')
        #print(json.dumps(faceDetail, indent=4, sort_keys=True))

def send_info_to_chat_gpt():
    return "soon implemented"

def render_result():
    return "soon implemented" 


# def get_fields(data):
#     data = json.load(data)
#     gender = data['Gender']['Value']
#     smile = None
#     if 'Smile' in data:
#         smile = data['Smile']['Value']
#     age = (data['AgeRange']['High'] + data['AgeRange']['Low']) // 2

#     # Print the extracted fields
#     print(f"Gender: {gender}")
#     print(f"Smile: {smile}")
#     print(f"Age: {age}")

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
