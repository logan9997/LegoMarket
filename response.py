from requests_oauthlib import OAuth1Session
from environment_manager import Manager
import json
from datetime import datetime, timedelta

class Response:

    def __init__(self) -> None:
        self.oauth_credentials = Manager.get_oauth_credentials()
        self.auth = OAuth1Session(*self.oauth_credentials.values())
        self.base_url = 'https://api.bricklink.com/api/store/v1/'
        self.daily_max_calls = 4999
        self.date_format = '%Y-%m-%d %H:%M:%S'
        self.check_daily_calls_limit()

    def check_daily_calls_limit(self) -> None:
        timeout_value = self.get_timeout()
        timed_out = False
        if timeout_value != None:
            timed_out = datetime.now() < timeout_value

        if timed_out:
            print(f'TIMED OUT; reset at {timeout_value}')
            exit()
        self.reset_timeout()

        calls_exceeded = self.get_daily_calls_count() >= self.daily_max_calls
        if calls_exceeded:
            print('MAX DAILY API CALLS MET.')
            self.reset_daily_calls_count()
            self.set_timeout()
            exit()

    def reset_timeout(self) -> None:
        Manager.update_value('API_CALLS_TIMEOUT', 'None')

    def get_timeout(self) -> datetime | None:
        timeout = Manager.get_value('API_CALLS_TIMEOUT')
        if timeout == 'None':
            return None
        return datetime.strptime(timeout, self.date_format)

    def set_timeout(self) -> None:
        timeout = datetime.now() + timedelta(days=1)
        timeout = timeout.strftime(self.date_format)
        Manager.update_value('API_CALLS_TIMEOUT', str(timeout))

    def reset_daily_calls_count(self) -> None:
        Manager.update_value('DAILY_API_CALLS', '0')

    def get_daily_calls_count(self) -> int:
        return int(Manager.get_value('DAILY_API_CALLS'))

    def increment_daily_call_count(self) -> None:
        daily_api_calls = self.get_daily_calls_count() 
        daily_api_calls += 1
        Manager.update_value('DAILY_API_CALLS', str(daily_api_calls))

    def get_response(self, sub_url: str) -> dict:
        self.check_daily_calls_limit()
        response = self.auth.get(self.base_url + sub_url)
        json_data = json.loads(response.text)
        self.increment_daily_call_count()

        if json_data['meta']['code'] != 200:
            exception_message = f'{str(json_data.get("meta"))}\nUPDATE KEYS - https://www.bricklink.com/v2/api/register_consumer.page'
            raise Exception(exception_message)
        return json_data['data']
    

if __name__ == '__main__':
    test = Response().get_response('items/MINIFIG/sw0001a')
