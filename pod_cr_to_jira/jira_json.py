import pod_cr_to_jira.utility as util

from pod_cr_to_jira.pod_to_jira import POD_CR_to_JIRA


class JIRA_JSON:
    def __init__(self):
        self.labels = []
        self.priority = None
        self.reporter = None
        self.description = None
        self.summary = None
        self.issue_type = None
        self.project = None

    def add_label(self, label_name: str):
        if label_name not in self.labels:
            self.labels += label_name

    def add_label_list(self, label_list: list):
        for label in label_list:
            self.add_label(label)

    def set_priority(self, priority: str = "Major"):
        self.priority = format_jira_field(priority)

    def set_reporter(self, reporter_username: str):
        self.reporter = {"name": reporter_username}

    def set_description(self, body_text: str):
        self.description = body_text

    def set_summary(self, summary_text: str):
        self.summary = summary_text

    def set_issue_type(self, issue_type: str):
        self.issue_type = format_jira_field(issue_type)

    def set_project(self, project_key: str):
        self.project = format_jira_field(project_key, is_key_type=True)

    def add_custom_key_value_field(self, field_name: str, field_value: str, is_key_type: bool = False):
        setattr(self, field_name, format_jira_field(field_value, is_key_type))

    def add_custom_std_field(self, field_name: str, field_value: str):
        setattr(self, field_name, field_value)

    def add_custom_fields(self, custom_field_dict: dict, is_key_type: bool = False):
        for k, v in custom_field_dict:
            self.add_custom_key_value_field(k, v, is_key_type)

    def submit_to_jira(self):
        util.submit_jira(self)


def format_jira_field(field_value: str, is_key_type: bool = False):
    if is_key_type:
        return {"key": field_value}

    return {"id": field_value} if str.isnumeric(field_value) else {"name": field_value}


def submit_ticket_to_jira(pod_cr: POD_CR_to_JIRA, ticket_type: str, subtask_parent_key: str = None):
    cr_jira_json = JIRA_JSON()
    cr_jira_json.set_priority(pod_cr.priority)
    cr_jira_json.set_issue_type(pod_cr.issue_type)
    cr_jira_json.set_reporter(pod_cr.reporter)
    cr_jira_json.set_description(pod_cr.description)
    cr_jira_json.add_label_list(pod_cr.labels)
    cr_jira_json.add_custom_fields(pod_cr.custom_fields)
    cr_jira_json.add_custom_fields(pod_cr.custom_key_fields)

    project_key, summary = pod_cr.get_project_summary_tuple(ticket_type)

    cr_jira_json.set_summary(summary)
    cr_jira_json.set_project(project_key)

    if subtask_parent_key:
        cr_jira_json.set_issue_type('5')
        cr_jira_json.add_custom_key_value_field('parent', subtask_parent_key, is_key_type=True)


    return cr_jira_json.submit_to_jira().key


def link_issue_relates(parent_key: str, child_key: str):
    util.link_issue_relates(parent_key, child_key)