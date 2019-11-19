import sfdc_data


class Create2JIRA(sfdc_data.POD2JIRA):
    def __init__(self, inbound_json, pod_data):
        super().__init__(inbound_json, pod_data)

    def get_description(self):
        pass

    def get_sre_service_catalog(self):
        return "14836"  # Pod create


def build_jira_tree_new_pod(inbound_json):
    parsed_pod_list = [Create2JIRA(inbound_json, pod) for pod in inbound_json['pod_list']]
