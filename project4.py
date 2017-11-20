# Olivia Gardella
# SI206 final project

import sqlite3
import json
import unittest
import itertools
import collections
import api_info         #import python file that has all the api keys

#notes: plot.ly to visualize


## Part 1 -------------------------------------------------------------------------------------------


# set up cache
CACHE_FNAME = "project4cache.json"
try:                                            #if the cache file already exists
    cache_file = open(CACHE_FNAME,'r')          #open and read the cache file
    cache_contents = cache_file.read()
    cache_file.close()                          #close the cache file
    CACHE_DICTION = json.loads(cache_contents)  #load cache's contents into the cache dictionary using json
except:                                         #if the cache file doesn't exsit already
    CACHE_DICTION = {}                          #create any empty dictionary for the cache


# utilize 5 api's for social networks

fb_consumer_key = api_info.fb_consumer_key
fb_consumer_secret = api_info.fb_consumer_secret
fb_access_token = api_info.fb_access_token
fb_access_token_secret = api_info.fb_access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #change
auth.set_access_token(access_token, access_token_secret) #change

def fbapi(user):                                #define the facebook api function
    pass

def instagramapi(user):                         #define the instagram api function
    pass


linkedin_consumer_key = api_info.linkedin_consumer_key
linkedin_consumer_secret = api_info.linkedin_consumer_secret
linkedin_access_token = api_info.linkedin_access_token
linkedin_access_token_secret = api_info.linkedin_access_token_secret
def linkedinapi(user):                          #define the linkedin api function
    pass

pin_consumer_key = api_info.pin_consumer_key
pin_consumer_secret = api_info.pin_consumer_secret
pin_access_token = api_info.pin_access_token
pin_access_token_secret = api_info.pin_access_token_secret
def pinterestapi(user):                         #define the pinterest api function
    pass

spotify_consumer_key = api_info.spotify_consumer_key
spotify_consumer_secret = api_info.spotify_consumer_secret
spotify_access_token = api_info.spotify_access_token
spotify_access_token_secret = api_info.spotify_access_token_secret
def spotifyapi(user):                           #define the spotify api function
    pass


# access exactly 100 interactions


# find the days these interactions took place


# write the data to the database


# create a report



## Part 2 -------------------------------------------------------------------------------------------
# create a report for overall project (not code)

## Part 3 ------------------------------------------------------------------------------------------
