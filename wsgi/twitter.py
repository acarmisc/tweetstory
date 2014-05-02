import tweepy
from flask_oauth import OAuth
from tools import getConfig, _logger


config = getConfig()
_logger = _logger('Twitter')


class twitterClient(object):

    def __init__(self, config_dict=False):

        self.t_acc_token = config_dict['t_acc_token']
        self.t_acc_secret = config_dict['t_acc_secret']
        self.t_api_key = config_dict['t_api_key']
        self.t_api_secret = config_dict['t_api_secret']

    def connect(self):
        auth = tweepy.OAuthHandler(self.t_api_key, self.t_api_secret)
        auth.set_access_token(self.t_acc_token, self.t_acc_secret)

        api = tweepy.API(auth)

        return api

    def authenticate(self):
        oauth = OAuth()
        twitter = oauth.remote_app('twitter',
            base_url='https://api.twitter.com/1/',
            request_token_url='https://api.twitter.com/oauth/request_token',
            access_token_url='https://api.twitter.com/oauth/access_token',
            authorize_url='https://api.twitter.com/oauth/authenticate',
            consumer_key=config['twitter']['t_api_key'],
            consumer_secret=config['twitter']['t_api_secret']
        )

        return twitter

    def fetch(self, todo):
        fetched = []

        for el in todo:
            api = self.connect()
            import pdb; pdb.set_trace()
            results = api.search(q=el.hashtag,result_type='recent')

            _logger.debug("Fetching data for #%s" % el.hashtag)

            for r in results:
                hashtags = []
                for h in r.entities['hashtags']:
                    hashtags.append(h['text'])

                data = {'oid': str(r.id),
                        'text': r.text,
                        'author': r.author.screen_name,
                        'avatar': r.user.profile_image_url_https,
                        'screen_name': r.user.screen_name,
                        'hashtags': hashtags,
                        'created_at': r.created_at}

                fetched.append(data)

        return fetched
