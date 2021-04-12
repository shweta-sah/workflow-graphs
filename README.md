# workflow-graphs

Workflow-graphs is a Python3 program to add valid json workflows to the db. Add, get and delete functionality is also exposed via APIs

## Pre-requisites:  

Python3: https://www.python.org/downloads/  
```python3 -m pip install --upgrade pip setuptools wheel```
```pip3 install -r requirements.txt```

Generic installation steps for MongoDB: https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-os-x/ \
To install on MAC:  
```
brew tap mongodb/brew  
brew install mongodb-community@4.4  
```

To start the mongo service:  
```brew services start mongodb/brew/mongodb-community```

To connect to DB:  
```mongo --host localhost:27017```

If you want a GUI, downlaod MongoDB Compass: https://docs.mongodb.com/compass/current/install/

## Usage:  
1. To validate a workflow to the database \
```python3 workflow.py validate -f input.json -n my-workflow```

2. To add a workflow to the database \
```python3 workflow.py add -f input.json -n my-workflow```

3. To get a workflow from the database \
```python3 workflow.py get -n my-workflow```

4. To remove a workflow from the database \
```python3 workflow.py remove -n my-workflow```

## API:  
The APIs are defined in ```workflowapi/workflowapi.py```

### Run the Flask App:  
#### Set the environment variable:
For MAC:
```export FLASK_APP=workflowapi.workflowapi```
For Windows:
```set FLASK_APP=workflowapi.workflowapi```

#### Run the flask app
```flask run```

1. Add a workflow  

* `POST /workflows/create` will create a new workflow. `name` is required, `input` is a the workflow dictionary to be added.
BODY:  
```json
{
  "name": "my-graph",
  "input": {
    "some-step": {
      "name": "Human-readable Step Name",
      "description": "This step does a thing",
      "depends_on": []
    },
    "step-b": {
      "name": "Another Step Name",
      "description": "This step does _another_ thing",
      "depends_on": ["a-step-not-in-the-graph"]
    }
  }
}
```

This will return `200 Success`, if successful, `400` and a dictionary of what's missing if missing fields.

2. Get a workflow  

* `GET /workflows/<workflow_name>` will get the workflow if exists. `workflow_name` is required.


3. Delete a workflow  

* `DELETE /workflows/<workflow_name>` will delete the workflow if exists. `workflow_name` is required.


