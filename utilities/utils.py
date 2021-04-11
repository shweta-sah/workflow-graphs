from utilities.error_message import ErrorMessage
import constants.resp_constants as constants

class Utilities():
    
    @staticmethod
    def validate_workflow(workflow):
        error_message = ErrorMessage()
        for node in workflow:
            block = error_message.create_node_block(node)
            if constants.NAME not in workflow[node]:
                error_message.add_missing_field(block, constants.MISSING_NAME)
            
            if constants.DESCRIPTION not in workflow[node]:
                error_message.add_missing_field(block, constants.MISSING_DESCRIPTION)

            if constants.DEPENDENCY not in workflow[node]:
                error_message.add_missing_field(block, constants.MISSING_DEPENDENCY)
            else:
                # depends_on list exists, check if each of the nodes in this list exist
                missing_pre_reqs = []
                for pre_req in workflow[node][constants.DEPENDENCY]:
                    if pre_req not in workflow.keys():
                        missing_pre_reqs.append(pre_req)
                if missing_pre_reqs:
                   error_message.add_missing_field(block, constants.MISSING_DEPENDENCY)
                   block[constants.MISSING_DEPENDENCY] = missing_pre_reqs
            if block['reason']:
                error_message.add_section(block)

        return error_message.message
