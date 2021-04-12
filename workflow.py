#!/usr/bin/env python3
import json
import sys
import argparse
import pymongo
from utilities.db_utils import MongoDB
import constants.resp_constants as constants
import constants.db_constants as db_constants
import utilities.error_message as ErrorMessage
from utilities.utils import Utilities
from pprint import pprint


def main():
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Validate and CRD operations on workflows")

    parser.add_argument('action', type=str, choices=['add', 'get', 'remove', 'validate'], action='store', help='valid actions')
    parser.add_argument('-f', '--file', action='store', help='path to a workflow in json format')
    parser.add_argument('-n', '--name', action='store', help='name of the workflow')

    parsed = parser.parse_args()
    mongo_cape = initialize_mongo(db_constants.host, db_constants.port, db_constants.db, db_constants.collection)

    # Pass collection instead of db to the functions
    if parsed.action == "validate":
        if not parsed.file:
            parser.error("The following arguments are required: -f/--file")
        validate_workflow(parsed.file)
    
    elif parsed.action == "add":
        if not parsed.file or not parsed.name:
            parser.error("the following arguments are required: -f/--file -n/--name")
        add_workflow(parsed.file, parsed.name, mongo_cape)
        
    elif parsed.action == "get":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        get_workflow(parsed.name, mongo_cape)
    
    elif parsed.action == "remove":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        remove_workflow(parsed.name, mongo_cape)

def initialize_mongo(host, port, db, collection):
    # Initializes MongoClient with database and collection
    # returns collection cursor
    mongo_cape = MongoDB(host, port, db, collection)
    # Make "name" as the unique index to avoid duplicate name workflows
    mongo_cape.create_index("name", name="name", unique=True)
    return mongo_cape

def validate_workflow(workflow_file):

    try:
        # Opening JSON file
        with open(workflow_file) as wfile:
            workflow = json.load(wfile)
    except FileNotFoundError:
        print(f"ERROR: {workflow_file} file does not exist")
    except json.JSONDecodeError:
        print(f"ERROR: Invalid json file {str(workflow_file)}")
    except Exception as e:
        print(f"Couldn't read the json file {workflow_file}")
        print(e)
        return False
    else:
        # Validate workflow
        message = Utilities.validate_workflow(workflow)
        try:
            # check if any invalids exist:
            if message["result"]["errors"]:
                raise ErrorMessage.InvalidWorkflowError(message)
            else:
                pprint(constants.SUCCESS_RESULT)
        except ErrorMessage.InvalidWorkflowError as e:
            pprint (e.error_log)

def add_workflow(file, name, mongo_cape):
    try:
        workflow_file = file
        # Opening JSON file
        with open(workflow_file) as wfile:
            workflow = json.load(wfile)
    except FileNotFoundError:
        print(f"ERROR: {file} file does not exist")
    except json.JSONDecodeError:
        print(f"ERROR: Invalid json file {file}")
    except Exception as e:
        print(f"Couldn't read the json file {workflow_file}")
        print(e)
    else:
        # Validate workflow
        message = Utilities.validate_workflow(workflow)
        try:
            # check if any invalids exist:
            if message["result"]["errors"]:
                raise ErrorMessage.InvalidWorkflowError(message)
            else:
                # Add workflow to MongoDB
                success = mongo_cape.add_workflow(workflow, name)
                if success:
                    print(f"Workflow {name} added to the db")
        except ErrorMessage.InvalidWorkflowError as e:
            pprint (e.error_log)

def get_workflow(name, mongo_cape):
    try:
        document_cursor = mongo_cape.get_workflow(name)
        if document_cursor:
            pprint(document_cursor['workflow'])
        else:
            raise Exception
    except:
        print(f"ERROR: Workflow {name} does not exist!!")

def remove_workflow(name, mongo_cape):
    response = mongo_cape.remove_workflow(name)
    if response["success"]:
        print(f"Workflow {name} deleted")
    else:
        print(f"Workflow {name} not found")

if __name__ == "__main__":
    main()