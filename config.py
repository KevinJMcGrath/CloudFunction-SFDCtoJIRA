import jsonpickle

from pathlib import Path

config_path = Path('config.json')
with open(config_path, 'r') as config_json:
    _config = jsonpickle.decode(config_json.read())

JIRA_Username = _config['jira']['username']
JIRA_Password = _config['jira']['password']
JIRA_Base_URL = _config['jira']['base_url']