import sfdc_data
import pod_cr_to_jira.jira_json as jira_json
import pod_cr_to_jira.pod_to_jira as p2j


class CreateParent(p2j.POD_CR_to_JIRA):
    def __init__(self, sfdc_pod_data: sfdc_data.POD_ChangeRequest):
        super().__init__(sfdc_pod_data)

        self.prepare_data()

    def prepare_data(self):
        self.priority = 'Major'
        self.issue_type = '10000'

        self.add_labels('ES-POD-BUILDING', 'POD-CREATE')
        self.add_custom_field('customfield_15334', '14838')

        self.description = self.build_desc()

    def build_desc(self):
        body = "POD Creation Request for " + self.pod_cr.account_name + "\n\n"
        body += "*Details*:\n\n"
        body += "* SFDC Account Id: "
        body += "* POD Datacenter: " + p2j.set_jira_color(self.pod_cr.pod_create_datacenter, 'D04437') + "\n"
        body += "* Account Owner: " + self.pod_cr.account_owner.fullname + "\n"
        body += "* Licenses: " + self.pod_cr.seat_count + "\n"
        body += "* Topology: " + self.pod_cr.pod_create_topology + "\n"

        if self.pod_cr.support_contacts:
            body += "\n*Customer Support Contacts*:\n"
            for contact in self.pod_cr.support_contacts:
                body += "* " + contact.contact_title + ": " + contact.fullname + " (" + contact.email + ")\n"

        body += "\n*POD Configuration Info*\n"
        body += "* Desired URL: " + self.pod_cr.client_url + "\n"
        body += "* XPOD Directory Name: " + self.pod_cr.directory_name + "\n"
        body += "* On Prem Deployment: " + p2j.color_boolean(self.pod_cr.on_prem_deployment_flag) + "\n"

        body += "* Whitelisted IPs: \n" + p2j.text_to_JIRA_sublist(self.pod_cr.whitelist_ip) + "\n"
        body += "* Whitelisted IPs (SFTP): \n" + p2j.text_to_JIRA_sublist(self.pod_cr.whitelist_ftp) + "\n"
        body += "* Subsidiary Company Names: \n" + p2j.text_to_JIRA_sublist(self.pod_cr.subsidiary_names) + "\n"
        body += "* Domains to Block on Public: \n" + p2j.text_to_JIRA_sublist(self.pod_cr.public_pod_domains_block) + "\n"

        body += "\n(*r) (*g) (*b) Notice (*r) (*g) (*b)\n"
        body += "This JIRA was created by Business Operations automation."

        return body


def build_jira_tree_new_pod(inbound_json):
    pod_list = inbound_json['pod_list']

    for pod_data in pod_list:
        sfdc_cr_data = sfdc_data.POD_ChangeRequest(inbound_json, pod_data)
        parent_data = CreateParent(sfdc_cr_data)

        # Submit tracking issues to JIRA, obtain keys:
        customer_tracking_key = jira_json.submit_ticket_to_jira(parent_data, 'customer')
        pod_tracking_key = jira_json.submit_ticket_to_jira(parent_data, 'pod')
        whitelist_tracking_key = jira_json.submit_ticket_to_jira(parent_data, 'whitelist')
        checkout_tracking_key = jira_json.submit_ticket_to_jira(parent_data, 'checkout')

        # Submit SOR/ESS issues to JIRA
        whitelist_sor = jira_json.submit_ticket_to_jira(parent_data, 'sor', subtask_parent_key=whitelist_tracking_key)
        checkout_ess = jira_json.submit_ticket_to_jira(parent_data, 'build', subtask_parent_key=checkout_tracking_key)

        # Create issue links
        jira_json.link_issue_relates(customer_tracking_key, pod_tracking_key)
        jira_json.link_issue_relates(pod_tracking_key, whitelist_tracking_key)
        jira_json.link_issue_relates(pod_tracking_key, checkout_tracking_key)
