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

# set up cache <-----MAKE SURE ITS OK TO HAVE BOTH APIS IN SAME CACHE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
    posts = graph.get_connections(id='me', connection_name='posts')
    if user_id in CACHE_DICTION:
        uprint("using cached data")
        data = CACHE_DICTION[user_id]
        #print('----------------------2')
    else:
        uprint("getting data from internet")
        data = []
        while True:
            #print('in loop')
            try:
                #print(type(posts))
                #print(len(posts))
                #print(posts)
                #print(len(posts['data']))
                for post in posts['data']:
                    data.append(post)
                posts = requests.get(posts['paging']['next']).json()
                #print('----------------------loop')
            except KeyError: #ran out of posts
                break
        CACHE_DICTION[user_id] = data
        f = open(CACHE_FNAME, 'w')
        f.write(json.dumps(CACHE_DICTION))
        f.close()
        #print('----------------------finished')
    return data

#print('----------------------runs the function')
# access exactly 100 interactions for the api; 100 of my posts (or less if I don't have enough posts)
my_posts = fbapi('943225772440871')

# find the days these interactions took place <---- ASK IF THIS BEING IN DATABASE IS OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# x = my_posts[0]['created_time']
# print(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+0000').weekday())
# print(datetime.today().weekday())

def day(x):
    days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    return days[x]
# print(fbday(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+0000').weekday()))

# write the data to the database
conn = sqlite3.connect('FBDatabase.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (message TEXT, story VARCHAR, created_time VARCHAR, created_day VARCHAR, id VARCHAR)')

x = 0
for post in my_posts:
    if x < 100:
    #print(post.keys())
        cur.execute('INSERT INTO Facebook (message, story, created_time, created_day, id) VALUES (?,?,?,?,?)',
        (post.get('message', 'none'),
        post.get('story', 'none'),
        post['created_time'],
        day(datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000').weekday()),
        post['id']))
        x += 1

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

# find the days these interactions took place??? <-MAKE SURE THIS IS OK, GETTING THE DAY ITS HAPPENING!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# x = aa_temps['hourly']['data'][0]['time']
# print (x)
# print(datetime.fromtimestamp(x).weekday())
# print(datetime.fromtimestamp(aa_temps['hourly']['data'][86]['time']).weekday())
# print(datetime.strptime(x, '%Y-%m-%dT%H:%M:%S+0000').weekday())
# print(datetime.today().weekday())

# write the data to the database
conn = sqlite3.connect('DarkSkyDatabase.sqlite')                                #connect to sqlite and initate the file
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS DarkSky')                                                  #if the darksky table already exists, get rid of it
cur.execute('CREATE TABLE DarkSky (time VARCHAR, day VARCHAR, temperature VARCHAR)')         #create the DarkSky table with the following columns

x = 0
for hour in aa_temps['hourly']['data']:
    #print (hour['temperature'])
    if x < 100:
        cur.execute('INSERT INTO DarkSky (time, day, temperature) VALUES (?,?,?)',
        (str(datetime.fromtimestamp(hour['time'])),                             #convert to datetime
        day(datetime.fromtimestamp(hour['time']).weekday()),
        hour['temperature']))
        x += 1

conn.commit()                                                                   #commit all changes to both databases



# visualize temperature over time using plot.ly

import plotly.plotly as py
import plotly.graph_objs as go

plotly.tools.set_credentials_file(username='gardella', api_key= api_info.plotly_key)

time = []
temp = []
x = 0
for hour in aa_temps['hourly']['data']:
    if x < 100:
        time.append(str(datetime.fromtimestamp(hour['time'])))
        temp.append(hour['temperature'])
        x += 1

# Create a trace
trace = go.Scatter(
    x = time,
    y = temp
)

# Edit the layout
layout = dict(title = 'Temperature Over 100 Hours in Ann Arbor',
              xaxis = dict(title = 'Time'),
              yaxis = dict(title = 'Temperature (degrees F)'),
              )

data = [trace]

fig = dict(data=data, layout=layout)
py.iplot(fig, filename='DarkSkyGraph')


# create a report <--HOW/WHAT DOES THIS MEAN??!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!




cur.close()

## Part 2 -------------------------------------------------------------------------------------------
# create a report for overall project (not code)

## Part 3 ------------------------------------------------------------------------------------------
