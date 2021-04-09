import constants
from pprint import pprint
class ErrorMessage():
    def __init__(self):
        self.message = {"result": {"errors": []}}
    
    def add_section(self, reason, name, missing_nodes=None):
        self.block = {}
        self.block["reason"] = reason
        self.block["name"] = name

        if reason == constants.MISSING_DEPENDENCY and missing_nodes:
            self.block[constants.MISSING_DEPENDENCY] = missing_nodes
        self.message["result"]["errors"].append(self.block)


class InvalidWorkflowError(Exception):
    def __init__(self, error_log, message="Invalid Workflow! Won't add to the db!!"):
        super().__init__(message)
        pprint(error_log)
