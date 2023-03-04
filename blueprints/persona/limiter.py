from flask_limiter import Limiter
from flask import request
import os

def get_proxy_remote_address():
    """
    :return: the ip address for the current request (or 127.0.0.1 if none found)
    """
    print("hey")
    if request.headers.get('X-Real-IP') != None:
        return str(request.headers.get('X-Real-IP'))
    return request.remote_addr or '127.0.0.1'


mongo_url = os.environ.get("MONGO_URL")
if mongo_url is None:
    mongo_url = "mongodb://root:root@localhost:27017" #URL for development

limiter = Limiter(key_func=get_proxy_remote_address,storage_uri=mongo_url)
