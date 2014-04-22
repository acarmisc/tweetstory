import tweepy
import logging

# must be better
logging.basicConfig(level=logging.DEBUG)


class twitterClient(object):

    def __init__(self, config_dict=False, consumer_key=False,
                 consumer_secret=False, key=False, secret=False):

        if config_dict:
            self.consumer_key = config_dict['consumer_key']
            self.consumer_secret = config_dict['consumer_secret']
            self.key = config_dict['key']
            self.secret = config_dict['secret']
        else:
            self.consumer_key = consumer_key
            self.consumer_secret = consumer_secret
            self.key = key
            self.secret = secret

    def connect(self):
        auth = tweepy.OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.key, self.secret)

        api = tweepy.API(auth)

        return api

    def fetch(self, todo):
        fetched = []

        for el in todo:
            api = self.connect()
            results = api.search(q=el['hashtag'])

            logging.debug("Fetching data for #%s" % el['hashtag'])

            for r in results:
                hashtags = []
                for h in r.entities['hashtags']:
                    hashtags.append({'tag': h['text']})

                data = {'oid': r.id,
                        'text': r.text,
                        'author': r.author.screen_name,
                        'avatar': r.user.profile_image_url_https,
                        'hashtags': hashtags,
                        'created_at': r.created_at}

                fetched.append(data)

        return fetched
