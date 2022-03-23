from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import numpy
import tensorflow as tf
import requests
import subprocess
import json

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongodb://db:27017")
db = client.IRG   ## New database
users = db["Users"]  ## collection users


def UserExist(username):
    #if users.find({"Username":username}).count_documents({}) == 0: ## if count =0, then there is no user in db
    if users.count_documents({"Username":username})==0:
        return False
    else:
        return True

class Register(Resource):
    def post(self):
        #Step 1 is to get posted data by the user
        postedData = request.get_json()

        #Get the data
        username = postedData["username"]
        password = postedData["password"] #"123xyz"


        if UserExist(username):
            retJson = {
                'status':301,
                'msg': 'Invalid Username'
            }
            return jsonify(retJson)

        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        #Store username and pw into the database
        users.insert_one({
            "Username": username,
            "Password": hashed_pw,
            "Tokens":10
        })

        retJson = {
            "status": 200,
            "msg": "You successfully signed up for the API"
        }
        return jsonify(retJson)

def verifyPw(username, password):
    if not UserExist(username):
        return False

    hashed_pw = users.find({
        "Username":username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def generateReturnDictionary(status, msg):
    retJson = {
        "status": status,
        "msg": msg
    }
    return retJson

def verifyCredentials(username, password):
    if not UserExist(username):
        return generateReturnDictionary(301, "Invalid Username"), True

    correct_pw = verifyPw(username, password)

    if not correct_pw:
        return generateReturnDictionary(302, "Incorrect Password"), True

    return None, False


class Classify(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        url = postedData["url"]  ## Image url that we want to classify (should be in jpg)

        retJson, error = verifyCredentials(username, password)
        if error:
            return jsonify(retJson)

        tokens = users.find({
            "Username":username
        })[0]["Tokens"]

        if tokens<=0:
            return jsonify(generateReturnDictionary(303, "Not Enough Tokens"))

#### ################ Below code-- To implement classify_image model ####################
        # Step 1:  get url of the image
        r = requests.get(url)
        retJson = {}
        #Step 2: Open temp.jpg file and save url content in that file
        with open('temp.jpg', 'wb') as f:
            f.write(r.content)

            ## Step 3:  subprocess is the classify_image.py file with --model_dir path and --image_file path
            ## # make changes in the classify_image model to provide txt file with json content
            proc = subprocess.Popen('python classify_image.py --model_dir=. --image_file=./temp.jpg', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
            ret = proc.communicate()[0]
            proc.wait() # wait for the subprocess to cget complete

            ## Step 4: classify_image.py will provide a text.txt file--

            with open("text.txt") as g:
                retJson = json.load(g)

################################################################
        users.update_one({
            "Username": username
        },{
            "$set":{
                "Tokens": tokens-1
            }
        })

        return retJson


class Refill(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["admin_pw"]
        amount = postedData["amount"]

        if not UserExist(username):
            return jsonify(generateReturnDictionary(301, "Invalid Username"))

        correct_pw = "abc123"
        if not password == correct_pw:
            return jsonify(generateReturnDictionary(302, "Incorrect Password"))

        users.update_one({
            "Username": username
        },{
            "$set":{
                "Tokens": amount
            }
        })
        return jsonify(generateReturnDictionary(200, "Refilled"))


api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')

if __name__=="__main__":
    app.run(host='0.0.0.0')
