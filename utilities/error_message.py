import constants.resp_constants as constants
from pprint import pprint
class ErrorMessage():
    def __init__(self):
        self.message = {"result": {"errors": []}}
    
    def create_node_block(self, node):
        return {"name": node, "reason": ""}
    def add_section(self, block):
        self.message["result"]["errors"].append(block)
    
    def add_missing_field(self, block, reason):
        block['reason'] = ", ".join([block['reason'], reason]) if block['reason'] else reason


class InvalidWorkflowError(Exception):
    def __init__(self, error_log, message="Invalid Workflow! Won't add to the db!!"):
        self.message = message
        self.error_log = error_log
