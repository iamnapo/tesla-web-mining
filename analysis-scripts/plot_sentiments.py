# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets, count each emotion's appearances and plots their daily count, using plotly

import json
import os
from datetime import datetime, timedelta

import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from pymongo import ASCENDING, DESCENDING, MongoClient

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

# Get earliest and latest timestamps
start_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", ASCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()
end_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", DESCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()

# Initialize a dict of arrays in order to save each emotion's daily count
sentiment_daily_counts = dict()
for sentiment in ["anger", "joy", "disgust", "fear", "sadness", "surprise"]:
  sentiment_daily_counts[sentiment] = [0 for i in range((end_date - start_date).days + 1)]

# Calculate emotion daily count
for tweet in tweets.find():
  if "six_sentiments" not in tweet:
    print(tweet)
  for sentiment in list(tweet["six_sentiments"]):
    tweet_date = datetime.fromtimestamp(float(tweet["timestamp_ms"]) / 1000).date()
    sentiment_daily_counts[sentiment][(tweet_date - start_date).days] += 1

# Create an interactive HTMl plot of the results
data = []
labels = [(start_date + timedelta(days = i)).strftime("%d/%m") for i in range((end_date - start_date).days + 1)]
ticks = [x for x in range((end_date - start_date).days + 1)]
layout = go.Layout(title = 'Sentiments per day', xaxis = go.layout.XAxis(ticktext = labels, tickvals = ticks),
                   yaxis = go.YAxis(showticklabels = False))
i = 0
tmp = []
for sentiment, counts in sentiment_daily_counts.items():
  tmp.append({ "y": list(np.add(np.array(counts) / np.array(counts).max(), i)), "name": sentiment })

  # Note that we plot the normalized value (divide by the max value) to get a better understanding of change
  data.append(
    go.Scatter(x = ticks, y = np.add(np.array(counts) / np.array(counts).max(), i), name = sentiment, mode = 'lines+markers',
               line = { 'shape': 'spline', 'smoothing': 0.75 }))
  i += 1

fig = go.Figure(data = data, layout = layout)
plot(fig, filename = 'sent_per_day.html')

# Also save them to a json file, so we can recreate the interactive plot in the website
with open('sent_per_day.json', 'w', encoding = 'utf-8') as outfile:
  json.dump({ "data": tmp, "ticks": ticks, "labels": labels }, outfile, ensure_ascii = False, indent = 2)
