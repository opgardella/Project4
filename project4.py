# Olivia Gardella
# SI206 final project

import sqlite3
import json
import unittest
import itertools
import collections
import api_info                 #import python file that has the api keys
import facebook
import requests
from datetime import datetime
import plotly

#notes: plot.ly, google maps to visualize

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
def fbapi(user_id):
    fb_access_token = api_info.fb_access_token
    graph = facebook.GraphAPI(fb_access_token)
    posts = graph.get_connections('me','posts')
    if user_id in CACHE_DICTION:
        uprint("using cached data")
        FBresults = CACHE_DICTION[user_id]
    else:
        uprint("getting data from internet")
        data = []
        while True:
            try:
            	for post in posts['data']:
                    data.append(post)
            	FBresults = requests.get(posts['paging']['next']).json()
            except KeyError:
            	#ran out of posts
            	break
        CACHE_DICTION[user_id] = data
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
    return FBresults



# access exactly 100 interactions for the api; 100 of my posts (or less if I don't have enough posts)
my_posts = fbapi('943225772440871')

# find the days these interactions took place

# write the data to the database
conn = sqlite3.connect('FBDatabase.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (message TEXT, story VARCHAR, created_time VARCHAR, id VARCHAR)')

# x = 0
for post in my_posts:
    # if x < 100:
    print(post.keys())
    cur.execute('INSERT INTO Facebook (message, story, created_time, id) VALUES (?,?,?,?)',
    (post.get('message', 'none'), post.get('story', 'none'), post['created_time'], post['id']))  #HOW TO CHANGE STORY TO MESSAGE, optional message?
        # x += 1

conn.commit()

# visualize using google maps

# create a report



# DarkSky api -------
def darkskyapi(lat_lng):
    base_url = 'https://api.darksky.net/forecast/'
    api_key = api_info.darksky_key                                              #retrieve darksky api key from api_info file
    full_url = base_url + api_key + '/'+ lat_lng + '?extend=hourly'             #combine parts to create full url, extend=hourly to get 168 instead of 48 hours in future
    if lat_lng in CACHE_DICTION:                                                #if the location is already in the cache
        uprint("using cached data")                                             #print that we are getting the data from the cache
        darksky_results = CACHE_DICTION[lat_lng]                                #grab data from the cache
    else:                                                                       #if the locaiton is not already in the cache
        uprint("getting data from internet")                                    #print that we are getting data from the internet
        darksky_results = requests.get(full_url)                                #retrieve darksky results using url
        data = json.loads(darksky_results.text)                                 #load results in json format
        CACHE_DICTION[lat_lng] = data                                           #add results to cache dictionary
        f = open(CACHE_FNAME, 'w')                                              #open the cache file to write to it
        f.write(json.dumps(CACHE_DICTION))                                      #write data to cache in json format
        f.close()
    return darksky_results


# access exactly 100 interactions for the api; temperature for the next 100 hours in Ann Arbor
aa_temps = darkskyapi('42.280841, -83.738115')

# find the days these interactions took place???

# write the data to the database
conn = sqlite3.connect('DarkSkyDatabase.sqlite')                                #connect to sqlite and initate the file
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS DarkSky')                                     #if the darksky table already exists, get rid of it
cur.execute('CREATE TABLE DarkSky (time VARCHAR, temperature VARCHAR)')         #create the DarkSky table with the following columns

x = 0
for hour in aa_temps['hourly']['data']:
    #print (hour['temperature'])
    if x < 100:
        cur.execute('INSERT INTO DarkSky (time, temperature) VALUES (?,?)',
        (str(datetime.fromtimestamp(hour['time'])),                             #convert to datetime
        hour['temperature']))
        x += 1

conn.commit()                                                                   #commit all changes to both databases

cur.close()                                                                     #close the databases

# visualize temperature over time using plot.ly

# df = pd.DataFrame( [[ij for ij in i] for i in rows] )
# df.rename(columns={0: 'Name', 1: 'Continent', 2: 'Population', 3: 'LifeExpectancy', 4:'GNP'}, inplace=True);
# df = df.sort(['LifeExpectancy'], ascending=[1]);
#
# country_names = df['Name']
# for i in range(len(country_names)):
#     try:
#         country_names[i] = str(country_names[i]).decode('utf-8')
#     except:
#         country_names[i] = 'Country name decode error'
#
# trace1 = Scatter(
#     x=df['GNP'],
#     y=df['LifeExpectancy'],
#     text=country_names,
#     mode='markers'
# )
# layout = Layout(
#     title='DarkSky: Temperature over next 100 hours in AA',
#     xaxis=XAxis( type='log', title='Temperature' ),
#     yaxis=YAxis( title='Time' ),
# )
# data = Data([trace1])
# fig = Figure(data=data, layout=layout)
# py.iplot(fig, filename='DarkSkyGraph')

# create a report - TALK TO GSI ABOUT HOW I CANT DO THIS BUT I FORGOT TO PUT THAT IN MY REPORT



## Part 2 -------------------------------------------------------------------------------------------
# create a report for overall project (not code)

## Part 3 ------------------------------------------------------------------------------------------
