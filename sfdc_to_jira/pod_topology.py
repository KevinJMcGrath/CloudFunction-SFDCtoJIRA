import sfdc_data


class Topology2JIRA(sfdc_data.POD2JIRA):
    def __init__(self, inbound_json, pod_data):
        super().__init__(inbound_json, pod_data)

    def get_description(self):
        pass

    def get_sre_service_catalog(self):
        return "14837"  # Pod upgrade


def build_jira_tree_topology_upgrade(inbound_json):
    parsed_pod_list = [Topology2JIRA(inbound_json, pod) for pod in inbound_json['pod_list']]