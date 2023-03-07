import pytest
from blueprints.persona.persona import get_random_image,get_image_info_from_aws,send_info_to_chat_gpt
import os
from PIL import Image

def test_get_random_image():
 """
 Test for getting random image and verifying this is a valid image.
 test for >> def  get_random_image()
 """
 expected_path = get_random_image() 
 assert os.path.exists(expected_path)
 assert is_jpeg(expected_path) == True # Check the the generate file is an image

def test_aws():
   """
   This will check that the following veriables have reecive some values
   age is an int betwin 1 and 100
   smile = true or false
   gender = male or female
   """
   result=get_image_info_from_aws(get_random_image())
   assert  1 <= float(result["age"]) <= 100 
   assert result["smile"] in ("True", "False")
   assert result["gender"] in ("Male", "Female")

def test_chatgpt_generate_logical_response():
   """
   Test to verify the ChatGpt returns a json with the expected fields
   """
   data = send_info_to_chat_gpt(get_image_info_from_aws(get_random_image()))
   assert verify_gpt_response_contains_expected_fields(data) == True

def is_jpeg(filename):
    """Check if a file is a JPEG image."""
    try:
        with Image.open(filename) as img:
            return True
    except IOError:
        return False

def verify_gpt_response_contains_expected_fields(data):
    """Verify that the response from GPT contains all expected fields."""
    expected_fields = ['Name', 'Job', 'Education', 'Hobbies', 'Age', 'Hometown', 'Background']
    for field in expected_fields:
        if field not in data:
            return False
    return True
