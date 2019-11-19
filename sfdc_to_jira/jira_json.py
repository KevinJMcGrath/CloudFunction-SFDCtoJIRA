import sfdc_data


class JIRA_JSON:
    def __init__(self, pod: sfdc_data.POD2JIRA):
        self.fields = {
            "labels": ["ES-POD-BUILDING"],
            "priority": {"name": "Major"},
            "reporter": "",
            "description": "",
            "summary": "",
            "issuetype": {},
            "project": {}

        }

        def add_sre_service_catalog(catalog_option: str):
            self.fields['customfield_15334'] = {"id": catalog_option}

        def set_issue_type(issue_type: str):
            if str.isnumeric(issue_type):
                self.fields['issuetype'] = {"id": issue_type}
            else:
                self.fields['issuetype'] = {"name": issue_type}

        def set_reporter(reporter_username: str):
            self.fields['reporter'] = {"name": reporter_username}

