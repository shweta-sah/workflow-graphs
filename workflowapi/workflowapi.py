#!/usr/bin/env python3
import json
from utilities.db_utils import MongoDB
import constants.resp_constants as constants
import constants.db_constants as db_constants
from utilities.utils import Utilities
from flask import Flask, request, Response

mongo_cape = MongoDB(db_constants.host, db_constants.port, db_constants.db, db_constants.collection)
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
            mongo_cape.add_workflow(workflow, name)
            return Response(response=json.dumps(constants.SUCCESS_RESULT),
                            status=200,
                            mimetype="application/json")
    except Exception as e:
        print("Couldn't add workflow")

@app.route("/workflows/<workflow_name>", methods =["GET"])
def get_workflows(workflow_name):
    workflow = mongo_cape.get_workflow(name=workflow_name)
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
    result = mongo_cape.remove_workflow(workflow_name)
    if result["success"]:
        return Response(response=json.dumps(f"Workflow {workflow_name} deleted"),
                        status=200,
                        mimetype="application/json")
    else:
        return Response(response=json.dumps({"error" : f"Workflow {workflow_name} does not exist!!"}),
                        status=404,
                        mimetype="application/json")
