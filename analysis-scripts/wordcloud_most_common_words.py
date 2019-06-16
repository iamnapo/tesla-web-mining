# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets, creates a list of all tokens that appeared (a. in all tweets and b. in tweets with
# a specific emotion) and then uses the wordcloud library to create a word-cloud of the 200 most common phrases (words and bigrams)

import os

import matplotlib.pyplot as plt
from pymongo import MongoClient
from wordcloud import WordCloud

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

sentiment_text = dict()
clean_text = ""
for sentiment in ["anger", "joy", "disgust", "fear", "sadness", "surprise"]:
  sentiment_text[sentiment] = ""

# Query all tweets
for tweet in tweets.find():
  # concatenate every tweet's text together
  clean_text += f" {tweet['clean_tweet']}"
  for sentiment in list(tweet["six_sentiments"]):
    # also concatenate tweets that exhibit the same emotion
    sentiment_text[sentiment] += f" {tweet['clean_tweet']}"

# Use wordcloud to create a word-cloud of the 200 most common phrases (words and bigrams)
wordcloud = WordCloud(stopwords = { "new", "it" }, background_color = "white", width = 1600, height = 800).generate(clean_text)
plt.figure()
plt.imshow(wordcloud, interpolation = "bilinear")
plt.axis("off")
plt.title('Common phrases in tweets')

# Use wordcloud to create a word-cloud of the 200 most common phrases (words and bigrams)
for sentiment in sentiment_text:
  wordcloud = WordCloud(stopwords = { "new", "it" }, background_color = "white", width = 1600, height = 800).generate(
    sentiment_text[sentiment])
  plt.figure()
  plt.imshow(wordcloud, interpolation = "bilinear")
  plt.axis("off")
  plt.title(f'Common phrases in tweets characterized as {sentiment}-tweets')

plt.show()
