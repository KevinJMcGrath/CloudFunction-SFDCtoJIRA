class Person:
    def __init__(self, person_record):
        self.sfdc_id = person_record['Id']
        self.fullname = person_record['Name']
        self.email = person_record['Email']


class SFDC_User(Person):
    def __init__(self, user_record):
        super().__init__(user_record)

        self.jira_username = user_record.get('JIRA_Username__c')

    @staticmethod
    def new_sfdc_user(user_json):
        if user_json:
            return SFDC_User(user_json)

        return None


class SFDC_SupportContact(Person):
    def __init__(self, support_contact):
        super().__init__(support_contact)

        self.contact_title = support_contact.get('Role')


class POD_ChangeRequest:
    def __init__(self, inbound_json, pod_data):
        self.type = inbound_json['type']
        self.pod_data = pod_data

        self.account = inbound_json['account']
        self.users: dict = inbound_json['users'] # Include map of owners/SAs/requester/etc.
        self.profile = inbound_json['client_profile']
        self.change_request = inbound_json.get('pod_change_request')

        self.account_name = self.account['Name']
        self.account_owner = SFDC_User.new_sfdc_user(self.users.get('account_owner'))
        self.cr_requesting_user = SFDC_User.new_sfdc_user(self.users.get('cr_requester'))
        self.primary_sa = SFDC_User.new_sfdc_user(self.users.get('primary_sa'))
        self.secondary_sa = SFDC_User.new_sfdc_user(self.users.get('secondary_sa'))
        self.tam = SFDC_User.new_sfdc_user(self.users.get('tam'))

        self.support_contacts = load_support_contacts(inbound_json.get('support_contacts'))

        self.pod_type = ''
        self.whitelist_ip = ''
        self.whitelist_ftp = ''
        self.subsidiary_names = []
        self.public_pod_domains_block = []
        self.seat_count = 0
        self.directory_name = ''
        self.product_type = ''
        self.client_url = ''
        self.pod_create_datacenter = ''
        self.pod_create_topology = ''
        self.on_prem_deployment_flag = False

        self.parse_data()

    def parse_data(self):
        # Account
        self.seat_count = self.account.get('Contracted_Seats__c', 0)

        # Client Profile
        self.pod_type = self.pod_data.get('Type__c')
        self.whitelist_ip = self.profile.get('Whitelisted_IP_s__c', 'TBD')
        self.whitelist_ftp = self.profile.get('Whitelisted_IP_s_SFTP__c', 'TBD')
        self.subsidiary_names = self.profile.get('Subsidiary_Company_Name__c', 'TBD')
        self.public_pod_domains_block = self.profile.get('Support_Domains_for_Blacklist__c', 'TBD')
        self.directory_name = self.profile.get('XPOD_Directory_Name__c', self.account.get('Name', 'Unknown Account'))

        if 'Datacenter__c' in self.pod_data:
            self.pod_create_datacenter = self.pod_data.get('Datacenter__c')
        elif 'POD_Datacenter__c' in self.profile:
            self.pod_create_datacenter = self.profile.get('POD_Datacenter__c')
        else:
            self.pod_create_datacenter = 'Not Specified'

        # POD Architecture
        self.client_url = self.pod_data.get('Base_URL__c', self.profile.get('Subdomain__c'))
        if self.client_url:
            if self.pod_type == 'Production':
                self.client_url += '.symphony.com'
            else:
                self.client_url += '-test.symphony.com'
        else:
            self.client_url = 'TBD'

        self.on_prem_deployment_flag = self.pod_data.get('Opp_On_Prem_Deployment__c')

    def get_reporter_username(self):
        if self.cr_requesting_user:
            return self.cr_requesting_user
        elif self.primary_sa:
            return self.primary_sa
        elif self.secondary_sa:
            return self.secondary_sa
        elif self.tam:
            return self.tam
        else:
            return 'kevin.mcgrath'


def load_support_contacts(support_contacts_json):
    if not support_contacts_json:
        return None

    return [SFDC_SupportContact(contact) for contact in support_contacts_json]
