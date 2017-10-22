import requests
import json
from uuid import uuid4
from os import getenv


class Marqeta:

    def __init__(self, item_id):
        self.application_token = getenv("MARQ_APP_TOKEN")
        self.master_access_token = getenv("MARQ_MASTER_TOKEN")
        self.funding = str(uuid4())
        self.card_product = str(item_id)
        self.user = str(uuid4())
        self.card = str(uuid4())

        self.marqeta_flow()

    def make_card_product(self):
        headers = {
            'Content-type': 'application/json',
        }


        data = {"start_date": "2017-10-21",
                "token": self.card_product,
                "name": self.card_product,
                "config": {
                    "fulfillment": {
                        "payment_instrument": "VIRTUAL_PAN"
                    },
                    "poi": {
                        "ecommerce": True
                    },
                    "card_life_cycle": {
                        "activate_upon_issue": True
                    },
                    "digital_wallet_tokenization": {
                        "provisioning_controls": {
                            "in_app_provisioning": {
                                "enabled": True
                            },
                            "wallet_provider_card_on_file": {
                                "enabled": True
                            }
                        }
                    }
                }
                }

        r = requests.post('https://shared-sandbox-api.marqeta.com/v3/cardproducts', headers=headers, data=json.dumps(data),
                          auth=(self.application_token, self.master_access_token))

        return r.json()

    def make_funding(self):
        headers = {
            'Content-type': 'application/json',
        }

        data = {
            "token": self.funding,
            "name": self.funding
        }

        requests.post('https://shared-sandbox-api.marqeta.com/v3/fundingsources/program', headers=headers, data=json.dumps(data),
                      auth=(self.application_token, self.master_access_token))


    def make_user(self):
        headers = {
            'Content-type': 'application/json',
        }

        data = {
            "token": self.user
        }

        requests.post('https://shared-sandbox-api.marqeta.com/v3/users', headers=headers, data=json.dumps(data),
                      auth=(self.application_token, self.master_access_token))

    def make_card(self):

        headers = {
            'Content-type': 'application/json',
        }

        data = {
            "user_token": self.user,
            "card_product_token": self.card_product,
            "token": self.card
        }

        requests.post('https://shared-sandbox-api.marqeta.com/v3/cards', headers=headers, data=json.dumps(data),
                      auth=(self.application_token, self.master_access_token))

    def fund_card(self):

        headers = {
            'Content-type': 'application/json',
        }

        data = {
            "user_token": self.user,
            "amount": "5.00",
            "currency_code": "USD",
            "funding_source_token": self.funding
        }

        r = requests.post('https://shared-sandbox-api.marqeta.com/v3/gpaorders', headers=headers, data=json.dumps(data),
                      auth=(self.application_token, self.master_access_token))

        return r.json()

    def get_apple_pay(self):
        headers = {
            'Content-type': 'application/json',
        }

        data = {
            "card_token": self.card,
            "device_type": "MOBILE_PHONE",
            "provisioning_app_version": "1.0.0",
            "certificates": ["MIIEPDCCA+ =", "MIIDZjCCAw2gAwI=="],
            "nonce": "vXWJaBidcTLaJJCF",
            "nonce_signature": "jD4Aphu+93N2wbBn"
        }

        return requests.post('https://shared-sandbox-api.marqeta.com/v3/digitalwalletprovisionrequests/applepay',
                      headers=headers, data=data, auth=('application_token', 'master_access_token'))

    def marqeta_flow(self):
        self.make_card_product()
        self.make_funding()
        self.make_user()
        self.make_card()
        self.fund_card()
        self.get_apple_pay()
