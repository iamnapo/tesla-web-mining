# Napoleon-Christos Oikonomou, AEM: 16
# Maria Kouvela, AEM: 9
# Script that uses the provided dataset to create a multi-label classifier in order to classify each tweet base on the emotions
# that are present in its language

import json
import os

import numpy as np
import pandas as pd
from bson.json_util import dumps
from bson.objectid import ObjectId
from pymongo import MongoClient
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from skmultilearn.problem_transform import BinaryRelevance

from twitter_preprocessor import TwitterPreprocessor

MONGO_HOST = os.getenv('MONGO_HOST')

client = MongoClient(MONGO_HOST)
db = client.twitterdb.twitter_search

tweets = json.loads(dumps(db.find({ }, { "clean_tweet": 1 })))

# Get a list of all tweets
list_of_tweet_text = list(map(lambda x: x["clean_tweet"], tweets))
list_of_tweet_ids = list(map(lambda x: x["_id"], tweets))

# Read the provided training set
df = pd.read_csv("datasets/emotions-classification-train.txt", delimiter = '	')

# Preprocess it in order to make it have the same "form" as the tweets
X = df['Tweet'].apply(lambda x: TwitterPreprocessor(x).fully_preprocess().text.lower().strip()).values
y = df.iloc[:, [2, 6, 4, 5, 10, 11]].values  # a) anger, b) joy, c) disgust, d) fear, e) sadness, f) surprise

# Create a bag-of-words representation of every tweet (both the ones provided and the ones we want to clasify
vectorizer = CountVectorizer(max_features = 20000).fit(np.concatenate((X, list_of_tweet_text)))
X = vectorizer.transform(X)
list_of_tweet_text = vectorizer.transform(list_of_tweet_text)

# Split the input dataset in order to evaluate our resutls
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 14)

# Train a RandomForest classifier, using the Binary Relevance dataset transormation method
model = BinaryRelevance(classifier = RandomForestClassifier(n_estimators = 200, random_state = 14, n_jobs = -1),
                        require_dense = [False, True])
model.fit(X_train, y_train)

# Print the evaluation results
predictions = model.predict(X_test)
print(classification_report(y_test, predictions))

# Use the trained model to clasify each tweet and save the results into the 'six_sentiments' property
predictions = model.predict(list_of_tweet_text)
for tweet_ind, prediction in enumerate(predictions):
  labels = []
  for ind, label in enumerate(prediction.A.tolist()[0]):
    if label == 1:
      labels.append(["anger", "joy", "disgust", "fear", "sadness", "surprise"][ind])
  db.update_one({ "_id": ObjectId(list_of_tweet_ids[tweet_ind]["$oid"]) }, { "$set": { "six_sentiments": labels } })
