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

    def get_auth(self):
        auth = tweepy.OAuthHandler(self.t_api_key, self.t_api_secret)
        auth.set_access_token(self.t_acc_token, self.t_acc_secret)

        return auth

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
        api = self.connect()

        done = []

        for el in todo:
            if el.hashtag not in done:
                done.append(el.hashtag)
                results = api.search(q=el.hashtag, result_type='recent', include_entities=True)

                _logger.debug("Fetching data for #%s" % el.hashtag)
                _logger.debug("Fetched %i elements" % len(results))

                for r in results:
                    hashtags = []
                    media = []

                    for h in r.entities['hashtags']:
                        hashtags.append(h['text'])

                    if 'media' in r.entities:
                        for m in r.entities['media']:
                            media.append(m['media_url'])

                    data = {'oid': str(r.id),
                            'text': r.text,
                            'author': r.author.screen_name,
                            'avatar': r.user.profile_image_url_https,
                            'screen_name': r.user.screen_name,
                            'hashtags': hashtags,
                            'created_at': r.created_at,
                            'retweet_count': r.retweet_count,
                            'media': media}

                    fetched.append(data)
            else:
                pass

        return fetched

    def get_user(self, screen_name):
        api = self.connect()
        user = api.get_user(screen_name, include_entities=1)

        return user

    def write_tweet(self, msg):
        api = self.connect()
        return True if api.update_status(msg) else False


    def fetch_stream(self, todo):
        fetched = []
        auth = self.get_auth()
        stream = tweepy.Stream(auth, StreamWatcherListener(), timeout=None)

        track_list = []

        for el in todo:
            track_list.append(el.hashtag)

        follow_list = None

        found = 0
        stream.filter(follow_list, track_list)


class StreamWatcherListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            print status
            hashtags = []
            media = []

            for h in r.entities['hashtags']:
                hashtags.append(h['text'])

            if 'media' in r.entities:
                for m in r.entities['media']:
                    media.append(m['media_url'])

            data = {'oid': str(r.id),
                    'text': r.text,
                    'author': r.author.screen_name,
                    'avatar': r.user.profile_image_url_https,
                    'screen_name': r.user.screen_name,
                    'hashtags': hashtags,
                    'created_at': r.created_at,
                    'retweet_count': r.retweet_count,
                    'media': media}

            return data

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print 'An error has occured! Status code = %s' % status_code
        return True  # keep stream alive

    def on_timeout(self):
        print 'Snoozing Zzzzzz'
