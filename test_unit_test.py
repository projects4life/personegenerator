import pytest
from app import * 
import os

# test for the get_random_image function
def test_get_random_image():
 get_random_image() 
 expected_path = "images/random-face.jpg"
 assert os.path.exists(expected_path)
 # Check that the saved file is a JPEG image

 with open(expected_path, "rb") as f:
    data = f.read()
    assert data[:2] == b"\xff\xd8"  # Check the first two bytes of the file for the JPEG magic number

def test_aws():
   result=get_image_info_from_aws(get_random_image())
   assert  1 < float(result["age"]) < 100 
   assert result["smile"] in ("True", "False")
   assert result["gender"] in ("Male", "Female")

def test_chatgpt_generate_logical_response():
   data = send_info_to_chat_gpt(get_image_info_from_aws(get_random_image()))

   # assert that all keys are in the dictionary
   assert 'Name' in data.keys()
   assert 'Job' in data.keys()
   assert 'Education' in data.keys()
   assert 'Hobbies' in data.keys()
   assert 'Personality' in data.keys()
   assert 'Hometown' in data.keys()
   assert 'Background' in data.keys()

