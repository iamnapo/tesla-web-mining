# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that creates a listener to the Twitter Streaming API and writes each incoming tweet to a MongoDB database

import json
import os

import tweepy
from pymongo import MongoClient

MONGO_HOST = os.getenv('MONGO_HOST')

WORDS = ['#Tesla', '#TeslaMotors', '#ElonMusk', '#Elon', '#Model3', '#ModelX', '#ModelY', '#TeslaRoadster']

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')


class StreamListener(tweepy.StreamListener):

  @staticmethod
  def on_connect(**kwargs):
    print("You are now connected to the streaming API.")

  @staticmethod
  def on_error(status_code, **kwargs):
    print('An Error has occurred: ' + repr(status_code))
    return False

  @staticmethod
  def on_data(data, **kwargs):
    try:
      client = MongoClient(MONGO_HOST)
      db = client.twitterdb

      data_json = json.loads(data)
      print("Tweet collected at " + str(data_json['created_at']))

      db.twitter_search.insert_one(data_json)
    except Exception as e:
      print(e)


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
listener = StreamListener(api = tweepy.API(wait_on_rate_limit = True))
streamer = tweepy.Stream(auth = auth, listener = listener)
print("Tracking: " + str(WORDS))
streamer.filter(track = WORDS)
