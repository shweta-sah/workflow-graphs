#!/usr/bin/env python3
import json
import constants
from ErrorMessage import ErrorMessage
from pprint import pprint
import sys
import argparse

def main():
    # Initialize argparse
    parser = argparse.ArgumentParser(description="Validate a workflow")
    parser.add_argument('-f', '--file', action='append', help='path to a json workflow')
    parsed = parser.parse_args()
    if not parsed.file:
        parser.error("Please provide file name with -f or --file")
    workflow_file = parsed.file[0]

    # Opening JSON file
    with open(workflow_file) as wfile:
        workflow = json.load(wfile)
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
    def __init__(self, error_log, message="Invalid Workflow"):
        super().__init__(message)
        pprint(error_log)

if __name__ == "__main__":
    main()