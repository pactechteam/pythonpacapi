from flask import Flask
from flask import request
from dotenv import load_dotenv
load_dotenv()
import os
SECRET_KEY = os.getenv("pythonapi")


app = Flask(__name__)

global tempTest
tempTest = 'Hello fellow PACers!'

@app.route('/')
def index():
    global tempTest
    return tempTest



@app.route('/create',methods=["POST"])
def create():
    params = request.json
    if SECRET_KEY == params["key"]:
        global tempTest
        tempTest  = params["name"]
    return 'complete'
