import sfdc_data


class Sunset2JIRA(sfdc_data.POD_ChangeRequest):
    def __init__(self, inbound_json, pod_data):
        super().__init__(inbound_json, pod_data)

    def get_description(self):
        pass

    def get_sre_service_catalog(self):
        return "14840"  # Pod sunset



def build_jira_tree_sunset_pod(inbound_json):
    parsed_pod_list = [Sunset2JIRA(inbound_json, pod) for pod in inbound_json['pod_list']]