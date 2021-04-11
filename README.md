# workflow-graphs

Workflow-graphs is a Python3 program to add valid json workflows to the db.

### Pre-requisites:
Python3: https://www.python.org/downloads/
* ```python3 -m pip install --upgrade pip setuptools wheel```
* ```pip3 install -r requirements.txt```

Generic installation steps for MongoDB: https://docs.mongodb.com/manual/tutorial/install-mongodb-enterprise-on-os-x/
To install on MAC:
* ```brew tap mongodb/brew```
* ```brew install mongodb-community@4.4```

To start the mongo service:
* ```brew services start mongodb/brew/mongodb-community```

To connect to DB:
* ```mongo --host localhost:27017```

If you want a GUI, downlaod MongoDB Compass: https://docs.mongodb.com/compass/current/install/

### Usage:
1. To validate a workflow to the database \
```python3 workflow.py validate -f input.json -n my-workflow```

2. To add a workflow to the database \
```python3 workflow.py add -f input.json -n my-workflow```

3. To get a workflow from the database \
```python3 workflow.py get -n my-workflow```

4. To remove a workflow from the database \
```python3 workflow.py remove -n my-workflow```
