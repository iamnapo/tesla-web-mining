# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets, calculates their polarity using the textblob library, saves the 'overall_sentiment'
# base on polarity's value and the calculates and creates a plot of the daily count of each sentiment (positive, negative,
# neutral), using plotly

import json
import os
from datetime import datetime, timedelta

import plotly.graph_objs as go
from plotly.offline import plot
from pymongo import ASCENDING, DESCENDING, MongoClient
from textblob import TextBlob

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

# Query all tweets
for tweet in tweets.find({ "overall_sentiment": None }):
  # Decide on their sentiment, based on polarity value
  polarity = TextBlob(tweet["clean_tweet"]).sentiment.polarity
  if polarity > 0:
    sentiment = "positive"
  elif polarity < 0:
    sentiment = "negative"
  else:
    sentiment = "neutral"
  # Update them with the new 'overall_sentiment' property
  tweets.update_one({ "_id": tweet["_id"] }, { "$set": { "overall_sentiment": sentiment } })

# Earliest & latest timestamps
start_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", ASCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()
end_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", DESCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()

# Initialize a dict of arrays in order to save sentiments daily counts
overall_sentiment_daily_counts = dict()
for sentiment in ["negative", "neutral", "positive"]:
  overall_sentiment_daily_counts[sentiment] = [0 for i in range((end_date - start_date).days + 1)]

# Calculate sentiment daily count
for tweet in tweets.find({ }, { "overall_sentiment": 1, "_id": 0, "timestamp_ms": 1 }):
  tweet_date = datetime.fromtimestamp(float(tweet["timestamp_ms"]) / 1000).date()
  overall_sentiment_daily_counts[tweet["overall_sentiment"]][(tweet_date - start_date).days] += 1

data = []
labels = [(start_date + timedelta(days = i)).strftime("%d/%m") for i in range((end_date - start_date).days + 1)]
ticks = [x for x in range((end_date - start_date).days + 1)]
layout = go.Layout(title = 'Overall sentiment per day', xaxis = go.layout.XAxis(ticktext = labels, tickvals = ticks),
                   barmode = 'relative')
tmp = []

# Create an interactive HTMl plot of the results
for sentiment, counts in overall_sentiment_daily_counts.items():
  if sentiment == 'positive':
    color = 'green'
  elif sentiment == 'negative':
    color = 'red'
  else:
    color = 'gray'
  data.append({ 'x': ticks, 'y': counts, 'name': sentiment, 'type': 'bar', 'marker': { 'color': color } })
  tmp.append({ 'y': counts, 'color': color, 'name': sentiment })
  fig = go.Figure(data = data, layout = layout)
  plot(fig, filename = 'ov_sentiment_per_day.html')

# Also save them to a json file, so we can recreate the interactive plot in the website
with open('ov_sentiment_per_day.json', 'w', encoding = 'utf-8') as outfile:
  json.dump({ "data": tmp, "ticks": ticks, "labels": labels }, outfile, ensure_ascii = False, indent = 2)
