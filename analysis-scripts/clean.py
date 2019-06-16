# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets and applies pre-processing methods to "clean" them

import os

from pymongo import MongoClient

from twitter_preprocessor import TwitterPreprocessor

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

# Query all tweets
for tweet in tweets.find():
  # Query for the full_text property, keeping in mind that it might not exist in some deleted tweets
  # and apply all pre-processing methods plus converting the text to lowercase
  clean_tweet = TwitterPreprocessor(
    tweet["full_text"] if "full_text" in tweet else tweet["text"]).fully_preprocess().text.lower()
  # Update document with a new 'clean_tweet' property
  tweets.update_one({ "id": tweet["id"] }, { "$set": { "clean_tweet": clean_tweet } })
