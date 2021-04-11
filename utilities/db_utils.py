import constants
import pymongo
from pprint import pprint

class MongoDB():
    def __init__(self, host, port, db, collection):
        self.client = pymongo.MongoClient(host=host, port=port)
        
        # We will have a db called "cape" and a collection inside it "cape_workflows". A collection in Mongo is similar to a table in a RDBMS.
        # If db "cape" doesn't exist it will create one.
        self.db = self.client['db']
        self.collection = self.db['collection']

    def add_workflow(self, workflow, name):
        try:
            document = {"name": name, "workflow": workflow}
            self.collection.insert_one(document)
            self.client.close()
            return True
        except pymongo.errors.DuplicateKeyError:
            print(f"Workflow with name {name} already exists")
            return False           

    def get_workflow(self, name):
        document_cursor = self.collection.find_one({"name": name})
        self.client.close()
        return document_cursor

    def remove_workflow(self, name):
        result= self.collection.delete_many({"name": name})
        self.client.close()
        if result.deleted_count > 0:
            return {"success": True, "count": result.deleted_count}
        else: 
            return {"success": False, "count": result.deleted_count}
    
    def create_index(self, column, name, unique):
        self.collection.create_index("name", name="name", unique=True)
