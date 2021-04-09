#!/usr/bin/env python3
from flask import Flask, request, Response
import pymongo
from pymongo import MongoClient
import json
import db_utils
from utils import Utilities
import constants

client = pymongo.MongoClient(host="localhost", port=27017)
    
# We will have a db called "cape" and a collection inside it "cape_workflows". A collection in Mongo is similar to a table in a RDBMS.
# If db "cape" doesn't exist it will create one.
db = client.cape
collection = db.cape_workflows

app = Flask(__name__)

@app.route("/")
def get_homepage():
    return "Welcome to workflow-graphs"

@app.route("/workflows/create", methods =["POST"])
def add_workflows():
    try:
        request_payload = request.json
        name = request_payload["name"]
        workflow = request_payload["input"]
        message = Utilities.validate_workflow(workflow)
        if message["result"]["errors"]:
            return Response(response=json.dumps(message),
                            status=404,
                            mimetype="application/json")
        else:
            # Add workflow to MongoDB
            db_utils.add_workflow(db, workflow, name)
            return Response(response=json.dumps(constants.SUCCESS_RESULT),
                            status=200,
                            mimetype="application/json")
    except Exception as e:
        print("Couldn't add workflow")



@app.route("/workflows/<workflow_name>", methods =["GET"])
def get_workflows(workflow_name):
    workflow = db_utils.get_workflow(db, workflow_name)
    if workflow:
        return Response(response=json.dumps(workflow["workflow"]),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=json.dumps({"error" : f"Workflow {workflow_name} does not exist!!"}),
                        status=404,
                        mimetype="application/json")

@app.route("/workflows/<workflow_name>", methods =["DELETE"])
def delete_workflows(workflow_name):
    result = db_utils.remove_workflow(db, workflow_name)
    if result["success"]:
        return Response(response=json.dumps(f"Workflow {workflow_name} deleted"),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=json.dumps({"error" : f"Workflow {workflow_name} does not exist!!"}),
                        status=404,
                        mimetype="application/json")



