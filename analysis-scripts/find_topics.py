# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that iterates through a given set of timeframes and extracts topics by finding sets of bursty keywords

import os

import numpy as np
from pymongo import ASCENDING, DESCENDING, MongoClient
from textblob import TextBlob

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)

tweets = MongoClient(MONGO_HOST).twitterdb.twitter_search

# Timeframe window
interval = 1000 * 60 * 60 * 12  # 12 hours

# Earliest & latest tweets
start_time = float(list(tweets.find().sort("timestamp_ms", ASCENDING).limit(1))[0]["timestamp_ms"])
end_time = float(list(tweets.find().sort("timestamp_ms", DESCENDING).limit(1))[0]["timestamp_ms"])

# Tweets during each timeframe
tweets_per_timeframe = dict()

# Number of windows
windows_no = (end_time - start_time) // interval + 1

# Normalised usage of each term found during each timeframe
term_historic_usage = []
print(windows_no)
for window_no in range(int(windows_no)):
  print(window_no)
  # IDs of users that posted a specific term
  timeframe_users_per_term = dict()

  # Normalized usage of each term
  timeframe_usage_of_term = dict()

  # Words that were determined to be bursty
  timeframe_bursty_keywords = set()

  # Each tweet's terms
  timeframe_tweets = dict()

  # Users that posted a tweet
  timeframe_users = set()

  start_range = start_time + window_no * interval
  end_range = start_range + interval

  # Query all tweets that got posted in this timeframe and for everyone of them:
  for tweet in tweets.find({ "$and": [
    { "$expr": { "$lt": [{ "$toDouble": "$timestamp_ms" }, end_range] } },
    { "$expr": { "$gte": [{ "$toDouble": "$timestamp_ms" }, start_range] } }] }):

    tmp = ""
    # Add its user to the list
    timeframe_users.add(tweet["user"]["id"])

    # Add its tokens to the set of tokens
    tokens = TextBlob(tweet["clean_tweet"]).words
    for token in tokens:
      if token not in timeframe_users_per_term:
        timeframe_users_per_term[token] = set()
      timeframe_users_per_term[token].add(tweet["user"]["id"])
      tmp += token + " "

    # Add its hashtages to the set of tokens
    hashtags = list(map(lambda x: x["text"].lower(), tweet["entities"]["hashtags"]))
    for token in hashtags:
      if token not in timeframe_users_per_term:
        timeframe_users_per_term[token] = set()
      timeframe_users_per_term[token].add(tweet["user"]["id"])
      tmp += token + " "

    # Add its ID to the list of tweets
    timeframe_tweets[tweet["id_str"]] = tmp.strip()

  # For each term found
  for key, value in timeframe_users_per_term.items():
    # 1. Calculate its normalized usage in the frame (i.e. how many users used it)
    normalized_usage = len(value) / len(timeframe_users)
    timeframe_usage_of_term[key] = normalized_usage

    # 2. Calculate historic usage mean value and std. deviation
    mean = 0
    variance = 0

    for elem in term_historic_usage:
      if key in elem: mean += elem[key]
    if window_no != 0: mean /= window_no # normalize values

    for elem in term_historic_usage:
      if key in elem:
        variance += np.power(mean - elem[key], 2)
      else:
        variance += np.power(mean, 2)
    if window_no != 0: variance /= window_no # normalize values
    std = np.sqrt(variance)

    # 3. If it's more than μ + 2σ, add it to the set of bursty keywords
    z_score = 3 if std == 0 else (normalized_usage - mean) / std # some value that will surely make it bursty, if std = 0
    if z_score >= 2 and normalized_usage > 0.1: timeframe_bursty_keywords.add(key)

  term_historic_usage.append(timeframe_usage_of_term)
  tweets_per_timeframe[start_range] = len(timeframe_tweets)

  # Turn each keyword into a topic
  topics = []
  keywords_cooccurrences = dict()

  for keyword in timeframe_bursty_keywords:
    keywords_cooccurrences[keyword] = set()

    # Find each term that co-occurs with a bursty keyword
    for key, value in timeframe_tweets.items():
      if keyword in value:
        keywords_cooccurrences[keyword].add(key)

    topics.append([keyword, keywords_cooccurrences.get(keyword)])

  # If two topics share a lot (>5) of common co-occurring terms, merge them into one topic
  for j in range(len(topics)):
    for l in range(j):
      if len(topics[l][0]) < 1: continue
      intersected = [x for x in topics[j][1] if x in topics[l][1]]
      if len(intersected) > 5:
        topics[j][1] = intersected[:]
        topics[j][0] = f"{topics[j][0]} {topics[l][0]}"
        topics[l][0] = ""
        topics[l][1] = []

  frameTopics = []
  for x in topics:
    if x[0] != '': frameTopics.append(x[0])

  # Write results to a file for manual inspection
  with open('topics.txt', 'a') as fp:
    if len(frameTopics) == 0: continue
    fp.write(f"{int(start_range)}:{frameTopics}\n")
