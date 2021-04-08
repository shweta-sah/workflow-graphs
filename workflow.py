#!/usr/bin/env python3
import json
import constants
from ErrorMessage import ErrorMessage
from pprint import pprint
import sys
import argparse
import pymongo

def main():
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Validate a workflow")

    parser.add_argument('action', type=str, choices=['add', 'get', 'remove'], action='store', help='valid actions')
    parser.add_argument('-f', '--file', action='store', help='path to a workflow in json format')
    parser.add_argument('-n', '--name', action='store', help='name of the workflow')

    parsed = parser.parse_args()

    client = pymongo.MongoClient(host="localhost", port=27017)
    
    db = client.cape
    resp = db.cape_workflows.create_index("name", name="name", unique=True)

    if parsed.action == "add":
        if not parsed.file or not parsed.name:
            parser.error("the following arguments are required: -f/--file -n/--name")
        
        try:
            workflow_file = parsed.file
            # Opening JSON file
            with open(workflow_file) as wfile:
                workflow = json.load(wfile)
        except FileNotFoundError:
            print(f"ERROR: {parsed.file} File does not exist")
        except json.JSONDecodeError:
            print(f"ERROR: Invalid json file {parsed.file}")
        except Exception as e:
            print(f"Couldn't read the json file {workflow_file}")
            print(e)
        else:
            # Validate workflow
            validate_workflow(workflow)

            # Add workflow to MongoDB
            add_workflow(db, workflow, parsed.name)
        
    elif parsed.action == "get":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        try:
            document_cursor = get_workflow(db,  parsed.name)
            if document_cursor:
                pprint(document_cursor['workflow'])
            else:
                raise Exception
        except:
            print(f"ERROR: Workflow {parsed.name} does not exist!!")
    
    elif parsed.action == "remove":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        remove_workflow(db, parsed.name)


def add_workflow(db, workflow, name):
    try:
        document = {"name": name, "workflow": workflow}
        cape_workflows = db.cape_workflows
        cape_workflows.insert_one(document)
    except pymongo.errors.DuplicateKeyError:
        print(f"Workflow with name {name} already exists")


def get_workflow(db, name):
    cape_workflows = db.cape_workflows
    document_cursor = cape_workflows.find_one({"name": name})
    return document_cursor

def remove_workflow(db, name):
    cape_workflows = db.cape_workflows
    result= cape_workflows.delete_many({"name": name})
    print("Deleted ", result.deleted_count, "workflows")

def validate_workflow(workflow):
    error_message = ErrorMessage()
    for node in workflow:
        if constants.NAME not in workflow[node]:
            error_message.add_section(reason=constants.MISSING_NAME, name=node)
        if constants.DESCRIPTION not in workflow[node]:
            error_message.add_section(reason=constants.MISSING_DESCRIPTION, name=node)
        
        if constants.DEPENDENCY not in workflow[node]:
            error_message.add_section(reason=constants.MISSING_DEPENDENCY, name=node)
        else:
            # depends_on list exists, check if each of the nodes in this list exist
            missing_pre_reqs = []
            for pre_req in workflow[node][constants.DEPENDENCY]:
                if pre_req not in workflow.keys():
                    missing_pre_reqs.append(pre_req)
            if missing_pre_reqs:
                error_message.add_section(reason=constants.MISSING_DEPENDENCY, name=node, missing_nodes=missing_pre_reqs)
    
    # check if any invalids exist:
    if error_message.message["result"]["errors"]:
        raise InvalidWorkflowError(error_message.message)
    else:
        pprint(constants.SUCCESS_RESULT)


class InvalidWorkflowError(Exception):
    def __init__(self, error_log, message="Invalid Workflow! Won't add to the db!!"):
        super().__init__(message)
        pprint(error_log)

if __name__ == "__main__":
    main()