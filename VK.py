import requests
from urllib.parse import urlencode
from time import sleep


class VK:
    def __init__(self, call_back):
        self.call_back = call_back

    @staticmethod
    def make_key_URL():
        APP_ID = '7344387'
        OAUTH_URL = 'https://oauth.vk.com/authorize'
        OAUTH_PARAMS = {
            'client_id': APP_ID,
            'display': 'page',
            'scope': 'status,groups',
            'response_type': 'token',
            'v': '5.89',
        }
        return '?'.join((OAUTH_URL, urlencode(OAUTH_PARAMS)))

    @staticmethod
    def get_token():
        # ACCESS_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1' # given
        ACCESS_TOKEN = '0ffb0c371911eaf302630c1f4976243572dd2fd31a20369cd1c45b3ee2d5c2f7e873bae5bc075b04d1e80'
        return ACCESS_TOKEN



    @staticmethod
    def req(url, params):
        response = ''
        for i in range(10):
            print('.', end='')   # callback function would be better
            response = requests.get(url,params)
            if response.status_code != 200:
                sleep(2)
            elif 'error' in response.json():
                err_code = response.json().get('error').get('error_code')
                err_msg = response.json().get('error').get('error_msg')
                key = response.json().get('error').get('request_params')[0].get('key')
                value = response.json().get('error').get('request_params')[0].get('value')
                if err_code == 6:  # 'Too many requests per second'
                    sleep(2)
                else:
                    raise Exception(f'Error: {err_msg}, {key}: {value}')
            else:
                break
        return response

    @staticmethod
    def get_permissions(user_id):
        response = VK.req(
            'https://api.vk.com/method/account.getAppPermissions',
            params={
                'user_id': user_id,
                'access_token': VK.get_token(),
                'v': '5.89',
            }
        )
        return response.json()

    @staticmethod
    def get_groups_info(groups):
        groups_string = ",".join([str(gr) for gr in groups])
        response = VK.req(
            'https://api.vk.com/method/groups.getById',
            params={
                'group_ids': groups_string,
                'access_token': VK.get_token(),
                'fields': 'members_count',
                'v': '5.89',
            }
        )
        return [{"name": gr['name'], "gid": gr['id'], "members_count": gr['members_count']} for gr in response.json()['response']]

