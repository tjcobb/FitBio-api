# app.py
import pymongo
import os
from flask import Flask, jsonify, request
app = Flask(__name__)

MongoClient = pymongo.MongoClient("mongodb+srv://fitbio-app:RIAUhKkDs4mVwHFH@tylercobbtestcluster-atvya.mongodb.net/test?retryWrites=true")
FitbioDB = MongoClient[os.environ["FITBIO_DB"]]
WeightCollection = FitbioDB[os.environ["WEIGHT_COLLECTION"]]


@app.route("/weight/<string:user_id>", methods=["GET"])
def get_weight(user_id):
    # TODO - user validation
    print(request.headers)
    print("Getting weights for {0}".format(user_id))
    res = WeightCollection.find_one({"user_id": user_id}) or {}

    # ObjectId not serializable, there is probably a better way to do this
    if "_id" in res:
        res["_id"] = str(res["_id"])

    return jsonify(res)


@app.route("/weight", methods=["POST"])
def insert_weight():
    print(request.headers)

    # TODO - Input validation
    # TODO - Sort by date?
    # TODO - Consider max doc size of 16MB if we are storing all weights for someone in single doc
    existing = WeightCollection.find_one({"user_id": request.json["user_id"]}) or {}
    existing_weights = existing["weights"] if "weights" in existing else []
    new_weight_dates = [w["date"] for w in request.json["weights"]]
    merged_weights = request.json["weights"]

    for old_weight in [w for w in existing_weights if w["date"] not in new_weight_dates]:
        merged_weights.append(old_weight)

    WeightCollection.update_one(
        {"user_id": request.json["user_id"]},
        {"$set": {"weights": merged_weights}},
        upsert=True
    )

    return jsonify({"message": "Done"})
