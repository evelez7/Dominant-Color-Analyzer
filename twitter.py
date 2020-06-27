import json, requests, base64
import urllib.parse


class Twitter:
    BASE_URL = "https://api.twitter.com/1.1/"
    USERS_SUFFIX = "users/"
    OAUTH2_SUFFIX = "oauth2/"

    def __init__(self):
        print("initializing Twitter API")
        with open('./keys.json') as key_file:
            key_json = json.load(key_file)
            self.secret = key_json['consumer_secret']
            self.key = key_json['consumer_key']
            self.authenticate()

    def show_user(self):
        GET_SUFFIX = "show.json"
        payload = {"screen_name": "Dominant_Colors"}
        url = self.BASE_URL + self.USERS_SUFFIX + GET_SUFFIX;
        headers = {
            "Authorization": 'Bearer {}'.format(self.bearer_token),
            "Accept-Ending": 'gzip'
        }
        user_object = requests.get(url, headers=headers, params=payload)
        print(user_object.json())

    def authenticate(self):
        print("authenticating...")

        consumer_key = urllib.parse.quote(self.key)
        consumer_secret = urllib.parse.quote(self.secret)
        bearer_token =  consumer_key + ':' + consumer_secret
        base64_encoded_bearer_token = base64.b64encode(bearer_token.encode('utf-8'))

        url = 'https://api.twitter.com/oauth2/token'
        bearer_token_credentials = base64.urlsafe_b64encode('{}:{}'.format(consumer_key, consumer_secret).encode('ascii')).decode('ascii')
        headers = {
            'Authorization': 'Basic {}'.format(bearer_token_credentials),
            'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        }
        response = requests.post(url, headers=headers, data={'grant_type': 'client_credentials'})
        response_json = response.json()
        if response_json['token_type'] == 'bearer':
            print("obtained bearer token")
            self.bearer_token = response_json['access_token']
        else:
            raise RuntimeError('unexpected token type: {}'.format(response_json['token_type']))
