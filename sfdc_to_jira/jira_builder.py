from sfdc_to_jira.pod_create import build_jira_tree_new_pod as create
from sfdc_to_jira.pod_relocate import build_jira_tree_relocate_pod as relocate
from sfdc_to_jira.pod_topology import build_jira_tree_topology_upgrade as topology
from sfdc_to_jira.pod_sunset import build_jira_tree_sunset_pod as sunset

valid_types = ['create', 'relocate', 'topology', 'sunset']


class SFDC_Data:
    def __init__(self, inbound_json):
        self.type = inbound_json['type']
        self.account = inbound_json['account']
        self.pod_list = [pod for pod in inbound_json['pod_list']]
        self.profile = inbound_json['client_profile']
        self.change_request = inbound_json['pod_change_request']


def create_jira_tree(inbound_json):
    if 'type' in inbound_json and inbound_json['type'] in valid_types:
        data = SFDC_Data(inbound_json)

        if data.type == 'create':
            create(data)
        elif data.type == 'relocate':
            relocate(data)
        elif data.type == 'topology':
            topology(data)
        elif data.type == 'sunset':
            sunset(data)

    else:
        return False, {"message": "Missing or invalid request type"}