# Napoleon-Christos Oikonomou, AEM: 16
# Maria-Kouvela, AEM: 9
# Script that iterates through tweets and tries to find thei location, either by users providing the specific coordinates of a
# tweet, or by users providing a known place. Then it plot a map of every tweet found, using the overall sentiment for the point's
# color

import json
import os

import numpy as np
import plotly.graph_objs as go
from plotly.offline import plot
from pymongo import MongoClient

MONGO_HOST = os.getenv('MONGO_HOST')
MAP_BOX_TOKEN = os.getenv('MAP_BOX_TOKEN')

client = MongoClient(MONGO_HOST)
db = client.twitterdb
tweets = db.twitter_search

lat = []
lon = []
users = []
colors = []

# Query all tweets
for tweet in tweets.find():
  # If the user provided a set of coordinates save it
  if tweet["coordinates"] is not None and 'coordinates' in tweet["coordinates"]:
    lon.append(tweet["coordinates"]["coordinates"][0])
    lat.append(tweet["coordinates"]["coordinates"][1])
    users.append(tweet["user"]["screen_name"])
    # Find out what color to use for this point
    if tweet["overall_sentiment"] == "positive":
      colors.append("green")
    elif tweet["overall_sentiment"] == "negative":
      colors.append("red")
    else:
      colors.append("gray")
  # else check if the user provided a known place, and save its location
  elif tweet["place"] is not None:
    box = tweet["place"]["bounding_box"]["coordinates"][0]
    lon.append(np.mean((box[0][0], box[1][0], box[2][0], box[3][0])))
    lat.append(np.mean((box[0][1], box[1][1], box[2][1], box[3][1])))
    users.append(tweet["user"]["screen_name"])
    # Find out what color to use for this point
    if tweet["overall_sentiment"] == "positive":
      colors.append("green")
    elif tweet["overall_sentiment"] == "negative":
      colors.append("red")
    else:
      colors.append("gray")

print(f"Found {len(users)} geo-tagged tweets!")

# Create an interactive HTML map, using MapBox
data = [go.Scattermapbox(lat = lat, lon = lon, mode = 'markers', marker = go.scattermapbox.Marker(size = 5, color = colors),
                         text = users)]
layout = go.Layout(autosize = True, hovermode = 'closest', title = 'Geo-location of users',
                   mapbox = go.layout.Mapbox(bearing = 0, accesstoken = MAP_BOX_TOKEN, zoom = 1,
                                             center = go.layout.mapbox.Center(lat = np.mean(lat), lon = np.mean(lon))))
fig = go.Figure(data = data, layout = layout)
plot(fig, filename = 'geo_loc.html')

# Also save them to a json file, so we can recreate the interactive plot in the website
with open('geo_loc.json', 'w', encoding = 'utf-8') as outfile:
  json.dump({ "lat": lat, "lon": lon, "colors": colors, "lat_mean": np.mean(lat), "lon_mean": np.mean(lon),
              "users": users }, outfile, ensure_ascii = False, indent = 2)
