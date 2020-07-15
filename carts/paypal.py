

from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment

import sys

class PayPalClient:
    def __init__(self):
        self.client_id = "PAYPAL-SANDBOX-CLIENT-ID"
        self.client_secret = "PAYPAL-SANDBOX-CLIENT-SECRET"
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        result = {}
        if sys.version_info[0] < 3:
            itr = json_data.__dict__.iteritems()
        else:
            itr = json_data.__dict__.items()
        for key, value in itr:
            if key.startswith("__"):
                continue
            result[key] = self.array_to_json_array(value) if isinstance(value, list) else\
                        self.object_to_json(value) if not self.is_primittive(value) else\
                         value
        return result
    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                result.append(self.object_to_json(item) if  not self.is_primittive(item) \
                              else self.array_to_json_array(item) if isinstance(item, list) else item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, unicode) or isinstance(data, int)