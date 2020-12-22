import json, requests, base64
from requests_oauthlib import OAuth1Session
import urllib.parse


class Twitter:
    def __init__(self):
        print("Initializing Twitter API connection...")
        with open('./keys.json') as key_file:
            key_json_file = json.load(key_file)
        self.api_secret = key_json_file['api_secret']
        self.api_key = key_json_file['api_key']
        self.bearer_token = key_json_file['bearer_token']
        self.authorized = False
        
    def create_authentication(self):
        request_token_url = "https://api.twitter.com/oauth/request_token"
        oauth = OAuth1Session(self.api_key, client_secret = self.api_secret)
        auth_response = oauth.fetch_request_token(request_token_url)
        resource_token = auth_response.get("oauth_token")
        resource_secret = auth_response.get("oauth_token_secret")
        base_authorization_url = "https://api.twitter.com/oauth/authorize"
        authorization_url = oauth.authorization_url(base_authorization_url)
        print("Please go here and authorize: %s" % authorization_url)
        verifier = input("Paste the PIN here: ")

        oauth = OAuth1Session(
            self.api_key,
            client_secret=self.api_secret,
            resource_owner_key=resource_token,
            resource_owner_secret=resource_secret,
            verifier=verifier
        )
        oauth_tokens = oauth.fetch_access_token("https://api.twitter.com/oauth/access_token")
        oauth = OAuth1Session(
            self.api_key,
            client_secret = self.api_secret,
            resource_owner_key=oauth_tokens.get("oauth_token"),
            resource_owner_secret=oauth_tokens.get("oauth_token_secret")
        )
        self.oauth = oauth

    def get_user(self):
        if self.authorized is not True:
            self.create_authentication()
        fields = "created_at,description"
        tweet_fields = "source,text,id,attachments,author_id"
        params = {"usernames": "Dominant_Colors", "user.fields": fields, "tweet.fields" : tweet_fields} 
        response = self.oauth.get("https://api.twitter.com/2/users/by", params=params)
        if response.status_code != 200:
            raise Exception(
                "Request returned an error: {} {}".format(response.status_code, response.text)
            )
        
        json_response = response.json()

        print(json.dumps(json_response, indent=4, sort_keys=True))
