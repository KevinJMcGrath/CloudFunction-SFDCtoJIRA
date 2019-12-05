from pod_cr_to_jira.pod_create import build_jira_tree_new_pod as create
from pod_cr_to_jira.pod_relocate import build_jira_tree_relocate_pod as relocate
from pod_cr_to_jira.pod_topology import build_jira_tree_topology_upgrade as topology
from pod_cr_to_jira.pod_sunset import build_jira_tree_sunset_pod as sunset

valid_types = ['create', 'relocate', 'topology', 'sunset']


def create_jira_tree(inbound_json):
    if 'type' in inbound_json and inbound_json['type'] in valid_types:
        request_type = inbound_json['type']

        if request_type == 'create':
            create(inbound_json)
        elif request_type == 'relocate':
            relocate(inbound_json)
        elif request_type == 'topology':
            topology(inbound_json)
        elif request_type == 'sunset':
            sunset(inbound_json)

    else:
        return False, {"message": "Missing or invalid request type"}