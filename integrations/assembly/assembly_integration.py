"""
assembly wrapper for escrow creation and transactions
"""

import requests
from urllib.parse import urlencode
from uuid import uuid4
from os import getenv


class AssemblyItem:
    transaction_counter = 0

    def __init__(self):
        """
        initializes Assembly
        """
        self.item_id = str(uuid4())
        self.base_url = "https://test.api.promisepay.com"
        self.authorization = getenv("ASS_AUTH")
        self.buyer = getenv("ASS_BUYER_ID")
        self.seller = getenv("ASS_SELLER_ID")
        self.state = ""

        self.create_item()
        self.make_payment()

    def create_item(self):
        """
        creates escrow item
        :return: escrow item ID
        """
        query_data = {
            'id': str(self.item_id),
            'name': 'GiftCardSell' + str(AssemblyItem.transaction_counter),
            'amount': '1000',
            'payment_type': 1,
            'buyer_id': self.buyer,
            'seller_id': self.seller,
        }

        headers = {'Authorization': self.authorization}

        item_url = self.base_url + "/items/?" + urlencode(query_data)
        AssemblyItem.transaction_counter = AssemblyItem.transaction_counter + 1

        r = requests.post(url=item_url, headers=headers)

    def get_buyer_card(self):
        """
        gets buyer card ID for payment to escrow
        :return:
        """
        card_url = self.base_url + "/users/" + self.buyer + "/card_accounts"

        headers = {'Authorization': self.authorization}

        r = requests.get(url=card_url, headers=headers)

        return r.json().get("card_accounts").get("id")

    def make_payment(self):
        """
        make payment using user payment
        :return: state of item [payment_held, payment_pending, payment_deposited]
        """
        payment_id = self.get_buyer_card()

        payment_url = self.base_url + "/items/" + str(self.item_id) + "/make_payment"

        headers = {'Authorization': self.authorization}
        data = {
            "account_id": str(payment_id),
            "ip_address": "192.0.0.1",
            "device_id": "sample device ID"
        }

        r = requests.patch(url=payment_url, headers=headers, data=data)

        self.state = r.json().get("items").get('state')
