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
    parser = argparse.ArgumentParser(description="Validate a workflow")

    parser.add_argument('action', type=str, choices=['add', 'get', 'remove', 'validate'], action='store', help='valid actions')
    parser.add_argument('-f', '--file', action='store', help='path to a workflow in json format')
    parser.add_argument('-n', '--name', action='store', help='name of the workflow')

    parsed = parser.parse_args()


    mongo_cape = MongoDB(db_constants.host, db_constants.port, db_constants.db, db_constants.collection)
    
    # Make "name" as the unique index to avoid duplicate name workflows
    mongo_cape.create_index("name", name="name", unique=True)

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
                success = mongo_cape.add_workflow(workflow, parsed.name)
                if success:
                    print(f"Workflow {parsed.name} added to the db")
        
    elif parsed.action == "get":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        try:
            document_cursor = mongo_cape.get_workflow(parsed.name)
            if document_cursor:
                pprint(document_cursor['workflow'])
            else:
                raise Exception
        except:
            print(f"ERROR: Workflow {parsed.name} does not exist!!")
    
    elif parsed.action == "remove":
        if not parsed.name:
            parser.error("The following arguments are required: -n/--name")
        response = mongo_cape.remove_workflow(parsed.name)
        if response["success"]:
            print(f"Workflow {parsed.name} deleted")
        else:
            print(f"Workflow {parsed.name} not found")

if __name__ == "__main__":
    main()