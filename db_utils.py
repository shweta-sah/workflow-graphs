import constants
import pymongo
from pprint import pprint
import ErrorMessage

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
    if result.deleted_count > 0:
        return {"success": True, "count": result.deleted_count}
    else: 
        return {"success": False, "count": result.deleted_count}


