import pytest
import json
import utilities.error_message as ErrorMessage
from utilities.utils import Utilities
import constants.resp_constants as constants

def test_validation_success():
    # Opening JSON file
    with open("tests/workflow_success.json") as wfile:
        workflow = json.load(wfile)
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': []}}

def test_validation_missing_all():
    workflow =  {
                "step-a": {}
                }
    print(Utilities.validate_workflow(workflow))
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': [{'name': 'step-a', 'reason': 'missing-name, missing-description, missing-dependency'}]}}

def test_validation_missing_name():
    workflow =  {
                "step-a": 
                    {
                    "description": "This step does a thing",
                    "depends_on": []
                    }
                }
    print(Utilities.validate_workflow(workflow))
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': [{'name': 'step-a', 'reason': 'missing-name'}]}}

def test_validation_missing_description():
    workflow =  {
                "step-a": 
                    {
                    "name": "First Step",
                    "depends_on": []
                    }
                }
    print(Utilities.validate_workflow(workflow))
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': [{'name': 'step-a', 'reason': 'missing-description'}]}}

def test_validation_missing_depedency_key():
    workflow =  {
                "step-a": 
                    {
                    "name": "First Step",
                    "description": "This step does a thing"
                    }
                }
    print(Utilities.validate_workflow(workflow))
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': [{'name': 'step-a', 'reason': 'missing-dependency'}]}}

def test_validation_missing_depedencies():
    workflow =  {
                "step-a": 
                    {
                    "name": "Another Step Name",
                    "description": "This step does _another_ thing",
                    "depends_on": ["step-b", "step-c", "step-d"]
                    },
                "step-b":
                    {
                    "name": "Step Name",
                    "description": "This step does a thing",
                    "depends_on": []
                    }
                }
    print(Utilities.validate_workflow(workflow))
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': [{'name': 'step-a', 'reason': 'missing-dependency', 'missing-dependency': ['step-c', 'step-d']}]}}

def test_validation_missing_name_description():
    workflow =  {
                "step-a": 
                    {
                    "depends_on": ["step-c"]
                    },
                "step-c":
                    {
                    "name": "Step Name",
                    "description": "This step does a thing",
                    "depends_on": []
                    }
    }
    print(Utilities.validate_workflow(workflow))
    assert Utilities.validate_workflow(workflow) == {'result': {'errors': [{'name': 'step-a', 'reason': 'missing-name, missing-description'}]}}
