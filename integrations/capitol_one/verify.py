import requests
from os import getenv
import hashlib
from urllib.parse import urlencode

class Verify:
    def __init__(self):
        self.client_credentials = ""
        self.secondary_auth = ""
        self.salt_version = "V1"
        self.base_url = "https://api.devexhacks.com"
        self.get_inital_auth()
        self.authorization = "Bearer " + self.client_credentials
        self.get_salt()

    def get_inital_auth(self):
        url = self.base_url + "/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        data = {
            "client_id": getenv("CAP_CLIENT"),
            "client_secret": getenv("CAP_SECRET"),
            "grant_type": "client_credentials"
        }
        r = requests.post(url=url, headers=headers, data=data)

        self.client_credentials = r.json().get("access_token")

    def get_salt(self):
        url = self.base_url + "/identity/salt"
        headers = {
            "Authorization": self.authorization,
            "Client-Correlation-Id": '123xyz',
            "Accept": "application/json;v=1"
        }

        r = requests.post(url=url, headers=headers)

        self.salt = r.json().get("salt")


    def get_button(self):
        url = self.base_url + "/identity/proof/tools/web-button"
        headers = {
            "Authorization": self.authorization,
            "Client-Correlation-Id": 'abc123',
            "Accept": "text/html;v=1"
        }

        r = requests.get(url=url, headers=headers)

        return r.text

    def get_second_access(self, code="8151af36a0a8478987117a960308bfb3"):
        url = self.base_url + "/oauth2/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        data = {
            "client_id": getenv("CAP_CLIENT"),
            "client_secret": getenv("CAP_SECRET"),
            "grant_type": "authorization_code",
            "code": code,
        }
        r = requests.post(url=url, headers=headers, data=data)

        self.secondary_auth = r.json().get("access_token")


    def verify(self):
        headers = {
            "Authorization": "Bearer " + self.secondary_auth,
            "Client-Correlation-Id": 'abc123',
            "Accept": "application/json;v=1"
        }

        query_data = {
            "ssnToken": hashlib.sha256(self.salt.encode() + "555333333".encode()).hexdigest(),
            "dateOfBirthToken": hashlib.sha256(self.salt.encode() + str("06/10/1947").encode()).hexdigest(),
            "lastNameToken": hashlib.sha256(self.salt.encode() + str("HANSEU").encode()).hexdigest(),
            "saltVersion": self.salt_version
        }

        verify_url = self.base_url + "/identity/proof?" + urlencode(query_data)

        r = requests.get(url=verify_url, headers=headers)

        return r.status_code
