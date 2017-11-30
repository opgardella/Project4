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
graph = facebook.GraphAPI(fb_access_token)

def fbapi():                                #define the facebook api function
    if user in CACHE_DICTION:
        uprint("using cached data")
        graph.get_connections(id='me', connection_name='posts')
    else:
        uprint("getting data from internet")

# access exactly 100 interactions for the api; 100 of my posts (or less if I don't have enough posts)
#my_posts = fbapi()

# find the days these interactions took place

# write the data to the database

# visualize using plot.ly(?) posts over time

# create a report



# DarkSky api -------
base_url = 'https://api.darksky.net/forecast/'
api_key = api_info.darksky_key
lat_lng = '42.280841, -83.738115'
full_url = base_url + api_key + '/'+lat_lng

def darkskyapi():
    if lat_lng in CACHE_DICTION:                        #if the location is already in the cache
        uprint("using cached data")                     #print that we are getting the data from the cache
        darksky_results = CACHE_DICTION[location]       #grab data from the cache
    else:                                               #if the locaiton is not already in the cache
        uprint("getting data from internet")            #print that we are getting data from the internet
        darksky_results = requests.get(full_url)
        data = json.loads(darksky_results.text)
        #hourly = data['hourly']['data']
        #print (data)
        CACHE_DICTION[lat_lng] = data
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return darksky_results

print (darkskyapi())


# access exactly 100 interactions for the api; temperature for the last 100 hours in Ann Arbor


# find the days these interactions took place


# write the data to the database

# visualize temperature over time


# create a report



## Part 2 -------------------------------------------------------------------------------------------
# create a report for overall project (not code)

## Part 3 ------------------------------------------------------------------------------------------
