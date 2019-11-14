import config

from jira import JIRA

base_url = config.JIRA_Base_URL
endpoint_base = '/rest/api/2/'

jira_username = config.JIRA_Username
jira_password = config.JIRA_Password

jira_client = JIRA(base_url, basic_auth=(jira_username, jira_password))

def submit_jira(jira_issue):

    return jira_client.create_issue(jira_issue)