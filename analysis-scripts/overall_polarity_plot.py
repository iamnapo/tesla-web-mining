# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through tweets, calculates their polarity using the textblob library, saves it in the 'overall_polarity'
# property and creates a plot of its mean daily value using plotly

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
for tweet in tweets.find({ "overall_polarity": None }):
  polarity = TextBlob(tweet["clean_tweet"]).sentiment.polarity
  # Update them with the new 'overall_polarity' property
  tweets.update_one({ "_id": tweet["_id"] }, { "$set": { "overall_polarity": polarity } })

# Earliest & latest timestamps
start_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", ASCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()
end_date = datetime.fromtimestamp(
  float(list(tweets.find().sort("timestamp_ms", DESCENDING).limit(1))[0]["timestamp_ms"]) / 1000).date()

# Initialize a dict of arrays in order to save sentiments daily sum and counts
overall_polarity_daily = [[0, 0] for i in range((end_date - start_date).days + 1)]

for tweet in tweets.find({ }, { "overall_polarity": 1, "_id": 0, "timestamp_ms": 1 }):
  tweet_date = datetime.fromtimestamp(float(tweet["timestamp_ms"]) / 1000).date()
  overall_polarity_daily[(tweet_date - start_date).days][0] += tweet["overall_polarity"]
  overall_polarity_daily[(tweet_date - start_date).days][1] += 1

# Create an interactive HTMl plot of the results
labels = [(start_date + timedelta(days = i)).strftime("%d/%m") for i in range((end_date - start_date).days + 1)]
ticks = [x for x in range((end_date - start_date).days + 1)]
layout = go.Layout(title = 'Polarity per day', xaxis = go.layout.XAxis(ticktext = labels, tickvals = ticks))

# Note that we plot the mean values
data = [
  go.Scatter(x = ticks, y = list(map(lambda x: 0 if x[1] == 0 else x[0] / x[1], overall_polarity_daily)), mode = 'lines+markers',
             line = { 'shape': 'spline', 'smoothing': 1.3 })]

fig = go.Figure(data = data, layout = layout)
plot(fig, filename = 'ov_polarity_per_day.html')

# Also save them to a json file, so we can recreate the interactive plot in the website
with open('ov_polarity_per_day.json', 'w', encoding = 'utf-8') as outfile:
  json.dump(
    { "data": list(map(lambda x: 0 if x[1] == 0 else x[0] / x[1], overall_polarity_daily)), "ticks": ticks, "labels": labels },
    outfile, ensure_ascii = False, indent = 2)
