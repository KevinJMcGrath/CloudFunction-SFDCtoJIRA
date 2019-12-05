import sfdc_data


class Relocate2JIRA(sfdc_data.POD_ChangeRequest):
    def __init__(self, inbound_json, pod_data):
        super().__init__(inbound_json, pod_data)

    def get_description(self):
        pass

    def get_sre_service_catalog(self):
        return "14838"  # Pod migrate
    

def build_jira_tree_relocate_pod(inbound_json):
    parsed_pod_list = [Relocate2JIRA(inbound_json, pod) for pod in inbound_json['pod_list']]