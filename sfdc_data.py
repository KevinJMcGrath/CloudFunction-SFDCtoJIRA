
class POD2JIRA:
    def __init__(self, inbound_json, pod_data):
        self.type = inbound_json['type']
        self.account = inbound_json['account']
        self.pod_data = pod_data
        self.profile = inbound_json['client_profile']
        self.change_request = inbound_json['pod_change_request']

        self.pod_type = ''
        self.whitelist_ip = ''
        self.whitelist_ftp = ''
        self.subsidiary_names = []
        self.public_pod_domains_block = []
        self.seat_count = 0
        self.directory_name = ''
        self.product_type = ''
        self.subdomain = ''
        self.pod_create_datacenter = ''
        self.pod_create_topology = ''

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
        self.subdomain = self.pod_data.get('Base_URL__c', self.profile.get('Subdomain__c'))
        if self.subdomain:
            if self.pod_type == 'Production':
                self.subdomain += '.symphony.com'
            else:
                self.subdomain += '-test.symphony.com'
        else:
            self.subdomain = 'TBD'

    def get_summary(self):
        pass

    def get_description(self):
        pass

    def get_service_catalog(self):
        pass

    def get_reporter(self):
        return {"name", "kevin.mcgrath"}

    def get_priority(self):
        return {"name", "Major"}

    def get_sre_service_catalog(self):
        pass


