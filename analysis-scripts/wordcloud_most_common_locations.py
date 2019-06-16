# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets, creates a list of all locations reported by users, after removing special characters,
# multiple blank spaces and converting it to lowercase  and then uses the wordcloud library to create a word-cloud of
# the 200 most common phrases (words and bigrams)

import os

import matplotlib.pyplot as plt
from pymongo import MongoClient
from wordcloud import WordCloud

from twitter_preprocessor import TwitterPreprocessor

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

locs = ""

# Query all tweets
for tweet in tweets.find():
  # concatenate every user's location together
  if "location" in tweet["user"] and tweet["user"]["location"] is not None:
    locs += f" {TwitterPreprocessor(tweet['user']['location']).remove_special_characters().remove_blank_spaces().text.lower()}"

# Use wordcloud to create a word-cloud of the 200 most common phrases (words and bigrams)
wordcloud = WordCloud(stopwords = { 'Earth' }, background_color = "white", width = 1600, height = 800,
                      normalize_plurals = False).generate(locs)
plt.figure()
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.title('Common locations of users')
plt.show()
