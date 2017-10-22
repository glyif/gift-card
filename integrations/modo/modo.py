import requests
from urllib.parse import urlencode
from uuid import uuid4
from os import getenv


class ModoApi:

    def __init__(self):
        self.rand_id = uuid4()[:4]
        self.base_url = "https://api.sbx.gomo.do"
        self.modo_key = getenv("MODO_KEY")
        self.authorization = "MODO0 key=" + self.modo_key

    def create_user(self):
        registration_url = self.base_url + "/api_v2/people/register"

        headers = {'Authorization': self.authorization}
        data = {
            "phone": 1234567890,
            "fname": "John",
            "lname": "Doe" + self.rand_id,
            "email": "info@modopayments.com"
        }

        r = requests.post(url=registration_url, headers=headers, data=data)

        return r.json()
