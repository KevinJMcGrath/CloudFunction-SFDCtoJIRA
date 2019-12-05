from sfdc_data import POD_ChangeRequest


class POD_CR_to_JIRA:
    def __init__(self, sfdc_pod_data: POD_ChangeRequest):
        self.pod_cr: POD_ChangeRequest = sfdc_pod_data

        self.reporter = self.pod_cr.get_reporter_username()
        self.action = self.set_action()

        # Default values
        self.labels = ['ES-POD-BUILDING']
        self.priority = 'Major'
        self.issue_type = '10000'
        self.project = 'ESS'
        self.summary = ''
        self.description = ''

        self.custom_fields = {}
        # Use this dict to add fields that are in the format { "key": value }
        self.custom_key_fields = {}

    def add_custom_field(self, field_name, value_obj):
        self.custom_fields[field_name] = value_obj

    def add_labels(self, *label_names):
        for label in label_names:
            if label not in self.labels:
                self.labels += label

    def get_SRE_regex_code(self):
        if self.pod_cr.pod_type == 'Production':
            return 'PROD'
        else:
            return 'UAT'

    def set_action(self):
        if self.pod_cr.type == 'create':
            action = 'Create POD'
        elif self.pod_cr.type == 'relocate':
            action = 'Relocate POD'
        elif self.pod_cr.type == 'topology':
            action = 'Topology Upgrade'
        elif self.pod_cr.type == 'sunset':
            action = 'Sunset POD'
        else:
            action = 'Unknown Action'

        return action

    def build_summary(self, summary_list: list):
        return ' - '.join(summary_list) + self.get_SRE_regex_code()

    def get_project_summary_tuple(self, ticket_type: str):
        project_key = ''
        summary = ''

        if ticket_type == 'customer':
            project_key = 'SA'
            summary = self.build_summary([
                 self.pod_cr.account_name,
                 'Client Tracking',
                 self.pod_cr.pod_type])
        elif ticket_type == 'pod':
            project_key = 'SA'
            summary = self.build_summary([
                self.pod_cr.account_name,
                'POD Tracking',
                self.pod_cr.pod_type
            ])
        elif ticket_type == 'whitelist':
            project_key = 'SA'
            summary = self.build_summary([
                self.pod_cr.account_name,
                'Whitelist Tracking',
                self.pod_cr.pod_type
            ])
        elif ticket_type == 'sor':
            project_key = 'SOR'
            summary = self.build_summary([
                'Whitelisting Request',
                self.pod_cr.account_name,
                self.pod_cr.pod_type
            ])
        elif ticket_type == 'checkout':
            project_key = 'SA'
            summary = self.build_summary([
                self.pod_cr.account_name,
                'Checkout',
                self.action,
                self.pod_cr.pod_type
            ])
        elif ticket_type == 'build':
            project_key = 'ESS'
            summary = self.build_summary([
                self.action,
                self.pod_cr.account_name,
                self.pod_cr.pod_type
            ])

        return project_key, summary


def text_to_JIRA_sublist(input_text: str):
    if not input_text:
        return 'Not Specified'

    item_list = input_text.replace('\r', '').replace('\n', ';').replace(',', ';').split(';')
    return ['** ' + item + '\n' for item in item_list]


def set_jira_color(body_value: str, html_color_code: str, is_bold: bool = False):
    coded_value = '{color:' + html_color_code + '}' + body_value + '{color}'

    if is_bold:
        coded_value = '*' + coded_value + '*'

    return coded_value


def color_boolean(body_value):
    coded_value = 'YES' if body_value else 'NO'
    color = 'green' if body_value else 'darkred'

    return set_jira_color(coded_value, color, True)