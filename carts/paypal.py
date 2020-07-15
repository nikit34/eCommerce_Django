import sys
from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
from paypalcheckoutsdk.orders import OrdersCreateRequest

from django.conf import settings


class PayPalClient:
    def __init__(self):
        self.client_id = "AQv95Gz28-ghtMCMN24EgeseG7GEfQulcJzlexHd9cDrsZfbdbwixzcU7z05dsgfyIh-kDuDuhqQftYJ"  # getattr(settings, 'PAYPAL_CLIENT_ID', None)
        self.client_secret = "EDKIu2nkYFXZdeAcqlAIY_0NGhgTIHdAC4jjjLdtnO6EyYZ1y_jdRf5pSeGAYrZFLPtIzbOqo6wzsmzE"  # getattr(settings, 'PAYPAL_CLIENT_SECRET', None)
        self.environment = SandboxEnvironment(client_id=self.client_id, client_secret=self.client_secret)
        self.client = PayPalHttpClient(self.environment)

    def object_to_json(self, json_data):
        result = {}
        itr = json_data.__dict__.items()
        for key, value in itr:
            if not key.startswith("__"):
                if isinstance(value, list):
                    result[key] = self.array_to_json_array(value)
                elif not self.is_primittive(value):
                    result[key] = self.object_to_json(value)
                else:
                    result[key] = value
        return result

    def array_to_json_array(self, json_array):
        result =[]
        if isinstance(json_array, list):
            for item in json_array:
                if not self.is_primittive(item):
                    result.append(self.object_to_json(item))
                elif isinstance(item, list):
                    result.append(self.array_to_json_array(item))
                else:
                    result.append(item)
        return result

    def is_primittive(self, data):
        return isinstance(data, str) or isinstance(data, int)


class CreateOrder(PayPalClient):
    def create_order(self):
        request = OrdersCreateRequest()
        request.prefer('return=representation')
        request.request_body(self.build_request_body())
        response = self.client.execute(request)
        if settings.DEBUG:
            print('Status Code: ', response.status_code)
            print('Status: ', response.result.status)
            print('Order ID: ', response.result.id)
            print('Intent: ', response.result.intent)
            print('Links:')
            for link in response.result.links:
                print('\t{}: {}\tCall Type: {}'.format(link.rel, link.href, link.method))
            print('Total Amount: {} {}' \
                .format(
                    response.result.purchase_units[0].amount.currency_code,
                    response.result.purchase_units[0].amount.value
                )
            )
        return response

    @staticmethod
    def build_request_body():
        return \
  {
    "intent": "CAPTURE",
    "application_context": {
      "brand_name": "EXAMPLE INC",
      "landing_page": "BILLING",
      "shipping_preference": "SET_PROVIDED_ADDRESS",
      "user_action": "CONTINUE"
    },
    "purchase_units": [
      {
        "reference_id": "PUHF",
        "description": "Sporting Goods",

        "custom_id": "CUST-HighFashions",
        "soft_descriptor": "HighFashions",
        "amount": {
          "currency_code": "USD",
          "value": "230.00",
          "breakdown": {
            "item_total": {
              "currency_code": "USD",
              "value": "180.00"
            },
            "shipping": {
              "currency_code": "USD",
              "value": "30.00"
            },
            "handling": {
              "currency_code": "USD",
              "value": "10.00"
            },
            "tax_total": {
              "currency_code": "USD",
              "value": "20.00"
            },
            "shipping_discount": {
              "currency_code": "USD",
              "value": "10"
            }
          }
        },
        "items": [
          {
            "name": "T-Shirt",
            "description": "Green XL",
            "sku": "sku01",
            "unit_amount": {
              "currency_code": "USD",
              "value": "90.00"
            },
            "tax": {
              "currency_code": "USD",
              "value": "10.00"
            },
            "quantity": "1",
            "category": "PHYSICAL_GOODS"
          },
          {
            "name": "Shoes",
            "description": "Running, Size 10.5",
            "sku": "sku02",
            "unit_amount": {
              "currency_code": "USD",
              "value": "45.00"
            },
            "tax": {
              "currency_code": "USD",
              "value": "5.00"
            },
            "quantity": "2",
            "category": "PHYSICAL_GOODS"
          }
        ],
        "shipping": {
          "method": "United States Postal Service",
          "address": {
            "name": {
              "full_name":"John",
              "surname":"Doe"
            },
            "address_line_1": "123 Townsend St",
            "address_line_2": "Floor 6",
            "admin_area_2": "San Francisco",
            "admin_area_1": "CA",
            "postal_code": "94107",
            "country_code": "US"
          }
        }
      }
    ]
  }