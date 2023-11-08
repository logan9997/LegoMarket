from requests_oauthlib import OAuth1Session
from environment_manager import Manager
import json

class Response:

    def __init__(self) -> None:
        self.oauth_credentials = Manager.get_oauth_credentials()
        self.auth = OAuth1Session(*self.oauth_credentials.values())
        self.base_url = 'https://api.bricklink.com/api/store/v1/'

    def get_response(self, sub_url: str):
        response = self.auth.get(self.base_url + sub_url)
        json_data = json.loads(response.text)

        if json_data['meta']['code'] != 200:
            print('UPDATE KEYS - https://www.bricklink.com/v2/api/register_consumer.page')
            raise Exception(str(json_data))
        return json_data['data']
    

if __name__ == '__main__':
    test = Response().get_response('items/MINIFIG/sw0001a')
    print(test)
