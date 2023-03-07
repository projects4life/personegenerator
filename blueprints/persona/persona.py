from flask import Blueprint, render_template, request
from bs4 import BeautifulSoup
import requests
import os
import openai
import uuid
import boto3
import json
from .limiter import limiter
import pymongo

persona_page = Blueprint('persona_page', __name__, template_folder="templates",static_folder="static")

@persona_page.record
def on_load(state):
    """
    Load the flask application on the blueprint load
    used to start the limeter
    """
    global limiter
    app = state.app
    limiter.init_app(app)

@persona_page.route('/persona', methods=['GET'])
@limiter.limit("5 per hour")
def persona():
    return render_template("loading.html", user=False) #### becouse this is the free pass and i want it to count thier times

@persona_page.route('/personaR', methods=['GET']) ######this is here for the screen loader
@limiter.limit("5 per hour")
def personaR():
    return render_persona(False) ### let the html know that this request came from persona and not admin

def render_persona(user):
    """
    A Flask view function that generates a random persona using various helper functions and returns the rendered HTML template with the generated persona information.
    
    Example of image data to be rendered: 
    image_data={'Name': 'Adam Smith', 'Job': 'Student', 'Education': 'Preschool', 'Hobbies': ['Playing with Toys', 'Drawing', 'Making Music'], 'Personality': 'Energetic and Inquisitive', 'Hometown': 'New York City, USA', 'Background': 'Adam is a 4.5 year old student from New York City. He loves playing with toys, drawing and making music. He is an energetic and inquisitive kid who loves exploring the world around him. He loves spending time with his family, playing outside and learning new things.'}

    Returns:
    HTML template -- Rendered HTML template with the generated persona information.
    """
    image_file = get_random_image()
    image_data_aws= get_image_info_from_aws(image_file)
    image_data = send_info_to_chat_gpt(image_data_aws)

    # image_data={'Name': 'Adam Smith', 'Job': 'Student', 'Education': 'Preschool', 'Hobbies': ['Playing with Toys', 'Drawing', 'Making Music'], 'Personality': 'Energetic and Inquisitive', 'Hometown': 'New York City, USA', 'Background': 'Adam is a 4.5 year old student from New York City. He loves playing with toys, drawing and making music. He is an energetic and inquisitive kid who loves exploring the world around him. He loves spending time with his family, playing outside and learning new things.'}
    return render_template('persona.html',person_image=image_file,image_data=image_data["Background"],name=image_data['Name'], job=image_data["Job"], education=image_data["Education"], hobbies=image_data["Hobbies"], age=image_data["Age"], hometown=image_data["Hometown"], user=user)

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
        age = str(((int(faceDetail['AgeRange']['High']) - int(faceDetail['AgeRange']['Low'])) // 4) + int(faceDetail['AgeRange']['Low']))
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
    
    promt_to_chatGpt= f"fill in the missing sections for me... be creative. the age is {data_about_person['age']} and the gender is {data_about_person['gender']} all keys must start with capital letter\r\n\r\nName: (choose a name+ last name. dont use common names)\r\nAge: (what I provided)\r\nGender: (what I provided)\r\nHobbies: (at least 3. type string)\r\nJob: (according to the age and education)\r\nEducation: (only name of the degree if he/she got one. don't incloud location)\r\nBackground:  (no less than 75 words)\r\nHometown: (country,state,city)(choose places from all around the planet. string not list )\r\n\r\nPlease generate a JSON response with this information(make sure this is correct JSON), replace all the information with the instructions inside do not add sub-fields to location and education!!!!!"
    
    gpt_respose = chat_get_response(promt_to_chatGpt)

    ##### this is a hotfix for the prod env that will try to get a ajson respone from gebeta
    ##### if the data recived from gebeta is not valid the try up to $max_attempts times
    ##### if still faild rais an exeption
    max_attempts = 5
    attempts = 0
    json_response = None
    while attempts < max_attempts:
        try:
            json_response = json.loads(gpt_respose.choices[0].text)
            data = json_response["Background"]
            data = json_response["Hometown"]
            break  # exit the loop if successful
        except:
            attempts += 1  # increment attempts count if unsuccessful
            gpt_respose = chat_get_response(promt_to_chatGpt) # Regenearte a response with chat gpt
            if attempts == max_attempts:
                raise  # raise an exception if maximum attempts exceeded
    
    return json_response
    
def chat_get_response(promt_to_chatGpt):
    """
    This Function sends a promt to chatGpt and return the response
    """
    respone = openai.Completion.create(
    model="text-davinci-003",
    prompt = promt_to_chatGpt,
    temperature=0.7,
    max_tokens=256,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    return respone