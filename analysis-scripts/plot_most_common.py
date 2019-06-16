# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets finds the 10 most common hashtags
# and plots their daily count, using plotly

import json
import os
from collections import Counter
from datetime import datetime, timedelta

import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from pymongo import ASCENDING, DESCENDING, MongoClient

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

hashtag_counts = Counter()

# Iterate through tweets and collect all hashtags
for tweet in tweets.find():
  for hashtag in list(map(lambda x: x["text"].lower(), tweet["entities"]["hashtags"])):
    hashtag_counts[hashtag] += 1

print(hashtag_counts.most_common(10))

# Find the 10 most common ones
most_common_10 = list(map(lambda x: x[0], hashtag_counts.most_common(10)))

# Get earliest and latest timestamps
start_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", ASCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()
end_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", DESCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()

# Initialize a dict of arrays in order to save hashtag daily counts
hashtag_daily_counts = dict()
for hashtag in most_common_10:
  hashtag_daily_counts[hashtag] = [0 for i in range((end_date - start_date).days + 1)]

# Iterate through tweets again and count each of the 10 most common hashtags' daily occurence
for tweet in tweets.find():
  for hashtag in list(map(lambda x: x["text"].lower(), tweet["entities"]["hashtags"])):
    if hashtag in hashtag_daily_counts:
      tweet_date = datetime.fromtimestamp(float(tweet["timestamp_ms"]) / 1000).date()
      hashtag_daily_counts[hashtag][(tweet_date - start_date).days] += 1

data = []
labels = [(start_date + timedelta(days = i)).strftime("%d/%m") for i in range((end_date - start_date).days + 1)]
ticks = [x for x in range((end_date - start_date).days + 1)]
layout = go.Layout(title = 'Common word frequency per day',
                   xaxis = go.layout.XAxis(ticktext = labels, tickvals = ticks, showgrid = True),
                   yaxis = go.YAxis(showticklabels = False))

i = 0
tmp = []
# Plot the normalized results one above the other so they are easier to see
for hashtag, counts in hashtag_daily_counts.items():
  tmp.append({ "y": list(np.add(np.divide(counts, np.max(counts)), i)), "name": hashtag })
  data.append(go.Scatter(x = ticks, y = np.add(np.divide(counts, np.max(counts)), i), name = hashtag))
  i += 1

fig = go.Figure(data = data, layout = layout)
# Also create an interactive HTML file
plot(fig, filename = 'freq_per_day.html')

# Also save them to a json file, so we can recreate the interactive plot in the website
with open('most_common.json', 'w', encoding = 'utf-8') as outfile:
  json.dump({ "data": tmp, "ticks": ticks, "labels": labels }, outfile, ensure_ascii = False, indent = 2)
