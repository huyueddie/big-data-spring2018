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

# New Scrapper function with write to Json fixed (without specifying a serch term)
def get_tweets(
    geo,
    out_file,
    search_term = '',
    tweet_per_query = 100,
    tweet_max = 150,
    since_id = None,
    max_id = -1,
    write = False
  ):
  tweet_count = 0
  all_tweets = pd.DataFrame()
  while tweet_count < tweet_max:
    try:
      if (max_id <= 0):
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            since_id = since_id
          )
      else:
        if (not since_id):
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1)
          )
        else:
          new_tweets = api.search(
            q = search_term,
            rpp = tweet_per_query,
            geocode = geo,
            max_id = str(max_id - 1),
            since_id = since_id
          )
      if (not new_tweets):
        print("No more tweets found")
        break
      for tweet in new_tweets:
         all_tweets = all_tweets.append(parse_tweet(tweet), ignore_index = True)
      max_id = new_tweets[-1].id
      tweet_count += len(new_tweets)
    except tweepy.TweepError as e:
      # Just exit if any error
      print("Error : " + str(e))
      break
  print (f"Downloaded {tweet_count} tweets.")
  if write == True:
     all_tweets.to_json(out_file)
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

# Customed parameters, trying to get 2000 tweets wihout a search term
latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
file_name = 'data/tweets.json'
t_max = 2000

# call the get_tweets function and let it run
tweets = get_tweets(geo = geocode_query, tweet_max = t_max, write = True, out_file = file_name)
df_tweets = pd.read_json('/Users/huyu/Desktop/github/big-data-spring2018/week-04/data/tweets.json')

tweets['location'].unique()

#clean location (Boston and Cambridge Case)
bos0 = tweets[tweets['location'].str.contains("Boston", case=False)]['location']
tweets['location'].replace(bos0, 'Boston, MA', inplace = True)

bos2 = tweets[tweets['location'].str.contains("boston")]['location']
tweets['location'].replace(bos2, 'Boston, MA', inplace = True)

bos3 = tweets[tweets['location'].str.contains("BOSTON")]['location']
tweets['location'].replace(bos3, 'Boston, MA', inplace = True)

cam0 = tweets[tweets['location'].str.contains("Cambridge")]['location']
tweets['location'].replace(cam0, 'Cambridge, MA', inplace = True)

cam1 = tweets[tweets['location'].str.contains("CAMBRIDGE")]['location']
tweets['location'].replace(cam0, 'Cambridge, MA', inplace = True)



# clean Duplicates
tweets[tweets.duplicated(subset = 'content', keep = False)]

tweets.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets

# initial grouping and sorting, trying to understand the Dataset
loc_tweets = tweets[tweets['location'] != '']
count_tweets = loc_tweets.groupby('location')['id'].count()
df_count_tweets = count_tweets.to_frame()
df_count_tweets
df_count_tweets.columns
df_count_tweets.columns = ['count']
df_count_tweets

df_count_tweets.sort_index()
df_count_tweets_10=df_count_tweets[df_count_tweets['count']>=10]


# Trying to create a pie yael_chart
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

plt.pie(df_count_tweets_10['count'], labels=df_count_tweets_10.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()

# Create a filter from df_tweets filtering only those that have values for lat and lon
tweets_geo = tweets[tweets['lon'].notnull() & tweets['lat'].notnull()]
len(tweets_geo)
len(tweets)

# Use a scatter plot to make a quick visualization of the data points
plt.scatter(tweets_geo['lon'], tweets_geo['lat'], s = 25)
plt.show()

# Export to CSV
tweets.to_csv('twitter_data.csv', sep=',', encoding='utf-8')








# search with a search term 'China'
latlng = '42.359416,-71.093993'
radius = '5mi'
geocode_query = latlng + ',' + radius
file_name = 'data/tweets_china.json'
t_max = 2000
tweets_china = get_tweets(geo = geocode_query, tweet_max = t_max, write = True, out_file = file_name, search_term = 'China')

df_china = pd.read_json('/Users/huyu/Desktop/github/big-data-spring2018/week-04/data/tweets_china.json')

tweets_china['location'].unique()

#clean location (Boston and Cambridge Case)
bos0 = tweets_china[tweets_china['location'].str.contains("Boston", case=False)]['location']
tweets_china['location'].replace(bos0, 'Boston, MA', inplace = True)

bos2 = tweets_china[tweets_china['location'].str.contains("boston")]['location']
tweets_china['location'].replace(bos2, 'Boston, MA', inplace = True)

bos3 = tweets_china[tweets_china['location'].str.contains("BOSTON")]['location']
tweets_china['location'].replace(bos3, 'Boston, MA', inplace = True)

cam0 = tweets_china[tweets_china['location'].str.contains("Cambridge")]['location']
tweets_china['location'].replace(cam0, 'Cambridge, MA', inplace = True)

cam1 = tweets_china[tweets_china['location'].str.contains("CAMBRIDGE")]['location']
tweets_china['location'].replace(cam0, 'Cambridge, MA', inplace = True)

tweets_china['location'].unique()

# clean Duplicates
tweets_china[tweets_china.duplicated(subset = 'content', keep = False)]

tweets_china.drop_duplicates(subset = 'content', keep = False, inplace = True)

tweets_china

# initial grouping and sorting, trying to understand the Dataset
loc_tweets_china = tweets_china[tweets_china['location'] != '']
count_tweets_china = loc_tweets_china.groupby('location')['id'].count()
df_count_tweets_china = count_tweets_china.to_frame()
df_count_tweets_china
df_count_tweets_china.columns
df_count_tweets_china.columns = ['count']
df_count_tweets_china

df_count_tweets_china.sort_index()
df_count_tweets_china_10=df_count_tweets_china[df_count_tweets_china['count']>=10]


# Trying to create a pie yael_chart
colors = ["#697dc6","#5faf4c","#7969de","#b5b246",
          "#cc54bc","#4bad89","#d84577","#4eacd7",
          "#cf4e33","#894ea8","#cf8c42","#d58cc9",
          "#737632","#9f4b75","#c36960"]

plt.pie(df_count_tweets_china_10['count'], labels=df_count_tweets_china_10.index.get_values(), shadow=False, colors=colors)
plt.axis('equal')
plt.tight_layout()
plt.show()

# Create a filter from df_tweets filtering only those that have values for lat and lon
china_geo = tweets_china[tweets_china['lon'].notnull() & tweets_china['lat'].notnull()]
len(china_geo) # in fact 0, no data
len(tweets_china)

# Use a scatter plot to make a quick visualization of the data points
plt.scatter(china_geo['lon'], china_geo['lat'], s = 25)
plt.show()

# Export to CSV
tweets_china.to_csv('twitter_china_data.csv', sep=',', encoding='utf-8')
