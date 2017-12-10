# Olivia Gardella
# SI206 final project

#import all necessary packages
import sqlite3
import json
import unittest
import itertools
import collections
#import api_info        #don't need this now that I am asking for users to input keys in terminal
import facebook
import requests
from datetime import datetime   #so we can convert timestamps to readable format
import plotly  #to create visualizations for FB and DarkSky
import plotly.plotly as py
import plotly.graph_objs as go

#to take care of unicode error, must use this function instead of print
import sys
def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)

#set up cache
CACHE_FNAME = "project4cache.json"
try:                                            #if the cache file already exists
    cache_file = open(CACHE_FNAME,'r')          #open and read the cache file
    cache_contents = cache_file.read()
    cache_file.close()                          #close the cache file
    CACHE_DICTION = json.loads(cache_contents)  #load cache's contents into the cache dictionary using json
except:                                         #if the cache file doesn't exsit already
    CACHE_DICTION = {}                          #create any empty dictionary for the cache

#API1
#Facebook api
def fbapi():                                                                #define the function
    if "Facebook" in CACHE_DICTION:                                         #if facebook is already in the cache dictionary
        uprint("using cached data")
        data = CACHE_DICTION["Facebook"]                                    #retrieve the data from the dictionary to return
    else:                                                                   #if the id is not yet in the cache dictionary
        #fb_access_token = api_info.fb_access_token                         #don't need now that I ask for token in terminal
        fb_access_token = input('Enter your Facebook access token:')        #ask for the user to input the access token
        graph = facebook.GraphAPI(fb_access_token)                          #connect to the fb graph api
        posts = graph.get_connections(id='me', connection_name='posts')     #retrieve the posts
        uprint("getting data from internet")
        data = []                                                           #initiate an empty data list
        while True:
            try:                                                            #try to iterate through posts and append them to the data list
                for post in posts['data']:
                    data.append(post)
                posts = requests.get(posts['paging']['next']).json()        #go through multiple pages of posts
            except KeyError:                                                #break if it ran out of posts
                break
        CACHE_DICTION["Facebook"] = data                                    #add that data to the cache under that id key
        f = open(CACHE_FNAME, 'w')                                          #open the cache to write to it
        f.write(json.dumps(CACHE_DICTION))                                  #write data to cache in json format
        f.close()                                                           #close the file
    return data                                                             #return the data of posts

#access the fb posts by calling the function
my_posts = fbapi()

#DATABASE1
#create a function that returns the day of the week based on the number outputted from datetime
def day(x):
    days = {0:'Monday', 1:'Tuesday', 2:'Wednesday', 3:'Thursday', 4:'Friday', 5:'Saturday', 6:'Sunday'}
    return days[x]

#to write the data to the database, first connect to sqlite and name file
conn = sqlite3.connect('FBDatabase.sqlite')
cur = conn.cursor()

#if the Facebook table already exists drop it, then create the Facebook table with the following columns
cur.execute('DROP TABLE IF EXISTS Facebook')
cur.execute('CREATE TABLE Facebook (message TEXT, story VARCHAR, created_time VARCHAR, created_day VARCHAR, id VARCHAR)')

#initiate counter so we only get 100 posts, and then iterate through my posts and insert those 100 posts' data into the Facebook table,
#using datetime to make the timestamp readable and the day function to get the day of the week of post
x = 0
for post in my_posts:
    if x < 100:
        cur.execute('INSERT INTO Facebook (message, story, created_time, created_day, id) VALUES (?,?,?,?,?)',
        (post.get('message', 'none'),
        post.get('story', 'none'),
        post['created_time'],
        day(datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000').weekday()),
        post['id']))
        x += 1

#commit all changes to the database
conn.commit()

#VISUALIZATION1
#define a function to create a plot.ly visulization with the facebook data
def fbvisualization():
    try:
        #ask user for their plotly key and username to use for visualizations
        plotly_key = input('Enter your plotly key: ')
        plotly_username = input('Enter your plotly username: ')

        #authenticate plot.ly to use for visualizations
        plotly.tools.set_credentials_file(username=plotly_username, api_key= plotly_key)

        #visualize how many of the posts were posted on which day (mon-sun) aka which day I am most active
        #create a dictionary, go through all of my posts and count how many posts were on each day of the week
        day_counts = {}
        for post in my_posts:
            if day(datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000').weekday()) not in day_counts:
                day_counts[day(datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000').weekday())] = 0
            day_counts[day(datetime.strptime(post['created_time'], '%Y-%m-%dT%H:%M:%S+0000').weekday())] += 1

        #define the labels and values for the different pieces of the pie chart
        labels1 = ['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'Saturday', 'Sunday']
        values1 = [day_counts['Monday'], day_counts['Tuesday'], day_counts['Wednesday'], day_counts['Thursday'], day_counts['Friday'], day_counts['Saturday'], day_counts['Sunday']]

        #create a dictionary with the data to plot (values and labels) and the title of the graph
        fig1 = {
          "data": [
            {
              "values": values1,
              "labels": labels1,
              "type": "pie"
            }],
          "layout": {
                "title":"Days I Post on Facebook",
            }
        }

        #plot the dictionary and name the file
        return py.iplot(fig1, filename='FBpiechart')
    #if the key or username is not correct
    except:
        print ("Cannot create FB visualization without plot.ly key and username")

#call the function to create the Facebook visulization
visualization1 = fbvisualization()





#API2
#DarkSky api
def darkskyapi(lat_lng):
    base_url = 'https://api.darksky.net/forecast/'
    #darksky_key = api_info.darksky_key                                         #dont need now that I ask for key in terminal
    if "DarkSky" in CACHE_DICTION:                                              #if DarkSky is already in the cache
        uprint("using cached data")                                             #print that we are getting the data from the cache
        darksky_results = CACHE_DICTION["DarkSky"]                              #grab data from the cache
    else:                                                                       #if DarkSky is not already in the cache
        darksky_key = input('Enter your DarkSky api key: ')                     #have user input their darksky key in terminal
        uprint("getting data from internet")                                    #print that we are getting data from the internet
        full_url = base_url + darksky_key + '/'+ lat_lng + '?extend=hourly'     #combine parts to create full url, extend=hourly to get 168 instead of 48 hours in future
        darksky_results = requests.get(full_url)                                #retrieve darksky results using url
        darksky_results = json.loads(darksky_results.text)                      #load results in json format
        CACHE_DICTION["DarkSky"] = darksky_results                              #add results to cache dictionary
        f = open(CACHE_FNAME, 'w')                                              #open the cache file to write to it
        f.write(json.dumps(CACHE_DICTION))                                      #write data to cache in json format
        f.close()
    return darksky_results


#access temperature for the next 100 hours in Ann Arbor by calling the function using AA's lat_lng
aa_temps = darkskyapi('42.280841, -83.738115')

#DATABASE2
#connect to sqlite and initate the file so we can write the data to the database
conn = sqlite3.connect('DarkSkyDatabase.sqlite')
cur = conn.cursor()

#if the darksky table already exists, get rid of it, then create the DarkSky table with the following columns
cur.execute('DROP TABLE IF EXISTS DarkSky')
cur.execute('CREATE TABLE DarkSky (time VARCHAR, day VARCHAR, temperature VARCHAR)')

#initiate a counter then update it in for loop in order to only get the next 100 hours of data and
#then iterate through 100 hours and insert data into the DarkSky table
#convert the timestamps to datetime so they are readable
x = 0
for hour in aa_temps['hourly']['data']:
    if x < 100:
        cur.execute('INSERT INTO DarkSky (time, day, temperature) VALUES (?,?,?)',
        (str(datetime.fromtimestamp(hour['time'])),
        day(datetime.fromtimestamp(hour['time']).weekday()),
        hour['temperature']))
        x += 1

#commit all changes to both databases
conn.commit()

#VISUALIZATION2
#define a function to create a dark sky visualization using plot.ly
def darkskyvis():
    try:
        #ask user for their plotly key and username to use for visualizations
        plotly_key = input('Enter your plotly key: ')
        plotly_username = input('Enter your plotly username: ')

        #authenticate plot.ly to use for visualizations
        plotly.tools.set_credentials_file(username=plotly_username, api_key= plotly_key)

        #create lists of both the time and temperature for the next 100 hours by iterating through all the hours and fetching the data
        time = []
        temp = []
        x = 0
        for hour in aa_temps['hourly']['data']:
            if x < 100:
                time.append(str(datetime.fromtimestamp(hour['time'])))
                temp.append(hour['temperature'])
                x += 1

        #create a trace and define what data goes into the x and y axis, which is the two lists created above
        trace2 = go.Scatter(
            x = time,
            y = temp
        )

        #edit the layout of the graph to include a title and x&y labels
        layout2 = dict(title = 'Temperature Over 100 Hours in Ann Arbor',
                      xaxis = dict(title = 'Time'),
                      yaxis = dict(title = 'Temperature (degrees F)'),
                      )

        #turn the data into a list
        data2 = [trace2]

        #create a dictionary of the data and layout, and then plot it using plot.ly and name the file
        fig = dict(data=data2, layout=layout2)
        return py.iplot(fig, filename='DarkSkyGraph')
    #if the key or username is not correct
    except:
        print ("Cannot create DarkSky visualization without plot.ly key and username")

#call function to create the dark sky visualization
visualization2 = darkskyvis()

#close the database connection so not to lock the database
cur.close()
