import config
import jsonpickle

from jira import JIRA

base_url = config.JIRA_Base_URL
endpoint_base = '/rest/api/2/'

jira_username = config.JIRA_Username
jira_password = config.JIRA_Password

jira_client = JIRA(base_url, basic_auth=(jira_username, jira_password))


def submit_jira(jira_issue):
    json = jsonpickle.encode(jira_issue, unpicklable=False)
    return jira_client.create_issue(json)


def link_issue_relates(parent_key: str, child_key: str):
    return jira_client.create_issue_link(type='Relates', inwardIssue=child_key, outwardIssue=parent_key)

