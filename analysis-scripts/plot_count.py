# Napoleon-Christos Oikonomou, AEM: 16
# Maria-Kouvela, AEM: 9
# Script that iterates through tweets and plots their daily count, using plotly

import json
import os
from datetime import datetime

import plotly.graph_objs as go
from plotly.offline import plot
from pymongo import MongoClient

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

tweets_per_day = []

# Query all tweets
for tweet in tweets.find({ }, { "timestamp_ms": 1 }):
  # For each one add a string in the form "day/month" to a list
  tweets_per_day.append(datetime.fromtimestamp(float(tweet["timestamp_ms"]) / 1000).strftime("%d/%m"))

# Plot the results in a histogram
layout = go.Layout(title = 'Tweet Activity Over Time', bargap = 0.2)
data = [go.Histogram(x = tweets_per_day, marker = dict(color = 'blue'), opacity = 0.75)]
fig = go.Figure(data = data, layout = layout)
# Also create an interactive HTML file
plot(fig, filename = 'tweet_per_day.html')

# Also save them to a json file, so we can recreate the interactive plot in the website
with open('tweets_time.json', 'w', encoding = 'utf-8') as outfile:
  json.dump(tweets_per_day, outfile, ensure_ascii = False, indent = 2)
