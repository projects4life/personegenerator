#!/usr/bin/env python3
from flask import Flask, render_template
import requests
import boto3
import json
from bs4 import BeautifulSoup
import os
import openai
import uuid
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address 


app = Flask(__name__)

limiter = Limiter(
    get_remote_address,
    app=app
)


# Index page
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/persona', methods=['GET'])
#@limiter.limit("5 per hour")
def persona():
    # Start loading screen until result is ready
    # Get random image
    image_file = get_random_image()
    image_data= get_image_info_from_aws(image_file)
    chat_gpt = send_info_to_chat_gpt(image_data)
    # Send image to aws
    # send result to chatgpt
    # Render all result with custom template(image, jsonBackground)
    # path = get_random_image()
    return render_template('persona.html',person_image=image_file,image_data=chat_gpt)



def get_random_image():
    """
    Gets a random image of a person generated by the website https://this-person-does-not-exist.com/en,
    saves it to a file named "random-face.jpg" in a directory called "images/", and returns nothing.

    This function sends a GET request to the website to get the URL of a randomly generated image of a person,
    parses the response using BeautifulSoup to find the image URL, sends a second GET request to get the image data,
    and saves the image data to a file named "random-face.jpg" in a directory called "images/".

    Args:
        None.

    Returns:
        File Path to The Image.
    """
    # Sending a request
    url = "https://this-person-does-not-exist.com/en"
    response = requests.get(url)
    # parsing the response 
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img", {"id": "avatar"})
    random_image_url=f"https://this-person-does-not-exist.com{img['src']}"
    # saving it into a file
    image = requests.get(random_image_url)
    # filename = "static/images/random-face.jpg"
    filename = f"static/images/random-face-{str(uuid.uuid4())}.jpg"
    with open(filename, "wb") as file:
        file.write(image.content)
    return filename

def get_image_info_from_aws(photo):
    '''
    Function Name: get_image_info_from_aws()

    Description:
    This function uses the AWS Rekognition service to detect faces in an image and extract information about the faces detected such as age, gender, and smile. The function takes no input parameters.

    Return:
    The function returns a string with the extracted information about the faces detected in the image. The string includes the smile value, age, and gender of each face detected.

    Libraries Used:
    The function uses the boto3 library to interact with the AWS Rekognition service.

    Usage:
    To use this function, you need to have an AWS account and have the boto3 library installed.

    Example:
    Output of the function call:
    Detected faces for photo.jpg
    The detected face is around 35.0
    gender: Male with 99.98998260498047%
    smile: False with 0.0009966576413214808%
    'smile: False, age~: 35.0, gender: Male'
    '''
    image_data={}
    client=boto3.client('rekognition')
    with open(photo, 'rb') as image:
            response = client.detect_faces(Image={'Bytes': image.read()},Attributes=['ALL'])
    
    #print('Detected faces for ' + photo)    
    for faceDetail in response['FaceDetails']:
        #print('The detected face is around ' + str(int(faceDetail['AgeRange']['Low']) + int(faceDetail['AgeRange']['High']) / 2 ))
        age = str(int(faceDetail['AgeRange']['Low']) + int(faceDetail['AgeRange']['High']) / 2 )
        #print("gender: " + str(faceDetail['Gender']['Value']) + " with " + str(faceDetail['Gender']['Confidence']) + "%" )
        gender = str(faceDetail['Gender']['Value'])
        #print("smile: " + str(faceDetail['Smile']['Value']) + " with " + str(faceDetail['Smile']['Confidence']) + "%" )
        smile = str(faceDetail['Smile']['Value'])
        #print(json.dumps(faceDetail, indent=4, sort_keys=True)) ##### to print the whole list
    
    image_data["age"]       = age
    image_data["gender"]    = gender
    image_data["smile"]     = smile
    return image_data

def send_info_to_chat_gpt(data_about_person):
    """
    This function send info to ChatGpt using the promt below:

    Please generate a background for a {data_about_person['gender']} character who is {data_about_person['age']} years old and is {is_smiling} in a portrait . Please provide information about his name job education, hobbies, personality, hometown, and background. give the response as a json the keys should start at uppercase.

    Then ChatGpt Respones with a json contains random information about the person.

    Args:
      data_about_person - a dictory contains three keys: age, gender, is_smiling, created by the get_image_info_from_aws function

    Output:
       The json response as chat gpt recived
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")
    is_smiling = "smiling" if data_about_person["smile"] == "True" else "not smiling"
    
    promt_to_chatGpt= f"Please generate a background for a {data_about_person['gender']} character who is {data_about_person['age']} years old and is {is_smiling} in a portrait . Please provide information about his name job education, hobbies, personality, hometown, and background. give the response as a json, the keys should start at uppercase"

    response = openai.Completion.create(
    model="text-davinci-003",
    prompt = promt_to_chatGpt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    
    json_repsonse = json.loads(response.choices[0].text)
    return json_repsonse
    

def render_result():
    return "soon implemented" 



if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)

