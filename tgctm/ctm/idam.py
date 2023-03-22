import re, json
import requests
from django.conf import settings

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r

class TGBT:

    def __init__(self):
        self.api_url = settings.IDAM_API_URL
        self.api_key = settings.IDAM_API_KEY

    def request(self, endpoint):
        req = requests.get(self.api_url + endpoint, auth=BearerAuth(self.api_key))
        if req.status_code == 200:
            return req.json()
        else:
            raise Exception("NFC Tag not found") 
    
    def get_wannabe_id_from_nfc_tag(self, nfc):
        return self.request("get_wbuser_fromidcard/?sn=" +nfc)['wannabe_id']
    
    def get_all_crews_with_crew_members(self):
        return self.request("get_wballcrewsallcrewmembers/")['data']