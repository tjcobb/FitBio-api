# weight.py
import pymongo
import os

from flask import Flask
app = Flask(__name__)

MongoClient = pymongo.MongoClient("mongodb+srv://tyjcobb:Neville0817!@tylercobbtestcluster-atvya.mongodb.net/test?retryWrites=true")
FitbioDB = MongoClient[os.environ["FITBIO_DB"]]
WeightCollection = FitbioDB[os.environ["WEIGHT_COLLECTION"]]

@app.route("/weight")
def hello():
    temp = {"name": "John", "address": "Highway 37"}
    return WeightCollection.insert_one(temp)
