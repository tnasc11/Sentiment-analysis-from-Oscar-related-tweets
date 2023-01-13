
from Twitter_credentials import *
import tweepy
import logging
import pymongo

##################
# Authentication #
##################

twitter_client = tweepy.Client(
    bearer_token=Bearer_token,
    wait_on_rate_limit=True,
)

if twitter_client:
    logging.critical('\nAuthetication OK')
else:
    logging.critical('\nVerify your credentials')

########################
# Get User Information #
########################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_user
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/user

theacademy = twitter_client.get_user(
    username='theacademy',
    user_fields=['created_at', 'description', 'location',
                 'public_metrics', 'profile_image_url']
)

user = theacademy.data

print(dict(user))


#########################
# Get a user's timeline #
#########################

# https://docs.tweepy.org/en/stable/pagination.html#tweepy.Paginator
# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.get_users_tweets
# https://developer.twitter.com/en/docs/twitter-api/data-dictionary/object-model/tweet

cursor = tweepy.Paginator(
    method=twitter_client.get_users_tweets,
    id=user.id,
    exclude=['replies', 'retweets'],
    tweet_fields=['author_id', 'created_at', 'public_metrics']
).flatten(limit=100)

for tweet in cursor:
    print(tweet.text)


#####################
# Search for Tweets #
#####################

# https://docs.tweepy.org/en/stable/client.html#tweepy.Client.search_recent_tweets
# https://developer.twitter.com/en/docs/twitter-api/tweets/search/integrate/build-a-query


# In[7]:


rottent = twitter_client.get_user(
    username='rottentomatoes',
    user_fields=['created_at', 'description', 'location',
                'public_metrics', 'profile_image_url']
)
user = rottent.data

print(dict(user))


# In[8]:

#### 3. SEARCHING FOR TWEETS #####

# Defining a query search string
#query = "Oscars2023 -is:retweet -is:reply -is:quote -has:links is:verified place_country:US lang:en"
query = "Oscars2023 -is:retweet -is:reply -is:quote lang:en"

search_tweets = twitter_client.search_recent_tweets(query=query, tweet_fields=['id','created_at','text','geo'], max_results=50)

#search_tweets = twitter_client.search_recent_tweets(query=query,
#                                    #start_time = "2022-01-01T00:00:00Z",
#                                    tweet_fields=["id", "author_id", "text", "created_at", "place"],
#                                    user_fields=["id", "name", "username"], max_results=100)


database_client = pymongo.MongoClient("mongodb")
db = database_client.twitter

for tweet in search_tweets.data:
    
    logging.critical(f'\n\n\nINCOMING TWEET username {tweet.id}:\n{tweet.text}\ncountry:{tweet.geo}\n\n\n')
    #record = {'text': tweet.text, 'id': tweet.id, 'created_at': tweet.created_at}
    file = open('tweets.txt',mode='a')
    file.write(f'\n\n\nINCOMING TWEET\n{tweet.text}\n\n\n')
    file.close()
    db.collections.tweets.insert_one(dict(tweet))