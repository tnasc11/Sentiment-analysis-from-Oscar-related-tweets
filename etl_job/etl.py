#from pymongo import MongoClient
import pymongo
from sqlalchemy import create_engine
import re
import logging
import random
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as analyzer

s  = analyzer()

# accessing mongodb
#client = MongoClient()
import time

time.sleep(10) 
database_client = pymongo.MongoClient("mongodb")
db = database_client.twitter

# accessing postgres and creating a table
# connection string for postgres "postgres://username:password@container_name:5555"
PG = create_engine("postgresql://postgres:1234@postgresdb:5432/twitter", echo=True)
PG.execute("""CREATE TABLE IF NOT EXISTS tweets(
    text VARCHAR(500),
    geo VARCHAR(2),
    sentiment NUMERIC);"""
)


# get_tweets from Mongo (Extract)

tweets = list(db.collections.tweets.find())

print(tweets)
def ETL():       
    for tweet in tweets:
        text = tweet['text']
        try:
            geo = tweet['geo']
        except KeyError:
            geo = "location not found"

        print(tweet['text'])
        result = re.sub(r"http\S+", "", text)
        sentiment = s.polarity_scores(result)
        score = sentiment['compound']  # placeholder value
        query = "INSERT INTO tweets VALUES (%s,%s,%s);"
        PG.execute(query, (result, geo, score))
        logging.critical("Wrote into postgres!")

ETL()
    

