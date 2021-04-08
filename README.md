# workflow-graphs

Workflow-graphs is a Python3 program to validate a workflow in json format.

### Pre-requisites:
* Python3: https://www.python.org/downloads/
* ```python3 -m pip install --upgrade pip setuptools wheel```
* ```pip3 install json```
* ```pip3 install pprint```
* ```pip3 install sys```
* ```pip3 install argparse```
* ```pip3 install pymongo```
* MongoDB: https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-os-x/
* To install on MAC:
* ```brew tap mongodb/brew```
* ```brew install mongodb-community@4.4```
* ```brew services start mongodb/brew/mongodb-community```
* To connect to DB:
* ```mongo --host localhost:27017```


Usage:\
```python3 workflow.py add -f input.json -n my-workflow```\
```python3 workflow.py get my-workflow```\
```python3 workflow.py remove my-workflow```

Example:\
```python3 workflow.py -f ./test_files/workflow_success.json```\
