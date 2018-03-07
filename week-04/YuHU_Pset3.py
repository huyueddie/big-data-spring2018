import jsonpickle
import tweepy
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import os
os.chdir('week-04')
from twitter_keys import api_key, api_secret

def auth(key, secret):
  auth = tweepy.AppAuthHandler(key, secret)
  api = tweepy.API(auth, wait_on_rate_limit = True, wait_on_rate_limit_notify = True)
  # Print error and exit if there is an authentication error
  if (not api):
      print ("Can't Authenticate")
      sys.exit(-1)
  else:
      return api
api = auth(api_key, api_secret)

# Old Scrapper function without specifying a serch term
def get_tweets(geo, out_file, search_term = '', tweet_per_query = 100, tweet_max = 150, since_id = None, max_id = -1, write = False):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(q = search_term, rpp = tweet_per_query, geocode = geo)
        else:
          new_tweets = api.search(q = search_term, rpp = tweet_per_query, geocode = geo, since_id = since_id)
      else:
        if (not since_id):
          new_tweets = api.search(q = search_term, rpp = tweet_per_query, geocode = geo, max_id = str(max_id - 1))
        else:
          new_tweets = api.search(q = search_term, rpp = tweet_per_query, geocode = geo, max_id = str(max_id - 1), since_id = since_id)
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
        all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
        if write == True:
            with open(out_file, 'w') as f:
                f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  return all_tweets

# Parsing the tweets
def parse_tweet(tweet):
  p = pd.Series()
  if tweet.coordinates != None:
    p['lat'] = tweet.coordinates['coordinates'][0]
    p['lon'] = tweet.coordinates['coordinates'][1]
  else:
    p['lat'] = None
    p['lon'] = None
  p['location'] = tweet.user.location
  p['id'] = tweet.id_str
  p['content'] = tweet.text
  p['user'] = tweet.user.screen_name
  p['user_id'] = tweet.user.id_str
  p['time'] = str(tweet.created_at)
  return p

# Customed parameters, trying to get 20000 tweets wihout a search term
latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
file_name = 'data/tweets.json'
t_max = 20000

# call the get_tweets function and let it run
tweets = get_tweets(geo = geocode_query, tweet_max = t_max, write = True, out_file = file_name)
# implement this line after the data are gathered
tweets.to_json('/Users/huyu/Desktop/github/big-data-spring2018/week-04/data/tweets.json')



#clean location, code taught by Yael
bos = tweets[tweets['location'].str.contains("Boston", case=False)]['location']
tweets['location'].replace(bos, 'Boston, MA', inplace = True)

bos2 = tweets[tweets['location'].str.contains("boston")]['location']
tweets['location'].replace(bos2, 'Boston, MA', inplace = True)

bos3 = tweets[tweets['location'].str.contains("BOSTON")]['location']
tweets['location'].replace(bos3, 'Boston, MA', inplace = True)

cambridge = tweets[tweets['location'].str.contains("Cambridge")]['location']
tweets['location'].replace(cambridge, 'Cambridge, MA', inplace = True)
















# china version
tweets = get_tweets(geo = geocode_query, tweet_max = t_max, write = True, out_file = file_name)
tweets.to_json('/Users/huyu/Desktop/github/big-data-spring2018/week-04/data/tweets.json')

china = pd.read_json('/Users/huyu/Desktop/github/big-data-spring2018/week-04/data/tweets.json')


china.shape
china.head()


china['location'].unique()
tweets_general.shape
tweets_general.head()

# clean the general tweets
loc_tweets_general = tweets_general[tweets_general['location'] != '']
count_tweets_general = loc_tweets_general.groupby('location')['id'].count()
df_count_tweets_general = count_tweets_general.to_frame()
df_count_tweets_general
df_count_tweets_general.columns
df_count_tweets_general.columns = ['count']
df_count_tweets_general
df_count_tweets_general.sort_index()

# Create a list of colors (from iWantHue)
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

# Create a pie chart
plt.pie(df_count_tweets_general['count'], labels=df_count_tweets_general.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()
