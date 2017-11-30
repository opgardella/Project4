# Olivia Gardella
# SI206 final project

import sqlite3
import json
import unittest
import itertools
import collections
import api_info         #import python file that has all the api keys
import facebook
import requests

#notes: plot.ly to visualize
#dont have to use social media, can use: darksky, google maps


## Part 1 -------------------------------------------------------------------------------------------

#to take care of unicode error, must use uprint instead of print
import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

# set up cache
CACHE_FNAME = "project4cache.json"
try:                                            #if the cache file already exists
    cache_file = open(CACHE_FNAME,'r')          #open and read the cache file
    cache_contents = cache_file.read()
    cache_file.close()                          #close the cache file
    CACHE_DICTION = json.loads(cache_contents)  #load cache's contents into the cache dictionary using json
except:                                         #if the cache file doesn't exsit already
    CACHE_DICTION = {}                          #create any empty dictionary for the cache


# Utilize 2 api's: Facebook and DarkSky

# Facebook api ------
fb_access_token = api_info.fb_access_token

auth = tweepy.OAuthHandler(consumer_key, consumer_secret) #change this!
auth.set_access_token(access_token, access_token_secret) #change this!

def fbapi(user):                                #define the facebook api function
    if user in CACHE_DICTION:
        uprint("using cached data")
    else:
        uprint("getting data from internet")

# access exactly 100 interactions for the api

# find the days these interactions took place

# write the data to the database

# create a report



# DarkSky api -------
base_url = 'https://api.darksky.net/forecast/'
api_key = api_info.darksky_key
lat_lng = '42.280841, -83.738115'
full_url = base_url + api_key + '/'+lat_lng

def darkskyapi(location):
    if location in CACHE_DICTION:                       #if the location is already in the cache
        uprint("using cached data")                     #print that we are getting the data from the cache
        darksky_results = CACHE_DICTION[location]       #grab data from the cache
    else:                                               #if the locaiton is not already in the cache
        uprint("getting data from internet")            #print that we are getting data from the internet
        darksky_results = requests.get(full_url)
        data = json.loads(response.text)
        hourly = data['hourly']['data']

        CACHE_DICTION[location] = darksky_results
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return darksky_results



# access exactly 100 interactions for the api


# find the days these interactions took place


# write the data to the database


# create a report



## Part 2 -------------------------------------------------------------------------------------------
# create a report for overall project (not code)

## Part 3 ------------------------------------------------------------------------------------------
