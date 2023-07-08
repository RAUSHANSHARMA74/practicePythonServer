from flask import Flask, request, jsonify

from config.connection import mydb
from dotenv import load_dotenv
import os
load_dotenv()
# from config.connection import connection
# from model.userModel import User


app = Flask(__name__)


mycol = mydb["customers"]

#greeting
@app.route("/", methods=["GET"])
def check():
    return {"message" : "server is running"}
# read user data
@app.route("/read", methods=["GET"])
def get_user_data():
    try:
        store = []
        for x in mycol.find():
            # Convert ObjectId to string representation
            x["_id"] = str(x["_id"])
            store.append(x)
        return jsonify(store)
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

# create user
@app.route("/create", methods=["POST"])
def add_user_data():
    try:
        data = request.get_json()
        mycol.insert_one(data)
        return jsonify({"message" : "Data is added"})
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

# update user data
@app.route("/update/<id>",  methods=["PATCH"])
def upadate_user_data(id):
    try:
        filter_criteria = {'_id': ObjectId(id)}
        data = request.get_json()
        update_data = {'$set': data}
        mycol.update_one(filter_criteria, update_data)
        return jsonify({"message": "User data updated successfully"})
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})

# delete user data
@app.route("/delete/<id>", methods=["DELETE"])
def delete_user_data(id):
    try:
        filter_criteria = {'_id': ObjectId(id)}
        result = mycol.delete_one(filter_criteria)

        if result.deleted_count > 0:
            return jsonify({"message": "User data deleted successfully"})
        else:
            return jsonify({"message": "User data not found"})
    except Exception as e:
        return jsonify({"message": "Error in code: " + str(e)})


db_port = os.getenv("port")
if __name__ == '__main__':

    app.run(port=1212,debug=True)