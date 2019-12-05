from pod_cr_to_jira import jira_builder

from flask import escape, abort
from google.cloud import error_reporting

google_error_client = error_reporting.Client()



def inbound_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args

    if request_json:
        try:
            success, result = jira_builder.create_jira_tree(request_json)

            if not success:
                abort(400, result['message'])

        except Exception as ex:
            # google_error_client.report_exception()
            abort(500, str(ex))

    else:
        abort(400, 'Payload missing or invalid.')