import ErrorMessage
import constants

class Utilities():
    
    @staticmethod
    def validate_workflow(workflow):
        error_message = ErrorMessage.ErrorMessage()
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
        return error_message.message
