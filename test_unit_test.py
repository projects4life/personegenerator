import pytest
from app import * 
import os

# test for the get_random_image function
def test_get_random_image():
 # this function will check that image was recived and saved to the expected path
 get_random_image() 
 expected_path = "images/random-face.jpg"
 assert os.path.exists(expected_path)
 # Check that the saved file is a JPEG image
 # this will check the file itself and see if the file is ok
 with open(expected_path, "rb") as f:
    data = f.read()
    assert data[:2] == b"\xff\xd8"  # Check the first two bytes of the file for the JPEG magic number

def test_aws():
   # this will check that the following veriables have reecive some values
   # age is an int betwin 1 and 100
   result=get_image_info_from_aws(get_random_image())
   assert  1 < float(result["age"]) < 100 
   assert result["smile"] in ("True", "False")
   assert result["gender"] in ("Male", "Female")
