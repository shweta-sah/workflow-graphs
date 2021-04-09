#!/usr/bin/env python3
import json
import constants
import ErrorMessage
from pprint import pprint
import sys
import argparse
import pymongo
import db_utils
from utils import Utilities

def main():
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Validate a workflow")

    parser.add_argument('action', type=str, choices=['add', 'get', 'remove', 'validate'], action='store', help='valid actions')
    parser.add_argument('-f', '--file', action='store', help='path to a workflow in json format')
    parser.add_argument('-n', '--name', action='store', help='name of the workflow')

    parsed = parser.parse_args()

    client = pymongo.MongoClient(host="localhost", port=27017)
    
    # We will have a db called "cape" and a collection inside it "cape_workflows". A collection in Mongo is similar to a table in a RDBMS.
    # If db "cape" doesn't exist it will create one.
    db = client.cape

    # Make "name" as the unique index to avoid duplicate name workflows
    resp = db.cape_workflows.create_index("name", name="name", unique=True)

    # Pass collection instead of db to the functions
    if parsed.action == "validate":
        if not parsed.file:
            parser.error("The following arguments are required: -f/--file")
        
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
            message = Utilities.validate_workflow(workflow)
            # check if any invalids exist:
            if message["result"]["errors"]:
                raise ErrorMessage.InvalidWorkflowError(message)
            else:
                pprint(constants.SUCCESS_RESULT)
    
    elif parsed.action == "add":
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
            message = Utilities.validate_workflow(workflow)
            # check if any invalids exist:
            if message["result"]["errors"]:
                raise ErrorMessage.InvalidWorkflowError(message)
            else:
                # Add workflow to MongoDB
                db_utils.add_workflow(db, workflow, parsed.name)
                print(f"Workflow {parsed.name} added to the db")
        
    elif parsed.action == "get":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        try:
            document_cursor = db_utils.get_workflow(db,  parsed.name)
            if document_cursor:
                pprint(document_cursor['workflow'])
            else:
                raise Exception
        except:
            print(f"ERROR: Workflow {parsed.name} does not exist!!")
    
    elif parsed.action == "remove":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        response = db_utils.remove_workflow(db, parsed.name)
        if response["success"]:
            print(f"Workflow {parsed.name} deleted")
        else:
            print(f"Workflow {parsed.name} not found")

if __name__ == "__main__":
    main()