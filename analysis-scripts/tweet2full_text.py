# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets and queries Twitter for the full text in them

import json
import os

import tweepy
from bson.json_util import dumps
from pymongo import MongoClient

MONGO_HOST = os.getenv('MONGO_HOST')

CONSUMER_KEY = os.getenv('CONSUMER_KEY')
CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('ACCESS_TOKEN_SECRET')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit = True)

# Get a list of every tweet
list_of_ids = list(map(lambda x: x["id"], json.loads(dumps(tweets.find({ "full_text": None }, { "id": 1, "_id": 0 })))))

# Iterate through them, 100 at a time (because this is Twitter's rate limit)
for i in range(0, len(list_of_ids), 100):
  # Query for the full text
  results = api.statuses_lookup(list_of_ids[i:i + 100], tweet_mode = 'extended')
  tw_list = [x._json for x in results]
  print(i, len(tw_list))
  for tweet in tw_list:
    # Extra check for deleted tweets
    full_text = tweet["retweeted_status"]["full_text"] if "retweeted_status" in tweet else tweet["full_text"]
    # Update document with a new 'full_text' property
    tweets.update_one({ "id": tweet["id"] }, { "$set": { "full_text": full_text } })
